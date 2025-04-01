FUNCTION_DESCRIPTION = [
    {
        "type": "function",
        "function": {
            "name": "open_master",
            "description": "Es la primera acción que debes hacer. Carga un archivo JSON que contiene las descripciones de las variables y lo almacena como un diccionario llamado 'master'.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_csv",
            "description": "Carga un archivo de Excel en un DataFrame de Pandas llamado 'df', leyendo solo la primera hoja y asumiendo que los encabezados están en la segunda fila.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sample_df",
            "description": "Devuelve una muestra aleatoria de n registros del DataFrame.",
            "parameters": {
                "type": "object",
                "properties": {
                    "n": {
                        "type": "integer",
                        "description": "Número de registros a mostrar."
                    }
                },
                "required": ["n"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "info_df",
            "description": "Devuelve información general del DataFrame usando df.info() como texto.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_column_dtype",
            "description": "Recibe el nombre de una columna y devuelve su tipo inferido por Pandas (por ejemplo: 'float64', 'object', 'int64').",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre_columna": {
                        "type": "string",
                        "description": "Nombre de la columna de la cual se quiere conocer el tipo de dato."
                    }
                },
                "required": ["nombre_columna"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_distribution_normality",
            "description": "Verifica si una columna numérica sigue una distribución normal mediante una prueba estadística (como Shapiro-Wilk).",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre_columna": {
                        "type": "string",
                        "description": "Nombre de la columna a analizar."
                    }
                },
                "required": ["nombre_columna"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_mean_std",
            "description": "Calcula la media y la desviación estándar para una columna numérica.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre_columna": {
                        "type": "string",
                        "description": "Nombre de la columna para calcular media y desviación estándar."
                    }
                },
                "required": ["nombre_columna"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_median_iqr",
            "description": "Calcula la mediana y el rango intercuartílico (RIC) para una columna numérica.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre_columna": {
                        "type": "string",
                        "description": "Nombre de la columna para calcular mediana y RIC."
                    }
                },
                "required": ["nombre_columna"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_to_summary",
            "description": "Agrega los valores estadísticos calculados de una variable al DataFrame resumen.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre_columna": {
                        "type": "string",
                        "description": "Nombre de la variable."
                    },
                    "media": {
                        "type": ["number", "null"],
                        "description": "Media de la variable (None si no aplica)."
                    },
                    "std": {
                        "type": ["number", "null"],
                        "description": "Desviación estándar (None si no aplica)."
                    },
                    "mediana": {
                        "type": ["number", "null"],
                        "description": "Mediana (None si no aplica)."
                    },
                    "ric": {
                        "type": ["number", "null"],
                        "description": "Rango intercuartílico (None si no aplica)."
                    }
                },
                "required": ["nombre_columna", "media", "std", "mediana", "ric"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_summary",
            "description": "Guarda el DataFrame resumen generado en un archivo local para su uso posterior.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]
