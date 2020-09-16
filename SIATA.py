import requests
import numpy as np 
import pandas as pd

url_promedio = 'http://siata.gov.co:3000/cc_api/estaciones/listar/'
url_minutal = 'http://siata.gov.co:3000/cc_api/estaciones/listar_minutal/'

def getData():
    
    try:
        response = requests.get(url_minutal)
        data = pd.read_json(response.content)
        print(type(data.head()))
        data_online = data[data["online"] == "Y"]
        data_online = data[data['PM2_5_last'] >= 0]
        data_online = data[data['humedad_relativa'] >= 0]
        data_online = data[data['temperatura'] >= 0]
        print(type(data_online.head()))
        print(data_online.head())
    except:    
        print("problems...")


if  __name__ == '__main__':
    getData()

