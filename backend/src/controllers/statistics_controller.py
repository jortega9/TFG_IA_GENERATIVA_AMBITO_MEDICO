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
