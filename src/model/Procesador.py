from numpy import mean,std,sqrt,pi,e
from scipy.integrate import quad
from datetime import datetime, timedelta

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

def save(input_estacion:dict, db)->dict:
    """
    Retorna la estación si la medición que contiene es válida
    o retorna un valor nulo si no lo es
    Esto significa que elimina los datos nulos
    y los datos atípicos usando el criterio de chauvenet
    """
    mediciones = []
    now = datetime.today()
    yesterday = now - timedelta(days=1)
    if(input_estacion["mediciones"][0]["fecha_hora"] == None):
        return None
    else:
        mediciones.append(input_estacion["mediciones"][0]["PM2_5"])
    # Se van a tomar todos los datos de las últimas 48 horas
    db_estacion = db.get_estacion_by_date(input_estacion["codigo"], yesterday, now)
    if(db_estacion is not None):
        for m in db_estacion["mediciones"]:
            mediciones.append(m["PM2_5"])
    
    Xm = mean(mediciones)
    
    # El cálculo de la desviación de la siguiente instrucción 
    # es equivalente a la siguiente función:
    # desviacion = sqrt(1/(N-1)*sum((mediciones-Xm)**2))
    # en donde:
    # N = len(mediciones)
    # Xm = mean(mediciones)
    desviacion = std(mediciones, ddof=1)
    t = abs(input_estacion["mediciones"][0]["PM2_5"]-Xm)/desviacion
    p = n(input_estacion["mediciones"][0]["PM2_5"], len(mediciones), t)
    if(p < 0.5):
        return None
    return input_estacion




def show(fecha_inicial,fecha_final,db):
    
    pass