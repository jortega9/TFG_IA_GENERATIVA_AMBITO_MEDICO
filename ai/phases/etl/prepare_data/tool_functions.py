FUNCTION_DEFINITIONS = [
  {
    "type": "function",
    "function": {
      "name": "read_excel",
      "description": "Carga un archivo de Excel en un DataFrame de Pandas, leyendo solo la primera hoja y asumiendo que los encabezados están en la segunda fila, y lo almacena.",
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
      "name": "open_master",
      "description": "Carga un archivo JSON que contiene las descripciones de las variables y lo almacena.",
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
      "description": "Devuelve información general del DataFrame usando df.info().",
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
      "name": "view_column_description",
      "description": "Devuelve el significado de una columna concreta usando el maestro, para usarla es necesario abrir el maestro primero",
      "parameters": {
        "type": "object",
        "properties": {
          "column": {
            "type": "string",
            "description": "Nombre de la columna a consultar."
          }
        },
        "required": ["column"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "drop_column",
      "description": "Elimina una columna específica si el usuario la considera irrelevante.",
      "parameters": {
        "type": "object",
        "properties": {
          "column": {
            "type": "string",
            "description": "Nombre de la columna a eliminar."
          }
        },
        "required": ["column"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "ask_question",
      "description": "Si tras acceder al maestro y al dataframe no te queda claro algo, usa esta función para preguntar al usuario cualquier duda sobre el maestro o el dataset para modificarlos.",
      "parameters": {
        "type": "object",
        "properties": {
          "question": {
            "type": "string",
            "description": "La pregunta a realizar al usuario."
          }
        },
        "required": ["question"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "add_to_master",
      "description": "Añade una nueva variable al maestro con la descripción proporcionada por el usuario y los valores si la variable es categórica.",
      "parameters": {
        "type": "object",
        "properties": {
          "column": {
            "type": "string",
            "description": "Nombre de la nueva variable."
          },
          "description": {
            "type": "string",
            "description": "Descripción de la variable."
          }
        },
        "required": ["column", "description"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "update_master_description",
      "description": "ctualiza la descripción de una variable en el maestro para hacerla más clara. Cuando después de leer esa descripción sea demasiado concisa o poco clara.",
      "parameters": {
        "type": "object",
        "properties": {
          "column": {
            "type": "string",
            "description": "Nombre de la variable a actualizar."
          },
          "new_description": {
            "type": "string",
            "description": "La nueva descripción de la variable."
          }
        },
        "required": ["column", "new_description"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "drop_corrupt_records",
      "description": "Identifica y elimina registros corruptos o con errores graves en los datos.",
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
      "name": "drop_corrupt_columns",
      "description": "Identifica y elimina columnas corruptas o con información inconsistente.",
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
      "name": "drop_duplicates",
      "description": "Identifica y elimina filas duplicadas en el dataset.",
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
      "name": "save_files_in_processed_data",
      "description": "Una vez hayas identificado que el dataset y el maestro esten preparados para poder hacerle un analisis estadistico guarda el maestro y df",
      "parameters": {
        "type": "object",
        "properties": {},
        "required": []
      }
    }
  }
]
