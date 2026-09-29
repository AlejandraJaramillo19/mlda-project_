from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="I-CARE Records Explorer",
    page_icon="🧠",
    layout="wide",
)

PROJECT_ROOT = Path(__file__).resolve().parent

BASE_URL = "https://physionet.org/files/i-care/2.1"
RECORDS_URL = f"{BASE_URL}/RECORDS"

PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"
PROCESSED_EEG_DIR = PROCESSED_DATA / "eeg_sample"

TARGET_FS = 200

COMMON_CHANNELS = [
    "Fp1", "Fp2",
    "F3", "F4",
    "C3", "C4",
    "P3", "P4",
    "O1", "O2",
    "F7", "F8",
    "T3", "T4",
    "T5", "T6",
    "Fz", "Cz", "Pz",
]


# ============================================================
# SESIÓN HTTP
# ============================================================

@st.cache_resource
def get_session():
    """
    Crea una sesión HTTP con reintentos automáticos.
    """

    session = requests.Session()

    retries = Retry(
        total=5,
        backoff_factor=1.5,
        status_forcelist=[502, 503, 504],
        allowed_methods=["GET"],
    )

    session.mount(
        "https://",
        HTTPAdapter(max_retries=retries)
    )

    return session


# ============================================================
# OBTENER PACIENTES
# ============================================================

@st.cache_data(show_spinner=False)
def get_patient_ids():
    """
    Obtiene los identificadores de pacientes disponibles
    en I-CARE.
    """

    response = requests.get(
        RECORDS_URL,
        timeout=30
    )

    response.raise_for_status()

    records = response.text.splitlines()

    patient_ids = [
        record.strip("/").split("/")[-1]
        for record in records
        if record.strip()
    ]

    return patient_ids


# ============================================================
# CONSTRUIR INVENTARIO DE RECORDS
# ============================================================

@st.cache_data(show_spinner=False)
def build_records_dataframe(patient_ids):
    """
    Consulta el archivo RECORDS de cada paciente y construye
    el inventario global de registros fisiológicos.
    """

    session = get_session()

    physiological_records = []

    for patient_id in patient_ids:

        records_url = (
            f"{BASE_URL}/training/"
            f"{patient_id}/RECORDS"
        )

        try:

            response = session.get(
                records_url,
                timeout=30
            )

            response.raise_for_status()

            patient_records = (
                response.text
                .strip()
                .splitlines()
            )

        except requests.RequestException:
            continue

        for record in patient_records:

            record = record.strip()

            if not record:
                continue

            if record.endswith("_EEG"):
                modality = "EEG"

            elif record.endswith("_ECG"):
                modality = "ECG"

            elif record.endswith("_OTHER"):
                modality = "OTHER"

            elif record.endswith("_REF"):
                modality = "REF"

            else:
                modality = "UNKNOWN"

            physiological_records.append(
                {
                    "Patient": patient_id,
                    "Record": record,
                    "Modality": modality,
                }
            )

    return pd.DataFrame(
        physiological_records
    )


# ============================================================
# DETECTAR EEG PROCESADOS
# ============================================================

@st.cache_data(show_spinner=False)
def find_processed_eeg():
    """
    Busca los archivos .npy generados por el pipeline EEG.

    Estructura esperada:

    data/processed/eeg_sample/
        patient/
            record.npy
    """

    files = sorted(
        PROCESSED_EEG_DIR.glob("*/*.npy")
    )

    rows = []

    for file in files:

        record = file.stem
        patient = file.parent.name

        parts = record.split("_")

        try:
            segment = int(parts[1])
            hour = int(parts[2])

        except (IndexError, ValueError):
            segment = None
            hour = None

        rows.append(
            {
                "Patient": patient,
                "Record": record,
                "Segment": segment,
                "Hour": hour,
                "Path": str(file),
            }
        )

    return pd.DataFrame(rows)


# ============================================================
# INTERFAZ PRINCIPAL
# ============================================================

st.title("🧠 I-CARE Records Explorer")

st.caption(
    "Exploración interactiva de los registros fisiológicos "
    "del dataset I-CARE."
)

st.divider()


# ============================================================
# CARGA DEL INVENTARIO
# ============================================================

try:

    with st.spinner(
        "Consultando estructura RECORDS de I-CARE..."
    ):

        patient_ids = get_patient_ids()

        records_df = build_records_dataframe(
            tuple(patient_ids)
        )

except Exception as error:

    st.error(
        "No fue posible consultar los registros de I-CARE."
    )

    st.exception(error)

    st.stop()


if records_df.empty:

    st.error(
        "No se encontraron registros fisiológicos."
    )

    st.stop()


# ============================================================
# DATAFRAME EEG
# ============================================================

eeg_df = records_df[
    records_df["Modality"] == "EEG"
].copy()


# ------------------------------------------------------------
# Extraer paciente, segmento y hora del nombre del registro
# ------------------------------------------------------------

record_parts = eeg_df["Record"].str.extract(
    r"^(?P<Patient_ID>\d+)_"
    r"(?P<Segment>\d+)_"
    r"(?P<Hour>\d+)_EEG$"
)

eeg_df["Segment"] = pd.to_numeric(
    record_parts["Segment"],
    errors="coerce"
)

eeg_df["Hour"] = pd.to_numeric(
    record_parts["Hour"],
    errors="coerce"
)


# ============================================================
# SELECCIÓN TEMPORAL EEG
# ============================================================

eeg_24_32 = eeg_df[
    eeg_df["Hour"].between(
        24,
        32,
        inclusive="both"
    )
].copy()


SELECTED_HOURS = [
    24,
    26,
    28,
    30,
    32,
]


eeg_selected = eeg_df[
    eeg_df["Hour"].isin(
        SELECTED_HOURS
    )
].copy()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("Filtros")

modalities = sorted(
    records_df["Modality"]
    .dropna()
    .unique()
)

selected_modality = st.sidebar.multiselect(
    "Modalidad",
    modalities,
    default=modalities,
)


filtered_df = records_df[
    records_df["Modality"].isin(
        selected_modality
    )
]


# ============================================================
# KPIs GENERALES
# ============================================================

col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Pacientes",
    records_df["Patient"].nunique()
)


col2.metric(
    "Registros fisiológicos",
    f"{len(records_df):,}"
)


col3.metric(
    "Registros EEG",
    f"{len(eeg_df):,}"
)


col4.metric(
    "Modalidades",
    records_df["Modality"].nunique()
)


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📊 Overview",
        "🧠 EEG",
        "🔎 Records",
        "⚙️ Pipeline",
        "📈 EEG Signals",
    ]
)


# ============================================================
# TAB 1 — OVERVIEW
# ============================================================

with tab1:

    st.subheader(
        "Distribución de modalidades fisiológicas"
    )

    modality_counts = (
        records_df["Modality"]
        .value_counts()
        .reset_index()
    )

    modality_counts.columns = [
        "Modality",
        "Records"
    ]


    fig = px.bar(
        modality_counts,
        x="Modality",
        y="Records",
        text_auto=True,
        title="Registros por modalidad",
    )

    fig.update_layout(
        xaxis_title="Modalidad",
        yaxis_title="Número de registros",
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


    # --------------------------------------------------------
    # Registros por paciente
    # --------------------------------------------------------

    st.subheader(
        "Registros por paciente"
    )

    records_per_patient = (
        records_df
        .groupby("Patient")
        .size()
        .reset_index(
            name="Number_of_records"
        )
    )


    fig = px.histogram(
        records_per_patient,
        x="Number_of_records",
        nbins=30,
        title=(
            "Distribución del número "
            "de registros por paciente"
        ),
    )

    fig.update_layout(
        xaxis_title="Número de registros",
        yaxis_title="Pacientes",
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


# ============================================================
# TAB 2 — EEG
# ============================================================

with tab2:

    st.subheader(
        "Disponibilidad temporal de EEG"
    )


    c1, c2, c3 = st.columns(3)


    c1.metric(
        "EEG totales",
        f"{len(eeg_df):,}"
    )


    c2.metric(
        "EEG 24–32 h",
        f"{len(eeg_24_32):,}"
    )


    c3.metric(
        "Horas seleccionadas",
        f"{len(eeg_selected):,}"
    )


    # --------------------------------------------------------
    # Distribución por hora
    # --------------------------------------------------------

    records_by_hour = (
        eeg_24_32
        .groupby("Hour")
        .size()
        .reset_index(
            name="Records"
        )
    )


    fig = px.bar(
        records_by_hour,
        x="Hour",
        y="Records",
        text_auto=True,
        title=(
            "Registros EEG disponibles "
            "por hora"
        ),
    )

    fig.update_layout(
        xaxis_title="Hora",
        yaxis_title="Registros EEG",
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


    # --------------------------------------------------------
    # Solo horas seleccionadas
    # --------------------------------------------------------

    st.subheader(
        "Horas seleccionadas para el análisis"
    )


    selected_by_hour = (
        eeg_selected
        .groupby("Hour")
        .size()
        .reset_index(
            name="Records"
        )
    )


    fig = px.bar(
        selected_by_hour,
        x="Hour",
        y="Records",
        text_auto=True,
        title=(
            "EEG en 24, 26, 28, 30 y 32 horas"
        ),
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=SELECTED_HOURS
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


# ============================================================
# TAB 3 — RECORDS
# ============================================================

with tab3:

    st.subheader(
        "Inventario de registros"
    )


    search = st.text_input(
        "Buscar paciente o registro"
    )


    table = filtered_df.copy()


    if search:

        mask = (
            table["Patient"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
            |
            table["Record"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        )

        table = table[mask]


    st.dataframe(
        table,
        width="stretch",
        hide_index=True,
        height=500,
    )


    st.caption(
        f"{len(table):,} registros mostrados"
    )


# ============================================================
# TAB 4 — PIPELINE
# ============================================================

with tab4:

    st.subheader(
        "Pipeline de selección EEG"
    )


    # --------------------------------------------------------
    # IMPORTANTE:
    #
    # 2590 y 2421 corresponden a resultados obtenidos en el
    # notebook después de inspeccionar los headers EEG.
    #
    # Posteriormente conviene guardar estos resultados como
    # archivos procesados y leerlos directamente desde aquí.
    # --------------------------------------------------------

    NOTEBOOK_ELIGIBLE = 2590
    NOTEBOOK_PATIENT_HOUR = 2421


    funnel = pd.DataFrame(
        {
            "Etapa": [
                "EEG iniciales",
                "24–32 h",
                "24, 26, 28, 30, 32 h",
                "Elegibles",
                "Paciente-hora",
            ],

            "Registros": [
                len(eeg_df),
                len(eeg_24_32),
                len(eeg_selected),
                NOTEBOOK_ELIGIBLE,
                NOTEBOOK_PATIENT_HOUR,
            ],
        }
    )


    fig = px.funnel(
        funnel,
        x="Registros",
        y="Etapa",
        title=(
            "Reducción progresiva "
            "del conjunto EEG"
        ),
    )


    st.plotly_chart(
        fig,
        width="stretch"
    )


    # --------------------------------------------------------
    # Pipeline técnico
    # --------------------------------------------------------

    st.subheader(
        "Preprocesamiento"
    )


    st.markdown(
        """
Cada registro seleccionado sigue el pipeline:

**EEG original**

↓

**Ventana central de 90 segundos**

↓

**19 canales EEG comunes**

↓

**Conversión digital → física**

↓

**Remuestreo a 200 Hz**

↓

**Filtro pasa banda 0.5–70 Hz**

↓

**Filtro notch 50 Hz**

↓

### Representación final

**19 canales × 18.000 muestras**

equivalentes a:

**90 segundos × 200 Hz**
"""
    )


# ============================================================
# TAB 5 — EEG SIGNALS
# ============================================================

with tab5:

    st.subheader(
        "Exploración de señales EEG procesadas"
    )


    processed_eeg = find_processed_eeg()


    if processed_eeg.empty:

        st.info(
            "No se encontraron EEG procesados en "
            "data/processed/eeg_sample."
        )


    else:

        # ====================================================
        # RESUMEN DE EEG PROCESADOS
        # ====================================================

        c1, c2, c3 = st.columns(3)


        c1.metric(
            "EEG procesados",
            f"{len(processed_eeg):,}"
        )


        c2.metric(
            "Pacientes",
            processed_eeg[
                "Patient"
            ].nunique()
        )


        c3.metric(
            "Horas disponibles",
            processed_eeg[
                "Hour"
            ].nunique()
        )


        st.divider()


        # ====================================================
        # SELECTOR DE PACIENTE
        # ====================================================

        patients = sorted(
            processed_eeg[
                "Patient"
            ].unique()
        )


        selected_patient = st.selectbox(
            "Paciente",
            patients,
            key="eeg_patient",
        )


        patient_records = processed_eeg[
            processed_eeg["Patient"]
            == selected_patient
        ].sort_values(
            [
                "Hour",
                "Segment"
            ]
        )


        # ====================================================
        # SELECTOR DE REGISTRO
        # ====================================================

        selected_record = st.selectbox(
            "Registro",
            patient_records[
                "Record"
            ].tolist(),
            key="eeg_record",
        )


        # ====================================================
        # SELECTOR DE CANAL
        # ====================================================

        selected_channel = st.selectbox(
            "Canal EEG",
            COMMON_CHANNELS,
            key="eeg_channel",
        )


        row = patient_records[
            patient_records["Record"]
            == selected_record
        ].iloc[0]


        # ====================================================
        # CARGAR EEG
        # ====================================================

        try:

            signal = np.load(
                row["Path"]
            )

        except Exception as error:

            st.error(
                "No fue posible cargar el archivo EEG."
            )

            st.exception(error)

            st.stop()


        # ====================================================
        # VALIDACIÓN
        # ====================================================

        if signal.shape != (
            19,
            18000
        ):

            st.error(
                f"Dimensión inesperada: "
                f"{signal.shape}. "
                "Se esperaba (19, 18000)."
            )

            st.stop()


        if not np.isfinite(
            signal
        ).all():

            st.error(
                "La señal contiene valores "
                "no finitos."
            )

            st.stop()


        # ====================================================
        # INFORMACIÓN DEL REGISTRO
        # ====================================================

        hour_value = row["Hour"]

        if pd.notna(hour_value):

            hour_text = (
                f"{int(hour_value)} h"
            )

        else:

            hour_text = "N/A"


        c1, c2, c3, c4 = st.columns(4)


        c1.metric(
            "Paciente",
            selected_patient
        )


        c2.metric(
            "Hora",
            hour_text
        )


        c3.metric(
            "Canal",
            selected_channel
        )


        c4.metric(
            "Duración",
            "90 s"
        )


        # ====================================================
        # EXTRAER CANAL
        # ====================================================

        channel_index = (
            COMMON_CHANNELS.index(
                selected_channel
            )
        )


        channel_signal = signal[
            channel_index
        ]


        time = (
            np.arange(
                channel_signal.size
            )
            / TARGET_FS
        )


        # ====================================================
        # VISUALIZACIÓN DEL CANAL
        # ====================================================

        st.subheader(
            f"Canal {selected_channel}"
        )


        plot_df = pd.DataFrame(
            {
                "Time (s)": time,
                "Amplitude": channel_signal,
            }
        )


        fig = px.line(
            plot_df,
            x="Time (s)",
            y="Amplitude",
            title=(
                f"{selected_patient} — "
                f"{selected_record} — "
                f"{selected_channel}"
            ),
        )


        fig.update_layout(
            xaxis_title="Tiempo (s)",
            yaxis_title="Amplitud",
            hovermode="x unified",
        )


        st.plotly_chart(
            fig,
            width="stretch"
        )


        # ====================================================
        # VENTANA DE ZOOM
        # ====================================================

        st.subheader(
            "Exploración temporal"
        )


        time_window = st.slider(
            "Ventana temporal (segundos)",
            min_value=0,
            max_value=90,
            value=(0, 10),
            step=1,
        )


        start_sample = int(
            time_window[0]
            * TARGET_FS
        )


        end_sample = int(
            time_window[1]
            * TARGET_FS
        )


        zoom_signal = (
            channel_signal[
                start_sample:end_sample
            ]
        )


        zoom_time = (
            np.arange(
                start_sample,
                end_sample
            )
            / TARGET_FS
        )


        zoom_df = pd.DataFrame(
            {
                "Time (s)": zoom_time,
                "Amplitude": zoom_signal,
            }
        )


        fig_zoom = px.line(
            zoom_df,
            x="Time (s)",
            y="Amplitude",
            title=(
                f"{selected_channel} — "
                f"{time_window[0]} a "
                f"{time_window[1]} segundos"
            ),
        )


        fig_zoom.update_layout(
            xaxis_title="Tiempo (s)",
            yaxis_title="Amplitud",
            hovermode="x unified",
        )


        st.plotly_chart(
            fig_zoom,
            width="stretch"
        )


        # ====================================================
        # ESTADÍSTICAS DEL CANAL
        # ====================================================

        st.subheader(
            "Estadísticas de la señal"
        )


        stats = pd.DataFrame(
            {
                "Estadístico": [
                    "Media",
                    "Desviación estándar",
                    "Mínimo",
                    "Máximo",
                    "Número de muestras",
                    "Frecuencia de muestreo",
                    "Duración",
                ],

                "Valor": [
                    float(
                        np.mean(
                            channel_signal
                        )
                    ),

                    float(
                        np.std(
                            channel_signal
                        )
                    ),

                    float(
                        np.min(
                            channel_signal
                        )
                    ),

                    float(
                        np.max(
                            channel_signal
                        )
                    ),

                    len(
                        channel_signal
                    ),

                    TARGET_FS,

                    (
                        len(
                            channel_signal
                        )
                        / TARGET_FS
                    ),
                ],
            }
        )


        st.dataframe(
            stats,
            width="stretch",
            hide_index=True,
        )


        # ====================================================
        # INFORMACIÓN DEL ARCHIVO
        # ====================================================

        with st.expander(
            "Información del archivo"
        ):

            st.write(
                "**Paciente:**",
                selected_patient
            )

            st.write(
                "**Registro:**",
                selected_record
            )

            st.write(
                "**Segmento:**",
                row["Segment"]
            )

            st.write(
                "**Hora:**",
                row["Hour"]
            )

            st.write(
                "**Dimensiones:**",
                signal.shape
            )

            st.write(
                "**Frecuencia:**",
                f"{TARGET_FS} Hz"
            )

            st.write(
                "**Archivo:**",
                row["Path"]
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "I-CARE • Data Preparation & Analysis • "
    "Records / EEG"
)