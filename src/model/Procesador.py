from numpy import mean,std,sqrt,pi,e
from scipy.integrate import quad
from db.DBController import get_estaciones

def G(x):
    """
    Función a integrar para obtener la probabilidad
    """
    return 1/sqrt(2*pi)*e**(-x**2/2)

def prob(t):
    """
    Calculo de la probabilidad usando una integración de G(x) desde -t hasta t
    """
    return quad(G, -t, t)[0]

def n(x, N, t)->float:
    """
    Calcula la probabilidad de que el datos ea un dato atípico.

    Si el resultado es menor a 0.5 (en porcentaje) entonces el
    dato se considera atípico
    """
    return N*(1-prob(t))

def save(input_estacion)->dict:
    """
    Retorna la estación si la medición que contiene es válida
    o retorna un valor nulo si no lo es
    Esto significa que elimina los datos nulos
    y los datos atípicos usando el criterio de chauvenet
    """
    mediciones = []
    if(input_estacion["fecha_hora"]== None):
        return None
    else:
        mediciones.append(input_estacion["mediciones"]["PM2_5"])
    # Se van a tomar todos los datos de las últimas 48 horas
    db_estacion= {
        "_id": '5f6577823a3853a0e0065d99',
        "latitude": 6.2550666,
        "longitude": -75.61927170000001,
        "online": True,
        "altitud": 1584,
        "barrio": 'San Javier No.1',
        "vereda": 'Zona Urbana',
        "ciudad": 'Medellin',
        "estado": 'A',
        "codigo": 2,
        "mediciones": [
            {
                "PM2_5": 40.1095897175,
                "fecha_hora": '2020-09-18T22:09:00'
            },
            {
                "PM2_5": 44.4460598266,
                "fecha_hora": '2020-09-18T22:19:00'
            },
            {
                "PM2_5": 60.3464502265,
                "fecha_hora": '2020-09-18T22:32:00'
            },
            {
                "PM2_5": 54.5644900811,
                "fecha_hora": '2020-09-18T22:45:00'
            },
            {
                "PM2_5": 50.228019972,
                "fecha_hora": '2020-09-18T22:54:00'
            },
            {
                "PM2_5": 54.5644900811,
                "fecha_hora": '2020-09-18T23:09:00'
            },
            {
                "PM2_5": 50.228019972,
                "fecha_hora": '2020-09-25T09:15:00'
            },
            {
                "PM2_5": 43.0005697902,
                "fecha_hora": '2020-09-25T09:25:00'
            },
            {
                "PM2_5": 48.7825299357,
                "fecha_hora": '2020-09-25T09:35:00'
            },
            {
                "PM2_5": 38.6640996811,
                "fecha_hora": '2020-09-25T09:49:00'
            },
            {
                "PM2_5": 28.5456694266,
                "fecha_hora": '2020-09-25T10:59:00'
            },
            {
                "PM2_5": 28.5456694266,
                "fecha_hora": '2020-09-25T11:08:00'
            }
        ]
    }  # Dato simulado. El contenido de esta variable debe obtenerse de la base de datos
    
    for m in enumerate(db_estacion["mediciones"]):
        mediciones.append(m["PM2_5"])
    
    Xm = mean(mediciones)
    
    # El cálculo de la desviación de la siguiente instrucción 
    # es equivalente a la siguiente función:
    # desviacion = sqrt(1/(N-1)*sum((mediciones-Xm)**2))
    # en donde:
    # N = len(mediciones)
    # Xm = mean(mediciones)
    desviacion = std(mediciones, ddof=1)
    t = abs(input_estacion["mediciones"]["PM2_5"]-Xm)/desviacion
    p = n(input_estacion["mediciones"]["PM2_5"], len(mediciones), t)
    if(p < 0.5):
        return None
    return input_estacion




def show(mediciones=[]):
    pass