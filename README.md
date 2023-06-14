# Proyecto Sistemas Inteligentes
# Procesamiento de datos

Esta API proporciona endpoints para el procesamiento y análisis de conjuntos de datos. A continuación se describen los diferentes endpoints disponibles.

## Endpoints

## Endpoints Disponibles

1. **Cargar Archivo** (`/loadFile` - POST): Permite cargar un archivo de datos en formato `.xlsx` o `.csv`.

2. **Describir Archivo** (`/descriptFile/{dataset}` - GET): Obtiene la descripción de un conjunto de datos específico.

3. **Listar Conjuntos de Datos** (`/datasets` - GET): Obtiene la lista de conjuntos de datos disponibles.

4. **Tratamiento de Datos** (`/dataTreatment/{dataset}` - GET): Realiza el tratamiento de datos para un conjunto de datos específico.

5. **Análisis Gráfico y Estadístico** (`/graphical/{dataset}` - GET): Realiza un análisis gráfico y estadístico de un conjunto de datos.

6. **Listar Modelos** (`/listModel` - GET): Obtiene una lista de modelos disponibles.

7. **Top 3 Modelos** (`/top3Models` - GET): Obtiene los tres mejores modelos basados en métricas de precisión, recall y F1-score.

8. **Entrenar Modelo** (`/trainingModel` - POST): Entrena un modelo utilizando los datos proporcionados.


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