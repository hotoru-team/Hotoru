#dt = data
#dto = data_online
import requests
import numpy as np 
import pandas as pd
from IFuenteDeDatos import IFuenteDeDatos


class SIATA(IFuenteDeDatos):

    url_minutal = 'http://siata.gov.co:3000/cc_api/estaciones/listar_minutal/'
    def getData(self):       
        try:
            response = requests.get(self.url_minutal)  
            dt = pd.read_json(response.content)
            print(type(dt.head()))
            dto = dt[dt["online"] == "Y"]
            dto = dt[dt['PM2_5_last'] >= 0]
            dto = dt[dt['humedad_relativa'] >= 0]
            dto = dt[dt['temperatura'] >= 0]
            print(type(dto.head()))
            dto = pd.get_dummies(dto, columns = ["estado"]) #convierte los valores de la columna de estado a 1 y 0
            t_naive =  pd.to_datetime(dto['fecha_hora'], format='%Y-%m-%dT%H:%M:%S')
            dto['fecha_hora'] = [t.tz_localize(tz='Etc/GMT+5') for t in t_naive]
            dto = dto[dto['fecha_hora'] >= (max(dto['fecha_hora']) - pd.Timedelta('00:15:00'))] # Filtrar datos que se alejen más de 30 min de la lectura más reciente.
            print(dto.head())
        except:    
            print("problems...")

