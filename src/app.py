import os, time, threading
import db.DBController as db
from flask import Flask, render_template
from dotenv import load_dotenv
from model.SIATA import SIATA

load_dotenv(dotenv_path='..', verbose=True)
app = Flask(__name__)

sources = [
    SIATA()
]

def getNewData():
    """
    Obtiene una lista de variables desde un servidor remoto, revisa los datos y los guarda en la base de datos
    """
    print("Getting new data from sources")
    for source in sources:
        estaciones = source.getData()
        db.crear_estaciones(estaciones)
        for estacion in estaciones:
            db.insertar_medicion(estacion.codigo, estacion.mediciones[0])
    threading.Timer(60, getNewData).start()

@app.route('/template')
def template():
    return render_template('template.html')

@app.route('/')
def hello():
    estaciones = db.get_estaciones()
    ciudades = []
    for estacion in estaciones:
        if estacion["ciudad"] not in ciudades:
            ciudades.append(estacion["ciudad"])

    return render_template('estaciones.html', estaciones=estaciones, zonas=ciudades)

@app.route('/<int:codigo>')
def render(codigo):
    return render_template('estacion.html', estacion=db.get_estacion(codigo))

if __name__ == '__main__':
    getNewData()
    app.run()