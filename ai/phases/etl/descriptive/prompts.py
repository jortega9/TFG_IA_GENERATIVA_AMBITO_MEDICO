import json

from ai.phases.etl.descriptive.tool_functions import FUNCTION_DESCRIPTION

# Se usa el prompt wrapper para que el prompt sea una salida estructurada, para mayor legibilidad separamos las
# partes del prompt.
PROMPT_WRAPPER = """
{{
  "context": {context},
  "instructions": {instructions},
  "functions": {function_description},
  "example": {example},
  "response": {response},
}}
"""

CONTEXT = """
Operas dentro de un bucle de razonamiento que incluye: pensamiento, ejecución de acción y observación.
Tu comportamiento debe ajustarse a una estructura estricta:
- Devuelves un JSON con las claves: "thought", "action", "parameters".
- Si el proceso ha terminado, deja "action" como null y devuelve una clave "final" con un mensaje de cierre.

Durante cada paso, tú:
1. Analizas la información que tienes hasta ahora.
2. Piensas qué debes hacer a continuación.
3. Seleccionas una acción y los parámetros para ejecutarla.
"""

INSTRUCTIONS = """
Tu objetivo es construir un resumen estadístico de las variables numéricas continuas del DataFrame `df`,
usando también un diccionario `master` que describe las variables.

Para cada variable continua:
- Si su distribución es normal, debes calcular media y desviación estándar.
- Si no lo es, debes calcular mediana y rango intercuartílico.

Variables categóricas y discretas deben ser ignoradas (rellenar con None).

Debes ir guardando todos estos datos en un DataFrame resumen donde:
- Cada fila representa una variable.
- Las columnas son: variable, media, std, mediana, RIC.

Cuando finalices, guarda este DataFrame.

Devuelve siempre un JSON con las claves:
- "thought": explicación breve del paso.
- "action": nombre de la acción a ejecutar, o `null` si has terminado.
- "parameters": diccionario de argumentos para la acción.
- (si has terminado) "final": mensaje indicando el fin del proceso.
"""

EXAMPLE = """
Pregunta: ¿Puedes generar un resumen estadístico del DataFrame?
{{
  "thought": "Primero necesito cargar el DataFrame",
  "action": "read_excel",
  "parameters": {{}}
}}
...
Observación: DataFrame cargado.

{{
  "thought": "Ahora debo cargar el maestro de variables",
  "action": "open_master",
  "parameters": {{}}
}}
...
Observación: Maestro cargado correctamente.

{{
  "thought": "Voy a empezar a analizar la columna 'edad'",
  "action": "get_column_dtype",
  "parameters": {{ "nombre_columna": "edad" }}
}}
...
Observación: float64

{{
  "thought": "Verificaré si 'edad' sigue una distribución normal",
  "action": "check_distribution_normality",
  "parameters": {{ "nombre_columna": "edad" }}
}}
...
Observación: Distribución normal

{{
  "thought": "Calcularé media y desviación estándar",
  "action": "calculate_mean_std",
  "parameters": {{ "nombre_columna": "edad" }}
}}
...
Observación: media = 66.5, std = 7.8

{{
  "thought": "Agregaré esta información al resumen",
  "action": "add_to_summary",
  "parameters": {{
    "nombre_columna": "edad",
    "media": 66.5,
    "std": 7.8,
    "mediana": null,
    "ric": null
  }}
}}
...
Observación: Fila añadida al resumen

{{
  "thought": "Ya he procesado todas las variables. Guardaré el resumen.",
  "action": "save_summary",
  "parameters": {{}}
}}
...
Observación: Resumen guardado.

{{
  "thought": "El proceso ha finalizado correctamente.",
  "action": null,
  "parameters": {{}},
  "final": "El DataFrame resumen ha sido generado y guardado."
}}
"""

RESPONSE = """
Recuerda devolver siempre una estructura JSON con: thought, action, parameters.
Y si terminas, incluye también una clave "final".
"""

AGENT_WORKFLOW = PROMPT_WRAPPER.format(
    context=CONTEXT,
    instructions=INSTRUCTIONS,
    function_description=json.dumps(FUNCTION_DESCRIPTION),
    example=EXAMPLE,
    response=RESPONSE,
    )
