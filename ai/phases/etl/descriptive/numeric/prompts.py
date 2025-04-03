IDENTIFY_WORKFLOW = """
<contexto>
Eres un experto en análisis de datos médicos y estadística aplicada. Se te proporcionarán dos estructuras:

- Un diccionario llamado `master` que contiene metadatos sobre las variables del dataset. Cada entrada incluye el nombre de la variable, una breve descripción, y un campo `"valores"` que puede ser `null` (para variables numéricas continuas) o contener categorías/precios discretos (para variables cualitativas o discretas).
- Un `sample` del DataFrame con valores reales de algunas columnas, que puedes usar para observar el tipo de dato, su distribución aparente, y comprobar si los valores parecen numéricos y continuos.
</contexto>

<importante>
Una variable numérica continua es aquella que representa una magnitud medible y puede tomar una amplia variedad de valores numéricos, incluyendo decimales o enteros, sin limitarse a categorías fijas. Su distribución en el dataset suele mostrar variación real y no se restringe a pocos valores repetidos.

Son variables numéricas continuas:
- Las que expresan medidas como edad, tiempo, volumen, porcentaje, concentración, etc.
- Tienen valores reales (decimales o enteros) con amplia variabilidad.

No son variables numéricas continuas:
- Variables categóricas codificadas como números (suelen tener "valores" definidos en el maestro).
- Variables discretas (pocos valores enteros, como recuentos).
- Fechas (aunque se expresen como números, representan eventos en el tiempo).
- Identificadores (números únicos sin valor cuantitativo real).
</importante>

<instrucciones>

Tu objetivo es **identificar de forma precisa todas las variables que sean numéricas continuas** en el dataset. Para ello:
1. Razona usando ambos elementos:
   - Si en el `master` una variable tiene `"valores": null` y en el `sample` contiene datos numéricos con decimales o gran variabilidad, probablemente es continua.
   - Si en el `master` la variable tiene categorías (es decir, `"valores"` no es null) pero en el `sample` contiene valores numéricos muy variados y sin codificación aparente, podría estar mal documentada y **también** deberías considerarla como continua si el patrón lo justifica.
   - Ignora las columnas con texto, fechas, identificadores o codificaciones categóricas claras.

2. **Piensa paso a paso**. Para cada variable, analiza:
   - ¿Qué dice el `master` sobre esta variable?
   - ¿Qué muestran los datos reales del `sample`?
   - ¿Hay evidencia de que sea continua a pesar de la definición del `master`?

3. No asumas que el `master` es siempre correcto. Prioriza el razonamiento basado en los datos reales si hay contradicciones.

4. Devuelve **únicamente una lista en formato Python** con los nombres (str) de las variables que consideres numéricas continuas. No incluyas explicación, encabezados, ni justificaciones. Solo la lista.

5. **NO INCLUYAS BAJO NINGUNA CIRCUNSTANCIA FECHAS, IDENTIFICADORES, VARIABLES CATEGORICAS Y DISCRETAS**
</instrucciones>


<entrada>
Sample del dataframe: {sample}
Diccionario del maestro: {master}
</entrada>
"""

CONCLUSION_WORKFLOW = """

"""