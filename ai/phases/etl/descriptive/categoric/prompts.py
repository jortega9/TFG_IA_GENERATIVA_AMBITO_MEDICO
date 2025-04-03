IDENTIFY_WORKFLOW = """
<contexto>
Tu tarea es identificar todas las variables categóricas presentes en un conjunto de datos clínicos. Para ello, se te proporciona:

1. Un fragmento (sample) del DataFrame con los datos reales (20 filas).
2. Un diccionario llamado "maestro" que contiene las descripciones de todas las variables y, cuando aplica, los posibles valores categóricos mapeados como diccionarios.

Debes devolver **únicamente una lista con los nombres exactos** de las variables categóricas detectadas, sin ninguna explicación adicional.
</contexto>

<instrucciones>
Ten en cuenta lo siguiente:

- Una **variable categórica** es aquella que representa clases, grupos o categorías discretas. Puede representarse con valores numéricos o de texto, pero su significado está acotado a un conjunto finito de categorías (ej: sexo, grupo sanguíneo, tipo de tumor).
- No son categóricas las variables **numéricas continuas**, como edad, porcentaje, volumen o cualquier valor medido en una escala infinita o decimal.
- Las **fechas** tampoco se consideran categóricas.

Reglas para identificar correctamente una variable categórica:
1. Si en el maestro aparece con un mapeo de valores, es probable que sea categórica.
2. Si ese mapeo existe pero en el dataset aparecen valores completamente numéricos o con mucha variabilidad decimal, probablemente **no** es categórica y debes descartarla.
3. Si no hay mapeo en el maestro, pero en el dataset se repiten pocos valores únicos que representan categorías, puede ser una categórica implícita.
4. Si una variable parece ambigua, decide usando tanto el contenido del maestro como el comportamiento de la variable en el dataset (frecuencia, tipos de valores, etc.).
</instrucciones>

<entrada>
A continuación se te dará el contenido del maestro y un sample del dataset. Devuelve una lista con los nombres exactos de las variables categóricas detectadas, sin explicaciones ni justificación.

Maestro: {master}
Sample del dataset: {sample}
</entrada>
"""

CONCLUSION_WORKFLOW = """

"""