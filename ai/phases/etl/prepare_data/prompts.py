# STRING = """hola {text}"""
# STRING.format(text=variable1, text2=variable2)

EXTRACT_INFO_VARIABLES = """ 
<contexto>
Actúa como un experto en procesamiento de texto y estructuración de datos. Quiero que analices un texto que \
contiene la descripción de las variables de un dataset y lo transformes en un JSON estructurado.
</contexto>

<instrucciones>
1. Leer un texto, ignorando cualquier información irrelevante.
2. Identificar las variables y sus descripciones, que están delimitadas en texto libre.
3. Extraer correctamente las variables categóricas con sus valores etiquetados y significados.
4. Transformación a JSON con la siguiente estructura:
5. Si la variable es numérica y no tiene valores específicos, el campo "valores" debe ser None.
6. Si la variable es categórica, el campo "valores" debe contener un diccionario donde las claves sean los valores numéricos \ 
y los valores sean sus significados (según la estructura del documento).

Manejo de casos específicos:

Diferenciar correctamente entre variables numéricas y categóricas en función de su formato.
Identificar variables categóricas cuando tienen valores numerados seguidos de descripciones.
Si la descripción de la variable está ausente o mal formateada, intentar inferir su significado a partir del contexto.

Devolver un JSON bien estructurado con todas las variables procesadas y formateadas correctamente.
</instrucciones>

<salida>
[
    {{
        "column_name": "EDAD",
        "column_info": {{
            "descripcion": "Edad del paciente",
            "valores": null
        }}
    }},
    {{
        "column_name": "ETNIA",
        "column_info": {{
            "descripcion": "Etnia del paciente",
            "valores": {{
                "1": "Caucásico",
                "2": "Negro",
                "3": "Hispano",
                "4": "Asiático"
            }}
        }}
    }}
]
</salida>

El texto que tienes que analizar es: {text}
"""