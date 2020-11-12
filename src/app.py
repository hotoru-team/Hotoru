import os, time, threading
import db.DBController as db
from flask import Flask, render_template, request
from dotenv import load_dotenv
from model.SIATA import SIATA


load_dotenv(dotenv_path='..', verbose=True)
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

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
        estacion["codigo"] = str(estacion["codigo"])
    #print(estaciones)
   
    return render_template('estaciones.html', estaciones=estaciones, zonas=ciudades)

@app.route('/graficas/<int:codigo>',methods=['GET'])
def graficas(codigo):

    fecha_inicial = request.args.get('trip-start')
    fecha_final = request.args.get('trip-end')
        
    db_estaciones = db.get_estaciones()
    fechas = []
    mediciones = []
    nombre = ''
    for estacion in db_estaciones:
        if estacion["codigo"] == codigo:
            nombre = estacion["barrio"]
            medicion = estacion["mediciones"]
            for i in range(len(medicion)):
                #tomar solo la fecha : medicion[i]["fecha_hora"].split('T')[0]
                if(fecha_inicial == medicion[i]["fecha_hora"].split('T')[0]):
                    fechas.append(medicion[i]["fecha_hora"])
                    mediciones.append(medicion[i]["PM2_5"])



    valoresY = mediciones
    valoresX = fechas
    #print(valoresY)
    #print(valoresX)
    return render_template('graficas.html',nombre=nombre,mediciones=mediciones,fechas=fechas,fecha_final=fecha_final,fecha_inicial=fecha_inicial)



@app.route('/<int:codigo>')
def render(codigo):
    return render_template('estacion.html', estacion=db.get_estacion(codigo))

if __name__ == '__main__':
    threading.Timer(0, getNewData).start()
    app.run()
