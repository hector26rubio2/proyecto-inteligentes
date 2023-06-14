# Proyecto Sistemas Inteligentes
# Procesamiento de datos

Esta API proporciona endpoints para el procesamiento y análisis de conjuntos de datos. A continuación se describen los diferentes endpoints disponibles.

## Endpoints

### 1. `/loadFile` (POST)
- Descripción: Permite cargar un archivo de datos en formato `.xlsx` o `.csv`.
- Parámetros:
  - `file` (tipo: UploadFile) - El archivo a cargar.
- Respuesta exitosa:
  - Código de estado: 200 OK
  - Modelo de respuesta: `NameDatase`
- Posibles errores:
  - Código de estado: 400 Bad Request - Se espera un archivo con extensión `.xlsx` o `.csv`.
  - Código de estado: 500 Internal Server Error - Error interno del servidor.

### 2. `/descriptFile/{dataset}` (GET)
- Descripción: Obtiene la descripción de un conjunto de datos.
- Parámetros:
  - `dataset` (tipo: str) - El nombre o identificador del conjunto de datos.
- Respuesta exitosa:
  - Código de estado: 200 OK
  - Modelo de respuesta: `dict`
- Posibles errores:
  - Código de estado: 404 Not Found - Conjunto de datos no encontrado.
  - Código de estado: 500 Internal Server Error - Error interno del servidor.

### 3. `/datasets` (GET)
- Descripción: Obtiene la lista de conjuntos de datos disponibles.
- Respuesta exitosa:
  - Código de estado: 200 OK
  - Modelo de respuesta: `List[str]`
- Posibles errores:
  - Código de estado: 500 Internal Server Error - Error interno del servidor.

### 4. `/dataTreatment/{dataset}` (GET)
- Descripción: Realiza el tratamiento de datos para un conjunto de datos específico.
- Parámetros:
  - `dataset` (tipo: str) - El nombre o identificador del conjunto de datos.
- Respuesta exitosa:
  - Código de estado: 200 OK
  - Modelo de respuesta: `NameDatase`
- Posibles errores:
  - Código de estado: 404 Not Found - Conjunto de datos no encontrado.
  - Código de estado: 500 Internal Server Error - Error interno del servidor.

### 5. `/graphical/{dataset}` (GET)
- Descripción: Realiza un análisis gráfico y estadístico de un conjunto de datos.
- Parámetros:
  - `dataset` (tipo: str) - El nombre o identificador del conjunto de datos.
- Respuesta exitosa:
  - Código de estado: 200 OK
  - Modelo de respuesta: `GraphicalAnalysis`
- Posibles errores:
  - Código de estado: 404 Not Found - Conjunto de datos no encontrado.
  - Código de estado: 500 Internal Server Error - Error interno del servidor.

### 6. `/listModel` (GET)
- Descripción: Obtiene una lista de modelos disponibles.
- Respuesta exitosa:
  - Código de estado: 200 OK
  - Modelo de respuesta: `dict`
- Posibles errores:
  - Código de estado: 500 Internal Server Error - Error interno del servidor.

### 7. `/top3Models` (GET)
- Descripción: Obtiene los tres mejores modelos basados en las métricas de precisión, recall y F1-score.
- Respuesta exitosa:
  - Código de estado: 200 OK
  - Modelo de respuesta: `List[ModelTRES]`
- Posibles errores:
  - Código de estado: 500 Internal Server Error - Error interno del servidor.

### 8. `/trainingModel` (POST)
- Descripción: Entrena un modelo utilizando los datos proporcionados.
- Parámetros:
  - `trainingModel` (tipo: TrainingModelDTO) - Los datos y la configuración del modelo de entrenamiento.
- Respuesta exitosa:
  - Código de estado: 200 OK
  - Modelo de respuesta: `Union[ModelTRES, Error]`
- Posibles errores:
  - Código de estado: 500 Internal Server Error - Error interno del servidor.

## Requisitos

A continuación se enumeran los paquetes y sus respectivas versiones requeridos para ejecutar esta API:

- anyio==3.7.0
- click==8.1.3
- colorama==0.4.6
- contourpy==1.0.7
- cycler==0.11.0
- dnspython==2.3.0
- exceptiongroup==1.1.1
- fastapi==0.97.0
- fonttools==4.40.0
- h11==0.14.0
- idna==3.4
- importlib-resources==5.12.0
- joblib==1.2.0
- kiwisolver==1.4.4
- matplotlib==3.7.1
- numpy==1.24.3
- packaging==23.1
- pandas==2.0.2
- Pillow==9.5.0
- pydantic==1.10.9
- pymongo==4.3.3
- pyparsing==3.0.9
- python-dateutil==2.8.2
- python-dotenv==1.0.0
- python-multipart==0.0.6
- pytz==2023.3
- scikit-learn==1.2.2
- scipy==1.10.1
- seaborn==0.12.2
- setuptools==57.4.0
- six==1.16.0
- sklearn==0.0.post5
- sniffio==1.3.0
- starlette==0.27.0
- threadpoolctl==3.1.0
- typing_extensions==4.6.3
- tzdata==2023.3
- uvicorn==0.22.0
- zipp==3.15.0