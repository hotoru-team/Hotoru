from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='../..', verbose=True)

conn = MongoClient("mongodb://{}:{}@{}:27017/".format(os.getenv("MONGO_USER"),os.getenv("MONGO_PASSWORD"),os.getenv("MONGO_HOST")))
db = conn["hotaru"]
estaciones = db["estaciones"]

def get_estaciones():
    """
    Retorna una lista de estaciones con sus respectivas mediciones
    """
    return estaciones.find()

def get_estacion(codigo_estacion):
    """
    Retorna la estación que tenga el código `codigo_estacion`
    """
    return estaciones.find_one({'codigo':codigo_estacion})

def crear_estaciones(Estaciones=[]):
    """
    Se inserta una lista de estaciones en la base de datos si no existían previamente.
    
    Las estaciones deben tener el siguiente formato:
    ```javascript
    {
        "latitude": number,
        "longitude": number,
        "online": bool,
        "altitud": number,
        "barrio": String,
        "vereda": String,
        "ciudad": String,
        "estado": String,
        "codigo": 1
        "mediciones": []
    }
    ```
    """
    for estacion in Estaciones:
        del estacion.mediciones[0]
        if(estaciones.find_one({"codigo":estacion.codigo}) == None):
            estaciones.insert_one(estacion)

def insertar_medicion(codigo_estacion, medicion):
    """
    Inserta una medición en una estación dada.
    El formato de la medición debe ser el siguiente:
    ```javascript
    {
        "PM2_5": number,
        "fecha_hora": Date,
    }
    ```
    """
    if (estaciones.find_one({'codigo':codigo_estacion}) != None):
        estaciones.update_one({'codigo':codigo_estacion},{
                '$push':{'mediciones': medicion}
            })

def actualizar_estacion(codigo_estacion, estacion):
    """
    Actualiza la estación que tenga el código `codigo_estacion`
    """
    estaciones.update_one({'codigo':codigo_estacion}, estacion)