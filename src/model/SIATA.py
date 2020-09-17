#dt = data
#dto = data_online
import requests
import numpy as np 
import pandas as pd
from IFuenteDeDatos import IFuenteDeDatos


class SIATA(IFuenteDeDatos):

    url_minutal = 'siata.gov.co:3000/cc_api/estaciones/listar_minutal/'
    def __init__(self):
        pass
    def getData(self):
        try:
            result = []
            response = requests.get(self.url_minutal)
            data = pd.read_json(response.content)
            for item in data:
                result.append({
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
                        "fecha_hora": item["fecha_hora"]
                    }]
                })
            return result
        except:
            raise Exception("Error getting data from SIATA:\n")

