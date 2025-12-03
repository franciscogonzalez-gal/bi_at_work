# BI at Work - Análisis de Datos de Netflix

## Descripción

Proyecto de Business Intelligence desarrollado como parte de la **Maestría en Business Intelligence & Analytics** de la **Universidad Galileo**. Este proyecto implementa un proceso ETL (Extract, Transform, Load) completo para analizar el catálogo de películas y series de Netflix.

## Estructura del Proyecto

```
├── proyecto_library.py          # Biblioteca con funciones ETL
├── ETL Proyecto.ipynb           # Notebook principal del proceso ETL
├── EDA.ipynb                    # Notebook de Análisis Exploratorio de Datos
├── EDA_peliculas_netflix.html   # Reporte HTML del análisis exploratorio
├── db_scripts.sql               # Scripts SQL para configurar el esquema estrella
├── LICENSE.txt                  # Licencia CC0 1.0 Universal
└── README.md                    # Este archivo
```

## Funcionalidades

### Biblioteca ETL (`proyecto_library.py`)

- **`read_file(file_path)`**: Lee un archivo CSV y realiza transformaciones necesarias:
  - Conversión de fechas
  - División de columnas (duration, listed_in, cast, country)
  - Manejo de valores nulos

- **`create_star_schema(df)`**: Crea un esquema estrella con las siguientes tablas:
  - `fact_table`: Tabla de hechos
  - `title_dim`: Dimensión de títulos
  - `people_dim`: Dimensión de personas (directores y elenco)
  - `country_dim`: Dimensión de países
  - `date_dim`: Dimensión de fechas
  - `type_dim`: Dimensión de tipo/rating

- **`initialize_db(username, password, host, port, database_name)`**: Inicializa la conexión a PostgreSQL

- **`load_data_to_table(engine, table_name, data, if_exists)`**: Carga datos a tablas de la base de datos

- **`dispose_engine(engine)`**: Cierra las conexiones a la base de datos

## Requisitos

### Dependencias de Python

- pandas
- sqlalchemy
- numpy
- ydata_profiling (para EDA)

### Base de Datos

- PostgreSQL

### Datos

El proyecto utiliza el dataset `netflix_titles.csv` que contiene información del catálogo de Netflix.

## Uso

### 1. Análisis Exploratorio de Datos (EDA)

Ejecutar el notebook `EDA.ipynb` para generar un reporte de análisis exploratorio:

```python
from proyecto_library import read_file
from ydata_profiling import ProfileReport

# Leer el archivo
peliculas_netflix = read_file('netflix_titles.csv')

# Generar el reporte
profile_peliculas = ProfileReport(peliculas_netflix, title='Peliculas Netflix', explorative=True)

# Guardar el reporte
profile_peliculas.to_file('EDA_peliculas_netflix.html')
```

### 2. Proceso ETL

Ejecutar el notebook `ETL Proyecto.ipynb` para realizar el proceso completo:

```python
from proyecto_library import read_file, create_star_schema, initialize_db, dispose_engine, load_data_to_table

# Extracción
data = read_file("netflix_titles.csv")

# Transformación
star_schema_dict = create_star_schema(data)

# Carga
engine = initialize_db(username, password, host, port, database_name)
try:
    for tabla in star_schema_dict.keys():
        load_data_to_table(engine, tabla, star_schema_dict[tabla])
finally:
    dispose_engine(engine)
```

### 3. Configuración de Base de Datos

Ejecutar los scripts en `db_scripts.sql` para establecer las llaves primarias y foráneas del esquema estrella.

## Esquema Estrella

El modelo de datos implementa un esquema estrella con:

- **Tabla de Hechos**: Contiene métricas y llaves foráneas hacia las dimensiones
- **Dimensiones**:
  - Títulos (título, género)
  - Personas (director, elenco)
  - País
  - Fecha de agregación
  - Tipo (rating, tipo de contenido, duración)

## Licencia

Este proyecto está licenciado bajo **CC0 1.0 Universal** - ver el archivo [LICENSE.txt](LICENSE.txt) para más detalles.
