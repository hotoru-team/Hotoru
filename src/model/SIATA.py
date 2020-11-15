#dt = data
#dto = data_online
import requests
import numpy as np 
import pandas as pd
import datetime

import abc

class IFuenteDeDatos(abc.ABC):
    @abc.abstractmethod
    def getData(self):
        """
        Obtiene mediciones desde un servidor
        """
        pass

class SIATA(IFuenteDeDatos):

    url = 'http://siata.gov.co:3000/cc_api/estaciones/listar_minutal/'

    def __init__(self):
        pass
    
    def getData(self):
        try:
            result = []
            data = requests.get(self.url).json()
            for item in data:
                dt = ""
                fecha_hora = item["fecha_hora"]
                if(fecha_hora == None):
                    dt = None
                else:
                    dt = datetime.datetime.strptime(fecha_hora, '%Y-%m-%dT%H:%M:%S')
                estacion = {
                    "latitude": item["latitude"],
                    "longitude": item["longitude"],
                    "online": item["online"] == "Y",
                    "altitud": item["altitud"],
                    "barrio": item["barrio"],
                    "vereda": item["vereda"],
                    "ciudad": item["ciudad"],
                    "estado": item["estado"],
                    "codigo": item["codigo"],
                    "mediciones":[{
                        "PM2_5": item["PM2_5_last"],
                        "fecha_hora": dt
                    }]
                }
                result.append(estacion)
            return result
        except:
            raise Exception("Error getting data from SIATA")

