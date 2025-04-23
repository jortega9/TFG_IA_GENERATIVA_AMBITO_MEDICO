import pandas as pd

def obtener_media_std(path_csv):
    """
    Lee un archivo CSV con estadísticas y devuelve un diccionario con la media y std de cada variable.

    Args:
        path_csv (str): Ruta al archivo CSV.

    Returns:
        dict: Diccionario con la forma {variable: {'media': valor, 'std': valor}}.
    """
    try:
        df = pd.read_csv(path_csv)
    except Exception as e:
        return {}
    
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
    try :
        df = pd.read_csv(path_csv)
    except Exception as e:
        return {}
    
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
    try:
        df = pd.read_csv(path_csv)
    except Exception as e:
        return {}
        
    resultado = {}
    for _, fila in df.iterrows():
        variable = fila['variable']
        valor = fila['valor']
        ic_95_inf = fila['ic_95_inf']
        ic_95_sup = fila['ic_95_sup']
        porcentaje = fila['porcentaje']
        n = fila['n']
        valor = fila['valor'].split('.')[0]
        clave = f"{fila['variable']}_{valor}"
        resultado[clave] = {
            'variable': variable,
            'valor': valor,
            'n': n,
            'porcentaje': porcentaje,
            'ic_95_inf': ic_95_inf,
            'ic_95_sup': ic_95_sup
        }
    
    return resultado

def obtener_chi_cuadrado(path_csv):
    """
    Lee un archivo CSV con estadísticas y devuelve un diccionario con el chi cuadrado y otros datos de cada variable.

    Args:
        path_csv (str): Ruta al archivo CSV.

    Returns:
        dict: Diccionario con la forma {variable: {'chi_cuadrado': valor, 'tabla': valor, 'dof': valor, 'p_value': valor, 'significativo': valor}}.
    """
    try:
        df = pd.read_csv(path_csv)
    except Exception as e:
        return {}
        
    resultado = {}
    for _, fila in df.iterrows():
        variable = fila['variable']
        tabla = fila['tabla']
        chi_cuadrado = fila['chi2']
        dof = fila['dof']
        p_value = fila['p_value']
        significativo = fila['significativo']
        
        resultado[variable] = {
            'tabla': tabla,
            'chi_cuadrado': chi_cuadrado,
            'dof': dof,
            'p_value': p_value,
            'significativo': significativo
        }
    
    return resultado


def obtener_fisher(path_csv):
    """
    Lee un archivo CSV con estadísticas y devuelve un diccionario con el fisher y otros datos de cada variable.

    Args:
        path_csv (str): Ruta al archivo CSV.

    Returns:
        dict: Diccionario con la forma {variable: {'fisher': valor, 'tabla': valor, 'dof': valor, 'p_value': valor, 'significativo': valor}}.
    """
    try:
        df = pd.read_csv(path_csv)
    except Exception as e:
        return {}
    
    resultado = {}
    for _, fila in df.iterrows():
        variable = fila['variable']
        tabla = fila['tabla']
        stat = fila['stat']
        p_value = fila['p_value']
        significativo = fila['significativo']
        
        resultado[variable] = {
            'tabla': tabla,
            'stat': stat,
            'p_value': p_value,
            'significativo': significativo
        }
    
    return resultado

    
def obtener_mann_withney(path_csv):
    """
    Lee un archivo CSV con estadísticas y devuelve un diccionario con el mann withney y otros datos de cada variable.

    Args:
        path_csv (str): Ruta al archivo CSV.

    Returns:
        dict: Diccionario con la forma {variable: {'mann': valor, 'tabla': valor, 'dof': valor, 'p_value': valor, 'significativo': valor}}.
    """
    try:
        df = pd.read_csv(path_csv)
    except Exception as e:
        return {}
    
    resultado = {}
    for _, fila in df.iterrows():
        variable = fila['variable']
        n_casos = fila['n_casos']
        n_controles = fila['n_controles']
        p_value = fila['p_value']
        significativo = fila['significativo']
        
        resultado[variable] = {
            'n_casos': n_casos,
            'n_controles': n_controles,
            'p_value': p_value,
            'significativo': significativo
        }
    
    return resultado

def obtener_t_student(path_csv):
    """
    Lee un archivo CSV con estadísticas y devuelve un diccionario con el t student y otros datos de cada variable.

    Args:
        path_csv (str): Ruta al archivo CSV.

    Returns:
        dict: Diccionario con la forma {variable: {'tStudent': valor, 'tabla': valor, 'dof': valor, 'p_value': valor, 'significativo': valor}}.
    """
    try:
        df = pd.read_csv(path_csv)
    except Exception as e:
        return {}

    resultado = {}
    for _, fila in df.iterrows():
        variable = fila['variable']
        n_casos = fila['n_casos']
        n_controles = fila['n_controles']
        p_value = fila['p_value']
        significativo = fila['significativo']
        
        resultado[variable] = {
            'n_casos': n_casos,
            'n_controles': n_controles,
            'p_value': p_value,
            'significativo': significativo
        }
    
    return resultado

def obtener_significativas(path_csv):

    try:
        df = pd.read_csv(path_csv)
    except Exception as e:
        return {}

    resultado = {}
    for _, fila in df.iterrows():
        variable = fila['variable']
        tipo = fila['tipo']
        test_aplicado = fila['test_aplicado']
        valor = fila['valor']
        
        resultado[variable] = {
            'tipo': tipo,
            'test_aplicado': test_aplicado,
            'valor': valor,
        }
    
    return resultado

def obtener_kaplan_general(path_csv):

    try:
        df = pd.read_csv(path_csv)
    except Exception as e:
        return {}
    resultado = {}
    for _, fila in df.iterrows():
        variable = fila['variable']
        median_survival_time = fila['median_survival_time']
        n_observations = fila['n_observations']
        
        resultado[variable] = {
            'median_survival_time': median_survival_time,
            'n_observations': n_observations,
        }
    
    return resultado

def obtener_kaplan_vars(path_csv):

    try:
        df = pd.read_csv(path_csv)
    except Exception as e:
        return {}
    resultado = {}
    for _, fila in df.iterrows():
        variable = str(fila['variable'])
        median_survival_time = str(fila['median_survival_time'])
        group = str(fila['group'])
        n_patients = str(fila['n_patients'])
        
        clave = f"{variable}_{group}"
        resultado[clave] = {
            "group": group,
            'median_survival_time': median_survival_time,
            'n_patients': n_patients,
        }
    
    return resultado