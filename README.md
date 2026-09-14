# I-CARE Data Analysis

Análisis exploratorio y descriptivo del conjunto de datos I-CARE v2.1 para la caracterización clínica y fisiológica de pacientes en estado de coma tras un paro cardiaco.

## Descripción

Este proyecto se centra en el estudio del conjunto de datos I-CARE (International Cardiac Arrest REsearch consortium Database), versión 2.1, distribuido a través de PhysioNet. El objetivo principal es caracterizar clínicamente a los pacientes incluidos en la base de datos y explorar la disponibilidad, estructura y relevancia de registros fisiológicos, especialmente EEG, en el contexto de la predicción pronóstica neurológica tras un paro cardíaco.

La investigación se fundamenta en la premisa de que la recuperación neurológica tras una parada cardiorrespiratoria no puede evaluarse únicamente con la supervivencia inmediata. En muchos pacientes, la recuperación de la circulación espontánea (ROSC) no garantiza una recuperación cerebral favorable; por ello, la evaluación del desenlace neurológico requiere considerar variables clínicas, temporales y fisiológicas. En este contexto, la información demográfica y clínica del paciente, junto con registros electrofisiológicos como EEG, ECG, OTHER y REF, ofrece una visión más completa de la evolución clínica y del pronóstico neurológico.

La documentación disponible en el repositorio indica que el trabajo actual se ha desarrollado en un enfoque descriptivo, exploratorio y metodológicamente reproducible, siguiendo la filosofía de CRISP-DM y priorizando la etapa de entendimiento del negocio y del dato antes de avanzar hacia análisis más complejos o modelos predictivos.

## Objetivos

### Objetivo general

Caracterizar el conjunto de datos I-CARE v2.1 y analizar de manera exploratoria la relación entre variables clínicas y la disponibilidad/estructura de registros fisiológicos, con especial atención a la información relevante para la evaluación del pronóstico neurológico tras un paro cardíaco.

### Objetivos específicos

1. Comprender el contexto clínico y la problemática pronóstica asociada a la supervivencia tras paro cardíaco y coma post-ROSC.
2. Revisar la estructura del conjunto de datos, las variables clínicas disponibles y la organización de los registros fisiológicos.
3. Integrar los metadatos clínicos de los pacientes en un formato tabular reproducible para su análisis descriptivo.
4. Explorar la calidad de los datos, la presencia de valores faltantes y la transformación necesaria para análisis estadísticos.
5. Describir la distribución de variables como edad, ROSC, TTM y desenlace neurológico (por ejemplo, CPC) en la población analizada.
6. Examinar la disponibilidad y estructura de registros EEG, ECG, OTHER y REF, con énfasis en la organización por paciente y por tipo de señal.
7. Preparar una base analítica y una documentación técnica que permita continuar el proyecto de forma reproducible en etapas posteriores.

## Fuente de datos

El proyecto utiliza el conjunto de datos I-CARE v2.1, disponible en PhysioNet. La documentación del repositorio y los notebooks indican que la base contiene una rama clínica y una rama fisiológica, ambas asociadas a pacientes adultos con paro cardíaco, especialmente con retorno de circulación espontánea (ROSC) y permanencia en estado de coma.

La documentación disponible en los notebooks señala que el conjunto público de entrenamiento comprende 607 pacientes. Además, se menciona que el conjunto fisiológico completo incluye registros de tipo EEG, ECG, OTHER y REF, y que el análisis de señal puede abarcar enormes volúmenes de datos, con un alcance total estimado del orden de 1.5 TB para la base completa de señales fisiológicas.

### Distinción entre datos clínicos y fisiológicos

El proyecto distingue claramente dos niveles conceptuales:

1. Metadatos clínicos del paciente
   - Archivos de texto plano por paciente.
   - Información demográfica y clínica: edad, sexo, hospital, localización del paro, ritmo inicial, ROSC, TTM, desenlace, CPC, entre otros.

2. Registros fisiológicos
   - Organizados por paciente y por tipo de modalidad.
   - EEG, ECG, OTHER y REF.
   - Cada registro fisiológico se acompaña de archivos de encabezado (`.hea`) y de señales en formato MATLAB (`.mat`), siguiendo el estándar WFDB/PhysioNet.

Esta separación es clave para el diseño del proyecto: los metadatos clínicos permiten un análisis descriptivo y inferencial a escala de paciente, mientras que los registros fisiológicos requieren un tratamiento específico por volumen, formato y complejidad de señal.

## Metodología

El proyecto sigue la metodología CRISP-DM (Cross-Industry Standard Process for Data Mining), adaptada al análisis de datos clínicos y fisiológicos.

### Fases documentadas o implementadas

1. Entendimiento del negocio
   - Se define el problema clínico, la necesidad de evaluar pronóstico neurológico y la relevancia del EEG como fuente de información multimodal.
   - Se revisa el rol del CPC, ROSC, TTM y la descripción clínico-pronóstica del contexto post-paro cardiaco.

2. Entendimiento de los datos
   - Se inspecciona la estructura del dataset, la organización por paciente y por registros fisiológicos.
   - Se revisan los archivos `RECORDS`, las variables clínicas y la disponibilidad de señales.

3. Preparación de los datos
   - Se integran los metadatos de pacientes desde archivos individuales a un DataFrame consolidado.
   - Se corrigen y normalizan tipos de datos, con tratamiento específico de valores faltantes y cadenas tipo `nan`.

4. Análisis descriptivo y exploratorio
   - Se analizan distribuciones de variables como edad, ROSC y TTM.
   - Se comparan grupos por desenlace neurológico y se revisan correlaciones y asociaciones descriptivas.

5. Evaluación
   - Se comparan patrones clínicos entre grupos según resultado, aunque el proyecto actual se mantiene en un nivel descriptivo y no finaliza con una validación predictiva concluyente.

6. Implementación / despliegue
   - No constituye un objetivo explícito del repositorio actual. La documentación disponible se concentra en análisis y caracterización del conjunto de datos, no en un producto operativo final.

## Estructura de los datos

La organización conceptual del dataset puede resumirse de la siguiente forma:

```text
I-CARE
├── paciente
│   ├── metadata_clinica (.txt)
│   └── RECORDS
│       ├── EEG
│       │   ├── *.hea
│       │   └── *.mat
│       ├── ECG
│       │   ├── *.hea
│       │   └── *.mat
│       ├── OTHER
│       │   ├── *.hea
│       │   └── *.mat
│       └── REF
│           ├── *.hea
│           └── *.mat
```

En esta estructura, cada paciente posee una identidad definida y una carpeta de registros. Los metadatos clínicos describen la historia clínica del paciente; los registros fisiológicos contienen señales que pueden ser revisadas a nivel de disponibilidad, tipo de modalidad y estructura del encabezado.

## Estructura del repositorio

La organización actual del repositorio es la siguiente:

```text
mlda-project/
├── .gitignore
├── README.md
├── requirements.txt
├── config/
├── data/
│   ├── raw/
│   │   ├── clinical/
│   │   └── eeg/
│   ├── interim/
│   └── processed/
├── notebooks/
│   ├── 01_understanding_business/
│   │   ├── 01_M1U2_fase_1_Entendimiento_del_negocio.ipynb
│   │   └── Plan_Proyecto_ICARE_CRISP_DM_corregido_1.pdf
│   └── 02_understanding_data/
│       └── 02_understanding_data.ipynb
├── results/
│   ├── figures/
│   └── tables/
├── src/
│   ├── analysis/
│   ├── data/
│   ├── preprocessing/
│   └── visualization/
└── .venv/   # entorno local, no versionado
```

### Propósito de las principales carpetas

| Directorio | Propósito |
|---|---|
| `config/` | Directorio de configuración del proyecto; actualmente vacío o sin artefactos versionados relevantes. |
| `data/raw/` | Datos originales no versionados y no incluidos en Git. Aquí se almacenan fuentes brutas, por ejemplo metadata clínica y registros fisiológicos. |
| `data/interim/` | Datos intermedios de preparación. |
| `data/processed/` | Datos ya transformados, limpios o listos para análisis. |
| `notebooks/` | Análisis exploratorio, documentación metodológica y trabajo de investigación en formato notebook. |
| `results/figures/` | Figuras generadas por los análisis. |
| `results/tables/` | Tablas y resúmenes exportados. |
| `src/` | Código fuente de análisis, preparación y visualización. |
| `requirements.txt` | Dependencias reproducibles del entorno. |

## Notebooks

El repositorio cuenta con los siguientes notebooks relevantes:

| Notebook | Fase | Propósito |
|---|---|---|
| `01_M1U2_fase_1_Entendimiento_del_negocio.ipynb` | Entendimiento del negocio | Contexto clínico del paro cardíaco, pronóstico neurológico, uso del EEG y objetivos del proyecto. |
| `02_understanding_data.ipynb` | Entendimiento de los datos | Descarga, integración, limpieza y análisis exploratorio inicial de los metadatos clínicos y de los registros fisiológicos. |
| `Plan_Proyecto_ICARE_CRISP_DM_corregido_1.pdf` | Planificación de proyecto | Documento de plan del proyecto, estructurado según CRISP-DM, con alcance del estudio. |

La documentación del repositorio sugiere una secuencia de trabajo orientada a: (1) entendimiento del negocio, (2) entendimiento de los datos, y (3) preparación y análisis descriptivo. No se observa en este repositorio una fase de despliegue o un producto final de software clínico operacional.

## Flujo de análisis de datos

El flujo de trabajo documentado en los notebooks se puede resumir así:

```text
I-CARE
→ identificación de pacientes
→ metadatos clínicos por paciente
→ DataFrame consolidado de pacientes
→ limpieza y normalización
→ análisis descriptivo
→ comparación por desenlace neurológico
→ exploración de registros fisiológicos
→ clasificación por modalidad (EEG / ECG / OTHER / REF)
→ inventario de registros por paciente
→ inspección de encabezados .hea
→ análisis exploratorio de señales .mat
```

En la rama fisiológica, el notebook describe un proceso conceptual de inventario y selección de registros que incluye:

- listado de `RECORDS` por paciente,
- identificación de registros por modalidad,
- análisis del contenido de cada archivo `.hea`,
- posterior análisis de señales de EEG y otras modalidades en una muestra seleccionada.

## Resultados preliminares

Los resultados documentados en el repositorio son de naturaleza preliminar y descriptiva. Se basan en el análisis exploratorio de los datos clínicos y en la caracterización de los registros fisiológicos, pero no constituyen una conclusión clínica final ni una validación predictiva concluida.

| Aspecto | Valor documentado | Observación |
|---|---:|---|
| Pacientes del conjunto clínico | 607 | Conjunto de entrenamiento público de I-CARE v2.1. |
| Registros clínicos | 607 | Uno por paciente en el DataFrame consolidado. |
| Registros fisiológicos | 80,809 | Señales/segmentos documentados por el notebook. |
| Variables clínicas por paciente | 10 | Incluye por ejemplo `Patient`, `Hospital`, `Age`, `Sex`, `ROSC`, `TTM`, `Outcome`, `CPC`. |
| Tamaño estimado del archivo clínico integrado | ~23 KB | Documento en el notebook como archivo CSV de metadatos clínicos. |
| Volumen estimado de la base fisiológica completa | ~1.5 TB | El notebook lo presenta como un volumen potencialmente elevado para almacenamiento personal. |

Además, los notebooks documentan observaciones descriptivas relevantes en la población analizada, por ejemplo:

- la edad y el tiempo hasta ROSC aparecen asociados a grupos con desenlace neurológico diferente,
- la variable `TTM` presenta una distribución muy concentrada en valores típicos del protocolo, más cercana a una estructura discreta/categórica que a una continua,
- la presencia de valores faltantes es variable entre columnas, con impacto directo en la interpretación estadística,
- el tipo de ritmo inicial y otras variables clínicas aparecen como factores de interés para la comparación entre grupos.

Estas observaciones son descriptivas y deben interpretarse como hallazgos preliminares del análisis exploratorio, no como evidencia final diagnóstica o predictiva.

## Análisis de encabezados EEG

Los archivos `.hea` son encabezados de texto que describen la estructura básica de una señal fisiológica sin requerir cargar toda la señal en memoria. En el contexto de los registros EEG, el notebook los utiliza para extraer metadatos esenciales como:

- frecuencia de muestreo,
- número de canales,
- número de muestras,
- duración estimada del registro,
- nombres de canales.

La duración de un registro puede aproximarse con la relación:

$$
T = \frac{N}{f_s}
$$

donde:

- $T$ es la duración del registro,
- $N$ es el número total de muestras,
- $f_s$ es la frecuencia de muestreo.

Este tipo de análisis permite caracterizar registros EEG antes de proceder a un tratamiento más intensivo de la señal, y resulta útil para seleccionar muestras representativas o detectar inconsistencias de formato o de temporalidad.

## Gestión de datos

La gestión de datos es un punto crítico en este proyecto, dado el volumen de la información fisiológica. El repositorio separa explícitamente los artefactos en:

- `data/raw`: datos originales no versionados,
- `data/interim`: artefactos intermedios,
- `data/processed`: datos transformados o ya listos para análisis,
- `results/figures`: figuras generadas,
- `results/tables`: tablas y resúmenes exportados.

La documentación del proyecto indica que la rama fisiológica puede ser de gran tamaño y que la base completa de señales incluye varios terabytes de material. Por esta razón, los datos brutos no se mantienen normalmente en GitHub como parte del control de cambios. El repositorio actual incluye una política explícita de exclusión a través del archivo `.gitignore`, con el fin de evitar subir archivos pesados de señal y derivados no deseados.

Esto representa una práctica adecuada para ciencia de datos reproducible y para análisis clínicos basados en señales, donde la integridad del dato original y el tamaño del conjunto hacen inviable el almacenamiento directo en un repositorio de código.

## Instalación

Se recomienda usar un entorno virtual aislado para reproducir el proyecto y evitar conflictos con dependencias del sistema.

### Opción 1: instalación automática según el sistema operativo

El repositorio incluye dos scripts para crear el entorno virtual, detectar el sistema operativo, instalar las dependencias de `requirements.txt` y dejarlo activado.

#### macOS / Linux

```bash
git clone git@github-mlda:byepesg/mlda-project.git
cd mlda-project
chmod +x scripts/setup_env.sh
./scripts/setup_env.sh
```

Este script:

- detecta macOS o Linux,
- crea `.venv` si no existe,
- activa el entorno virtual,
- ejecuta `python -m pip install --upgrade pip`,
- instala las dependencias del archivo `requirements.txt`.

#### Windows (PowerShell)

```powershell
git clone git@github-mlda:byepesg/mlda-project.git
cd mlda-project
powershell -ExecutionPolicy Bypass -File .\scripts\setup_env.ps1
```

Este script:

- detecta Windows,
- crea `.venv` si no existe,
- activa el entorno virtual,
- instala `pip` y las dependencias del proyecto.

### Opción 2: instalación manual

```bash
git clone git@github-mlda:byepesg/mlda-project.git
cd mlda-project
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

En Windows PowerShell:

```powershell
git clone git@github-mlda:byepesg/mlda-project.git
cd mlda-project
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Verificación del entorno

Una vez activado, puede comprobarse que el entorno está operativo con:

```bash
python --version
pip list
```

Para iniciar Jupyter, puede ejecutarse:

```bash
jupyter lab
```

## Ejecución

La ejecución del proyecto se realiza principalmente mediante notebooks Jupyter. La secuencia recomendada es la siguiente:

1. `notebooks/01_understanding_business/01_M1U2_fase_1_Entendimiento_del_negocio.ipynb`
2. `notebooks/02_understanding_data/02_understanding_data.ipynb`

La apertura con Jupyter, VS Code o JupyterLab permite explorar y ejecutar de forma reproducible cada fase del análisis. La estructura del proyecto está pensada para mantener la separación entre documentación, datos originales y resultados derivados.

## Dependencias principales

Las dependencias del proyecto están registradas en `requirements.txt`. Entre los paquetes relevantes para este trabajo destacan:

| Librería | Rol principal |
|---|---|
| `pandas` | Manipulación y análisis tabular de datos clínicos. |
| `numpy` | Operaciones numéricas y manejo vectorizado. |
| `matplotlib` | Visualización de distribuciones y diagnósticos exploratorios. |
| `scipy` | Análisis estadístico y cálculos científicos. |
| `scikit-learn` | Potencial análisis y modelado en etapas futuras. |
| `requests` | Descarga de recursos desde PhysioNet y APIs asociadas. |
| `wfdb` | Lectura y manejo del formato WFDB de PhysioNet. |
| `jupyter`, `notebook`, `ipykernel` | Ejecución y ejecución reproducible de notebooks. |
| `nbformat` | Escritura y lectura de notebooks. |

## Reproducibilidad

La reproducibilidad del proyecto depende de varios aspectos:

- uso de un entorno virtual Python,
- instalación explícita de dependencias desde `requirements.txt`,
- organización consistente de carpetas (`raw`, `interim`, `processed`, `results`),
- separación entre datos originales y artefactos derivados,
- documentación de los notebooks y del flujo de análisis,
- uso de principios de trazabilidad para la limpieza y transformación de datos.

La documentación del repositorio y el estado del `.gitignore` indican que los datos brutos de señales no se mantienen en Git por su tamaño y uso asociado a fuentes externas. Esta práctica es recomendable y consistente con la naturaleza del dataset.

## Equipo

En el repositorio no se documenta un equipo formal completo con afiliaciones o roles detallados. La evidencia disponible consiste en una planificación del proyecto y notebooks académicos, pero no se observa un archivo formal de colaboradores ni un perfil institucional completo en la estructura actual del repositorio.

## Referencias

El repositorio se apoya en la documentación del conjunto de datos I-CARE v2.1 y en la plataforma PhysioNet. La referencia más clara documentada en el notebook es la siguiente:

- Amorim, E., Zheng, W., Lee, J. W., Herman, S., Ghassemi, M., Sivaraju, A., Gaspard, N., Hofmeijer, J., van Putten, M. J. A. M., Reyna, M., Clifford, G., & Westover, B. (2023). I-CARE: International Cardiac Arrest REsearch consortium Database (version 2.1). PhysioNet. https://doi.org/10.13026/m33r-bj81

Además, la documentación del proyecto hace referencia a:

- PhysioNet como fuente principal de datos.
- CRISP-DM como marco metodológico para la planificación del estudio.
- I-CARE como base de datos multicéntrica y multimodal de pacientes en coma tras paro cardíaco.

## Licencia y uso de datos

El repositorio no incluye un archivo `LICENSE` explícito en la estructura actual. Por lo tanto, no se puede afirmar que el código de este proyecto esté distribuido bajo una licencia específica como MIT, Apache o GPL sin documentación adicional.

En cambio, la base de datos I-CARE v2.1 es referenciada como un recurso de PhysioNet. El notebook documenta que la base se distribuye bajo una licencia CC BY-NC-SA 4.0. Por tanto, el uso de los datos de I-CARE debe respetar los términos de la fuente original, mientras que la licencia del repositorio debe mantenerse separada de la licencia del dataset.

---

Este README refleja el estado actual del proyecto: una investigación académica en fase de entendimiento del negocio y del dato, con foco en la caracterización clínica y fisiológica del conjunto I-CARE v2.1, sin afirmar resultados predictivos finales ni una validación clínica concluyente.
