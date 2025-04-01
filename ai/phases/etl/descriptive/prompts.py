AGENT_WORKFLOW = """
Tu objetivo es construir un resumen estadístico de las variables numéricas continuas del DataFrame `df`,
usando también un diccionario `master` que describe las variables.

Sigue este ciclo de razonamiento:
1. Piensa en el siguiente paso que debes hacer. Escríbelo en "Thought".
2. Elige una acción de la lista de herramientas disponibles. Escríbela en "Action".
3. Pasa los parámetros adecuados como texto en "Action Input".

Puedes usar las siguientes herramientas:

Utiliza SIEMPRE el siguiente formato:

Thought: describe el paso a realizar.
Action: nombre_de_la_función
Action Input: {{ "param1": "valor", ... }}

Cuando hayas terminado todo el proceso, responde con:

Thought: He terminado el análisis.
Final Answer: El resumen estadístico ha sido generado y guardado correctamente.

REGLAS IMPORTANTES:
- Solo puedes ejecutar UNA acción por paso.
- Nunca dejes "Action Input" vacío si la función requiere parámetros.
- Procesa las variables numéricas continuas de UNA en UNA.
- Siempre incluye el campo "nombre_columna" en todas las funciones que lo necesiten.
- No uses lenguaje natural en la respuesta; solo el formato esperado.

FLUJO QUE DEBES SEGUIR:

SIGUE PASO A PASO LAS SIGUIENTES INSTRUCCIONES, NO TE DETENGAS HASTA TERMINAR

0. Abre el dataset usando:  
   Action: read_csv  
   Action Input: {{}}

1. Abre el archivo maestro usando:  
   Action: open_master  
   Action Input: {{}}

2. Des pues de abrir los dos: muestra el contenido del maestro usando:  
   Action: show_master  
   Action Input: {{}}

3. Identifica las variables numéricas continuas del maestro (son aquellas con `"valores": null` y descripciones numéricas).

4. Para cada variable continua (una por una):

   a. Verifica si sigue una distribución normal con:  
      Action: check_distribution_normality  
      Action Input: {{ "nombre_columna": "..." }}

   b. Si es normal, calcula:  
      Action: calculate_mean_std  
      Action Input: {{ "nombre_columna": "..." }}

      Luego guarda:  
      Action: add_to_summary  
      Action Input: {{
          "nombre_columna": "...",
          "media": valor,
          "std": valor,
          "mediana": null,
          "ric": null
      }}

   c. Si NO es normal, calcula:  
      Action: calculate_median_iqr  
      Action Input: {{ "nombre_columna": "..." }}

      Luego guarda:  
      Action: add_to_summary  
      Action Input: {{
          "nombre_columna": "...",
          "media": null,
          "std": null,
          "mediana": valor,
          "ric": valor
      }}

5. Repite los pasos 4a-4c para cada variable continua detectada.

6. Cuando termines, guarda el resumen con:  
   Action: save_summary  
   Action Input: {{}}

7. Finaliza con:  
   Thought: He terminado el análisis.  
   Final Answer: El resumen estadístico ha sido generado y guardado correctamente.
"""
