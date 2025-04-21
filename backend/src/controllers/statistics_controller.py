import pandas as pd

def obtener_media_std(path_csv):
    """
    Lee un archivo CSV con estadísticas y devuelve un diccionario con la media y std de cada variable.

    Args:
        path_csv (str): Ruta al archivo CSV.

    Returns:
        dict: Diccionario con la forma {variable: {'media': valor, 'std': valor}}.
    """
    df = pd.read_csv(path_csv)
    
    resultado = {}
    for _, fila in df.iterrows():
        variable = fila['variable']
        media = fila['media']
        std = fila['std']
        n = fila['n']
        resultado[variable] = {
            'n': n,
            'media': media,
            'std': std
        }
    
    return resultado

def obtener_mediana_rangoI(path_csv):
    """
    Lee un archivo CSV con estadísticas y devuelve un diccionario con la mediana y rango intercuartílico de cada variable.

    Args:
        path_csv (str): Ruta al archivo CSV.

    Returns:
        dict: Diccionario con la forma {variable: {'mediana': valor, 'rangoI': valor}}.
    """
    df = pd.read_csv(path_csv)
    
    resultado = {}
    for _, fila in df.iterrows():
        variable = fila['variable']
        mediana = fila['mediana']
        rangoI = fila['ric']
        n = fila['n']
        resultado[variable] = {
            'n': n,
            'mediana': mediana,
            'rangoI': rangoI
        }
    
    return resultado

def obtener_freq_ic95(path_csv):
    """
    Lee un archivo CSV con estadísticas y devuelve un diccionario con la frecuencia y el intervalo de confianza del 95% de cada variable.

    Args:
        path_csv (str): Ruta al archivo CSV.

    Returns:
        dict: Diccionario con la forma {variable: { }}.
    """
    df = pd.read_csv(path_csv)
    
    resultado = {}
    for _, fila in df.iterrows():
        variable = fila['variable']
        valor = fila['valor']
        ic_95_inf = fila['ic_95_inf']
        ic_95_sup = fila['ic_95_sup']
        porcentaje = fila['porcentaje']
        n = fila['n']
        clave = f"{fila['variable']}_{int(fila['valor'])}"
        resultado[clave] = {
            'variable': variable,
            'valor': valor,
            'n': n,
            'porcentaje': porcentaje,
            'ic_95_inf': ic_95_inf,
            'ic_95_sup': ic_95_sup
        }
    
    return resultado

def det_corr_vars(csvMannWhitneyPath, csvTStudentPath, csvChiPath, csvFisherPath):
    #TODO
    """
    Lee un archivo CSV con estadísticas y devuelve un diccionario con la correlación entre variables.

    Args:
        path_csv (str): Ruta al archivo CSV.

    Returns:
        dict: Diccionario con la forma {variable1_variable2: {'correlacion': valor}}.
    """
    df_mw = pd.read_csv(csvMannWhitneyPath)
    df_t = pd.read_csv(csvTStudentPath)
    df_chi = pd.read_csv(csvChiPath)
    df_fisher = pd.read_csv(csvFisherPath)
    
    resultado = {}
    for _, fila in df_mw.iterrows():
        variable1 = fila['variable1']
        variable2 = fila['variable2']
        correlacion = fila['correlacion']
        n = fila['n']
        clave = f"{fila['variable1']}_{fila['variable2']}"
        resultado[clave] = {
            'n': n,
            'correlacion': correlacion
        }
    
    return resultado
