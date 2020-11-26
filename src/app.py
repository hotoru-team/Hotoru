import os, time, threading
import db.DBController as db
from flask import Flask, render_template, request
from dotenv import load_dotenv
from model.SIATA import SIATA
from model.Procesador import save, ajustar_tiempo
from datetime import datetime, timedelta

load_dotenv(dotenv_path='..', verbose=True)
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

sources = [
    SIATA()
]

def llenarDatosVacios():
    threading.Timer(3600, getNewData).start()

    fecha_final = datetime()
    fecha_inicial = fecha_final - timedelta(hours=1)
    estaciones = db.get_estaciones_by_date(fecha_inicial, fecha_final)

    for estacion in estaciones:
        nuevas_mediciones = []
        mediciones_len = len(estacion["mediciones"])
        for i, medicion in enumerate(estacion["mediciones"]):
            next_medicion = estacion["mediciones"][i+1] if i < mediciones_len-1 else None
            
            if(next_medicion != None):
                delta_tiempo = (next_medicion["fecha_hora"] - medicion["fecha_hora"]).total_seconds()/60.0
                num_datos_faltantes = delta_tiempo/4 -1
                if(num_datos_faltantes>=1):
                    aux_date = medicion["fecha_hora"]
                    for i in range(num_datos_faltantes):
                        aux_date += timedelta(minutes=4)
                        # el peso del dato siguiente está dado por la distancia temporal
                        # entre la medición que se quiere calcular y la medición anterior
                        # dividido entre la distancia temporal entre la medición anterior
                        # y la siguiente que al simplificar queda como el índice de la
                        # medición que se está calculando más uno y eso dividido entre
                        # la cantidad de elementos faltantes más 1
                        peso_next = (i+1)/(num_datos_faltantes+1)
                        peso_prev = 1 - peso_prev
                        PM2_5 = (medicion["PM2_5"]*peso_prev + next_medicion["PM2_5"]*peso_next)/2
                        nueva_medicion = {
                            "PM2_5": PM2_5,
                            "fecha_hora": aux_date
                        }
                        nuevas_mediciones.append(nueva_medicion)
        for medicion in nuevas_mediciones:
            db.insertar_medicion(estacion["codigo"], medicion)
                    

def getNewData():
    """
    Obtiene una lista de variables desde un servidor remoto, revisa los datos y los guarda en la base de datos
    """
    print("Getting new data from sources")
    for source in sources:
        estaciones = source.getData()
        print("Insertando nuevos datos")
        for estacion in estaciones:
            e = save(estacion, db)
            if(e != None):
                medicion = e["mediciones"][0]
                medicion["fecha_hora"] = ajustar_tiempo(medicion["fecha_hora"])
                db.crear_estacion(estacion)
                db.insertar_medicion(estacion["codigo"],medicion) 
    print("Datos Incertados")
    print("─────────────────────────────")
            
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

@app.route('/estacion/<int:codigo>',methods=['GET'])
def estacion(codigo):


    if(request.args.get('start-date') is None or request.args.get('end-date') is None):
        fecha_final = datetime.today()
        fecha_inicial = fecha_final - timedelta(days=1)
    else:
        fecha_inicial = datetime.strptime(request.args.get('start-date'), "%Y-%m-%d")
        fecha_final = datetime.strptime(request.args.get('end-date'), "%Y-%m-%d")
        if(fecha_inicial == fecha_final):
            fecha_final += timedelta(days=1)

    estacion = db.get_estacion_by_date(codigo, fecha_inicial, fecha_final)
    fechas = []
    mediciones = []
    nombre = ''

    nombre = estacion["barrio"]
    for i in range(len(estacion["mediciones"])):
        #tomar solo la fecha : medicion[i]["fecha_hora"].split('T')[0]
        if(fecha_inicial <= estacion["mediciones"][i]["fecha_hora"] and fecha_final >= estacion["mediciones"][i]["fecha_hora"]):
            fechas.append(datetime.strftime(estacion["mediciones"][i]["fecha_hora"], "%d-%m-%Y %I:%M:%S %p"))
            mediciones.append(round(estacion["mediciones"][i]["PM2_5"], 3))



    # valoresY = mediciones
    # valoresX = fechas
    #print(valoresY)
    #print(valoresX)

    return render_template('estacion.html',nombre=nombre,mediciones=mediciones,fechas=fechas,fecha_final=fecha_final,fecha_inicial=fecha_inicial)



@app.route('/<int:codigo>')
def render(codigo):
    return render_template('estacion.html', estacion=db.get_estacion(codigo))

if __name__ == '__main__':
    threading.Timer(0, getNewData).start()
    threading.Timer(0, llenarDatosVacios).start()
    app.run()
