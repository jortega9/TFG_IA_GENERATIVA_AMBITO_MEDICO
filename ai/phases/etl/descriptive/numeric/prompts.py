IDENTIFY_WORKFLOW = """
<contexto>
Eres un experto en análisis estadístico de datos médicos. Se te proporciona:

1. Un `sample` (fragmento del dataset real con 20 filas) que muestra los valores reales de cada variable.
2. Un `master` (diccionario) que contiene descripciones de las variables y, cuando aplica, los posibles valores codificados como categorías.

Tu objetivo es identificar **todas las variables numéricas continuas** en el dataset basándote tanto en la descripción (`master`) como en los valores reales (`sample`).
</contexto>

<definiciones>
Una variable **numérica continua** es aquella que:
- Representa cantidades medibles como edad, tiempo, porcentaje, volumen, concentración, etc.
- Toma muchos valores diferentes, a menudo con decimales o alta variabilidad.
- No representa categorías, fechas, identificadores ni recuentos discretos.

NO son numéricas continuas:
- Fechas (aunque numéricas, representan momentos en el tiempo).
- Identificadores únicos como números de historia clínica.
- Variables categóricas codificadas con números (si tienen pocos valores únicos o están mapeadas en el `master`).
- Recuentos o categorías discretas con pocos valores posibles.

Si hay contradicción entre `master` y `sample`, **prioriza el análisis de los datos reales**. Si una variable en el `master` aparece con categorías (`valores`) pero en el dataset muestra muchos valores distintos sin patrón categórico claro, **puede** ser continua.

Si no estás seguro, razona siempre antes de decidir.
</definiciones>

<instrucciones>
1. Analiza cada variable comparando su definición en `master` con sus datos reales en `sample`.
2. Si los valores reales indican alta variabilidad y la descripción también sugiere una magnitud (edad, volumen, %…), clasifícala como continua.
3. Ignora cualquier variable que tenga apariencia de fecha, identificador, texto libre o categorías claras.
4. Devuelve un diccionario con dos claves:

- `explicacion`: explica brevemente el razonamiento para clasificar cada variable continua o descartarla.
- `variables`: una lista con los nombres exactos de las variables identificadas como numéricas continuas.

</instrucciones>

<entrada>
Sample del dataset: {sample}

Diccionario maestro: {master}
</entrada>
"""



CONCLUSION_WORKFLOW = """

"""