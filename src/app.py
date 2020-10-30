import os, time, threading
import db.DBController as db
from flask import Flask, render_template
from dotenv import load_dotenv
from model.SIATA import SIATA
import matplotlib.pyplot as plt

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
        for estacion in estaciones:
            medicion = estacion["mediciones"][0]
            db.crear_estacion(estacion)
            db.insertar_medicion(estacion["codigo"],medicion) 
            
    threading.Timer(60, getNewData).start()

@app.route('/template')
def template():
    return render_template('template.html')

@app.route('/')
def get_estaciones():
    db_estaciones = db.get_estaciones()
    estaciones = []
    ciudades = []
    for estacion in db_estaciones:
        if estacion["ciudad"] not in ciudades:
            ciudades.append(estacion["ciudad"])
        estaciones.append(estacion)
    print(estaciones)
    return render_template('estaciones.html', estaciones=estaciones, zonas=ciudades)

@app.route('/graficas')
def graficas():
    db_estaciones = db.get_estaciones()
    estaciones = []
    ciudades = []
    codigos = []
    mediciones = []
    for estacion in db_estaciones:
        if estacion["ciudad"] not in ciudades:
            ciudades.append(estacion["ciudad"])
        estaciones.append(estacion) 
    for estacion in estaciones:
        codigos.append(estacion["codigo"])
        medicion = estacion["mediciones"]
        mediciones.append(medicion[0])
    
    grafica = plt.stem(codigos,mediciones)
    plt.xlabel('codigo')
    plt.ylabel('pm2.5')
    plt.savefig("Grafica.jpg", bbox_inches='tight')
    return render_template('graficas.html', estaciones=estaciones, zonas=ciudades)

@app.route('/<int:codigo>')
def render(codigo):
    return render_template('estacion.html', estacion=db.get_estacion(codigo))

if __name__ == '__main__':
    #getNewData()
    app.run()