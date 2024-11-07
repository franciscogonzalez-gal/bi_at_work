import pandas as pd
from sqlalchemy import create_engine
import numpy as np
from sqlalchemy.ext.declarative import declarative_base
def read_file(file_path):
    """
    Lee un archivo CSV y realiza las transformaciones necesarias para el proyecto.

    :param file_path:
    :return data:
    """
    data = pd.read_csv(file_path, encoding='iso-8859-1', usecols=range(11))

    # Convertir 'date_added' a datetime
    data['date_added'] = pd.to_datetime(data['date_added'], errors='coerce')

      # Modificar los valores que coinciden con '2024-04-05'
    data.loc[data['date_added'] == pd.Timestamp('2024-04-05'), 'date_added'] = pd.Timestamp('2014-04-05')

    # dividir la columna 'duration' en 'duration_qty' y 'duration_type'
    data['duration_qty'] = data ['duration'].str.split(' ', expand=True)[0]
    data['duration_qty'] = pd.to_numeric(data['duration_qty'])
    data['duration_type'] = data ['duration'].str.split(' ', expand=True)[1]
    data['duration_type'] = data['duration_type'].str.replace('Seasons','Season')

    # dividir la columna 'listed_in' por coma y expandir en filas separadas
    data['listed_in'] = data['listed_in'].str.split(', ')
    data = data.explode('listed_in').reset_index(drop=True)

    # dividir la columna 'cast' por coma y expandir en filas separadas
    data['cast'] = data['cast'].str.split(', ')
    data = data.explode('cast').reset_index(drop=True)

    # dividir la columna 'country' por coma y expandir en filas separadas
    data['country'] = data['country'].str.split(', ')
    data = data.explode('country').reset_index(drop=True)

    #reemplzazar nulos por "NR" en la columna 'rating'
    data['rating'] = data['rating'].fillna('NR')

    return data

def create_star_schema(df):
    """
    Crea un esquema estrella a partir de un DataFrame de pandas.

    :param df:
    :return star_schema:
    """
    # Crear las tablas de dimensiones con claves únicas
    # Dimensión de título
    title_dim = df[['title', 'listed_in']].drop_duplicates().copy()
    title_dim['title_id'] = range(1, len(title_dim) + 1)

    # Dimensión de personas (directores y elenco)
    people_dim = df[['director', 'cast']].drop_duplicates().copy()
    people_dim['people_id'] = range(1, len(people_dim) + 1)

    # Dimensión de país
    country_dim = df[['country']].drop_duplicates().copy()
    country_dim['country_id'] = range(1, len(country_dim) + 1)

    # Dimensión de rating
    type_dim = df[['rating','type','duration_type']].drop_duplicates().copy()
    type_dim['type_id'] = range(1, len(type_dim) + 1)

    # Dimensión de fecha
    date_dim = df[['date_added']].drop_duplicates().copy()
    date_dim['date_id'] = range(1, len(date_dim) + 1)

    # Crear la tabla de hechos con claves sustitutas (foreign keys)
    fact_table = df[['show_id', 'type', 'release_year', 'rating', 'duration_qty', 'duration_type', 'title', 'director', 'cast', 'country', 'date_added']].copy()

    # Unir la tabla de hechos con las dimensiones para incluir las claves sustitutas
    fact_table = fact_table.merge(title_dim[['title', 'title_id']], on='title', how='left')
    fact_table = fact_table.merge(people_dim[['director', 'cast', 'people_id']], on=['director', 'cast'], how='left')
    fact_table = fact_table.merge(country_dim[['country', 'country_id']], on='country', how='left')
    fact_table = fact_table.merge(date_dim[['date_added', 'date_id']], on='date_added', how='left')
    fact_table = fact_table.merge(type_dim[['rating','type','duration_type', 'type_id']], on=['rating','type','duration_type'], how='left')

    # Dejar solo las claves sustitutas y las columnas necesarias
    fact_table = fact_table[['show_id',  'release_year', 'duration_qty',
                             'title_id', 'people_id', 'country_id', 'date_id', 'type_id']]

    # Retornar el diccionario de DataFrames
    star_schema = {
        'fact_table': fact_table,
        'title_dim': title_dim[['title_id', 'title', 'listed_in']],
        'people_dim': people_dim[['people_id', 'director', 'cast']],
        'country_dim': country_dim[['country_id', 'country']],
        'date_dim': date_dim[['date_id', 'date_added']],
        'type_dim': type_dim[['type_id', 'rating','type','duration_type']]
    }

    return star_schema

def initialize_db(username: str, password: str, host: str, port: str, database_name: str):
    """
    Inicializa la base de datos PostgreSQL creando el motor y las tablas.
    Devuelve el motor y la fábrica de sesiones.

    Argumentos:
    - username: Nombre de usuario de la base de datos
    - password: Contraseña del usuario de la base de datos
    - host: Dirección del servidor de la base de datos
    - port: Puerto en el que la base de datos está corriendo
    - database_name: Nombre de la base de datos

    Retorna:
    - engine: Motor de conexión a la base de datos
    - SessionLocal: Fábrica de sesiones para interactuar con la base de datos
    """

    # Crear la URL de conexión
    database_url = f"postgresql://{username}:{password}@{host}:{port}/{database_name}"

    # Crear el motor de conexión a la base de datos con SQLAlchemy
    engine = create_engine(database_url)

    return engine

def load_data_to_table(engine, table_name: str, data: pd.DataFrame, if_exists: str = 'replace'):
    """
   Carga un DataFrame de pandas a una tabla en la base de datos usando el motor de SQLAlchemy.

   Args:
   - engine: El motor de conexión a la base de datos.
   - table_name: El nombre de la tabla en la base de datos donde se insertarán los datos.
   - data: Un DataFrame de pandas que contiene los datos a insertar.
   - if_exists: Qué hacer si la tabla ya existe:
       * 'fail': Lanzará un error si la tabla ya existe.
       * 'replace': Borrará la tabla si existe y creará una nueva.
       * 'append': Añadirá los datos a la tabla existente. (valor por defecto)

   Returns:
   - None
   """
    try:
        # Utiliza el método `to_sql` de pandas para escribir el DataFrame en la base de datos
        data.to_sql(name=table_name, con=engine, if_exists=if_exists, index=False)
        print(f"Datos cargados exitosamente en la tabla {table_name}.")
    except Exception as e:
        print(f"Error al cargar los datos en la tabla {table_name}: {e}")


def dispose_engine(engine):
    """
    Cierra el motor de SQLAlchemy liberando todos los recursos y conexiones.

    Args:
    - engine: El motor SQLAlchemy que se desea cerrar.

    Returns:
    - None
    """
    try:
        engine.dispose()
        print("Motor cerrado correctamente.")
    except Exception as e:
        print(f"Error al cerrar el motor: {e}")
