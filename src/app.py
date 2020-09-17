import os
import db.DBController as db
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv(dotenv_path='..', verbose=True)
app = Flask(__name__)


# Este es el ejemplo de como deben estar las estaciones al momento de guardarlas en la base de datos
# hay que hacer una función que las traiga desde el SIATA y las guarde con la función db.crear_estacion() que guarda de a una
# la función que trae los datos desde el siata debe tener alguna especie de contador que la active cada cierto tiempo 
ESTACIONES = [
    {
        "latitude": 6.2550666,
        "longitude": -75.61927170000001,
        "online": "Y",
        "altitud": 1584,
        "barrio": "San Javier No.1",
        "vereda": "Zona Urbana",
        "ciudad": "Medellin",
        "estado": "A",
        "codigo": 1,
        "mediciones":[
            {
                "PM2_5": 25.6546893539, # este es el last
                "fecha_hora": "2020-09-16T21:59:00",
            },
            {
                "PM2_5":54.47731990069195,
                "fecha_hora": "2020-09-16T21:59:00",
            }
        ]
    },
    {
        "latitude": 6.2550666,
        "longitude": -75.61927170000001,
        "online": "Y",
        "altitud": 1584,
        "barrio": "ITM",
        "vereda": "Zona Urbana",
        "ciudad": "Medellin",
        "estado": "A",
        "codigo": 4,
        "mediciones":[
            {
                "PM2_5": 25.6546893539, # este es el last
                "fecha_hora": "2020-09-16T21:59:00",
            },
            {
                "PM2_5":54.47731990069195,
                "fecha_hora": "2020-09-16T21:59:00",
            }
        ]
    },
    {
        "latitude": 6.2550666,
        "longitude": -75.61927170000001,
        "online": "Y",
        "altitud": 1584,
        "barrio": "San Javier No.1",
        "vereda": "Zona Urbana",
        "ciudad": "Itagui",
        "estado": "A",
        "codigo": 2,
        "mediciones":[
            {
                "PM2_5": 25.6546893539, # este es el last
                "fecha_hora": "2020-09-16T21:59:00",
            },
            {
                "PM2_5":54.47731990069195,
                "fecha_hora": "2020-09-16T21:59:00",
            }
        ]
    },
    {
        "latitude": 6.2550666,
        "longitude": -75.61927170000001,
        "online": "Y",
        "altitud": 1584,
        "barrio": "San Javier No.1",
        "vereda": "Zona Urbana",
        "ciudad": "Sabaneta",
        "estado": "A",
        "codigo": 3,
        "mediciones":[
            {
                "PM2_5": 25.6546893539, # este es el last
                "fecha_hora": "2020-09-16T21:59:00",
            },
            {
                "PM2_5":54.47731990069195,
                "fecha_hora": "2020-09-16T21:59:00",
            }
        ]
    }
]

@app.route('/template')
def template():
    return render_template('template.html');

@app.route('/')
def hello():
    estaciones = ESTACIONES # Esto se debe reemplazar por la función que trae datos desde la base de datos
    ciudades = []
    for estacion in estaciones:
        if estacion["ciudad"] not in ciudades:
            ciudades.append(estacion["ciudad"])

    return render_template('estaciones.html', estaciones=estaciones, zonas=ciudades)

@app.route('/<int:codigo>')
def render(codigo):
    return render_template('estacion.html', estacion=db.get_estacion(codigo))

if __name__ == '__main__':
    app.run()