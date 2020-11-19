from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

db_uri="mongodb://{}:{}@{}:27017/".format(os.getenv("MONGO_USER"),os.getenv("MONGO_PASSWORD"),os.getenv("MONGO_HOST"))
conn = MongoClient(db_uri)
db = conn["hotoru"]
estaciones = db["estaciones"]

def dataOneYear(codigo_estacion):
    estacion = get_estacion(codigo_estacion)
    dt = datetime.now()
    fecha_ini_year = dt.replace(year=dt.year-2)
    fecha_fin_year = dt.replace(year=dt.year-1)
    fecha_inicial = dt.replace(year=dt.year-2)
    fecha_final = fecha_inicial + timedelta(days=7 )
    Insert = []
    while (fecha_inicial.year<dt.year-1):
        semana = []
        # Se van a tomar todos los datos de una semana
        estacion = db.get_estacion_by_date(codigo_estacion, fecha_inicial, fecha_final)
        for i in range(len(estacion["mediciones"])):
            if(fecha_inicial <= estacion["mediciones"][i]["fecha_hora"] and fecha_final >= estacion["mediciones"][i]["fecha_hora"]):
                semana.append(i["PM2_5"]))   
        # Se saca promedio de los datos de esa semana
        DateSemana = mean(semana)
        DataSemana.append([{
        'PM2_5': DateSemana,
        'fecha_hora': fecha_inicial,}])     
        fecha_inicial = fecha_final
        fecha_final = fecha_inicial + timedelta(days=7 )
    
    delete_mediciones_by_date(codigo_estacion, fecha_ini_year, fecha_fin_year)
    for j in range(len(DataSemana)):
       insertar_medicion(codigo_estacion, DataSemana[j])

def array_codigos_estaciones ():
    return estaciones.distinct('codigo')


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

def get_estacion_by_date(codigo_estacion, fecha_inicial, fecha_final):
    return estaciones.find_one({
        'codigo':codigo_estacion,
        'mediciones':{
            '$elemMatch':{
                'fecha_hora':{
                    '$gte': fecha_inicial,
                    '$lte': fecha_final
                }
            }
        }
    })

def delete_mediciones_by_date(codigo_estacion, fecha_inicial, fecha_final):
    estaciones.update_one({'codigo':codigo_estacion},
    {
        '$pull':{
            'mediciones':{
                'fecha_hora':{
                    '$gte': fecha_inicial,
                    '$lte': fecha_final
                }
            }
        }
    })

def crear_estacion(estacion):
    """
    Se inserta una estacion en la base de datos si no existía previamente.
    
    La estacion debe tener el siguiente formato:
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
    estacion["mediciones"]=[]
    if(estaciones.find_one({"codigo":estacion["codigo"]}) == None):
        estaciones.insert_one(estacion)

def insertar_medicion(codigo_estacion, medicion):
    """
    Inserta una nueva medición en una estación dada.
    El formato de la medición debe ser el siguiente:
    ```javascript
    {
        "PM2_5": number,
        "fecha_hora": Date,
    }
    ```
    """
    estacion = estaciones.find_one({'codigo':codigo_estacion})
    if (estacion != None):
        for med in estacion["mediciones"]:
            if (med["fecha_hora"] == medicion["fecha_hora"]):
                return
        estaciones.update_one({'codigo':codigo_estacion},{
            '$push':{'mediciones': medicion}
        })

def actualizar_estacion(codigo_estacion, estacion):
    """
    Actualiza la estación que tenga el código `codigo_estacion`
    """
    estaciones.update_one({'codigo':codigo_estacion}, estacion)