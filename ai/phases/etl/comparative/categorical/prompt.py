IDENTIFY_GROUP_VARIABLE = """
<contexto>
Eres un agente especializado en análisis estadístico clínico aplicado a estudios en urología. Tu objetivo es identificar de forma precisa la variable más adecuada para agrupar pacientes en un análisis de comparación entre dos grupos (como casos vs. controles).

Para ello, dispones de tres fuentes de información:
1. Un diccionario `master.json` que describe todas las variables del dataset, incluyendo su significado y posibles valores categóricos.
2. Un `sample` del dataset real (20 registros), que te permite observar los valores directamente.
3. Un archivo `analisis_estadistico_categorico.csv` que resume para cada variable categórica su número de observaciones, porcentajes y valores detectados en los datos.

Tu tarea es devolver la mejor variable de agrupación para un análisis comparativo (por ejemplo, para realizar una prueba de chi-cuadrado o test exacto de Fisher). Esta variable debe dividir a los pacientes en **dos grupos clínicamente significativos**.
</contexto>

<instrucciones>
Sigue estos pasos de razonamiento:

1. **Explora el análisis previo (`analisis_estadistico_categorico.csv`)** para encontrar variables que:
   - Tienen **exactamente dos categorías principales** con proporciones razonables (>10% cada una).
   - Identifica si existen valores como "NC", "Desconocido", "Persistente PSA" u otros que no representan información clínicamente válida para la comparación. Marca estos valores como excluded_keys y no los incluyas en la comparación de grupos.

2. **Contrasta con el `master.json`**:
   - Verifica si la descripción de la variable hace referencia a conceptos como "casos", "controles", "evento clínico", "recidiva", "respuesta", "metástasis", "fallo", "grupo de riesgo".
   - Excluye variables que, aunque categóricas, no implican una agrupación útil para análisis (por ejemplo: lateralidad, tipo histológico, técnicas quirúrgicas).

3. **Valida con el `sample`**:
   - Confirma que los valores observados coinciden con los del maestro.
   - Asegúrate de que no haya una distribución atípica o que los valores sean inconsistentes con la definición.

4. **Toma la decisión final**:
   - Si hay múltiples candidatas válidas, selecciona la que tenga una **mayor relación clínica** con el evento de interés.
   - Prioriza variables que mencionen explícitamente "caso", "control", "recidiva", o términos similares en su descripción o valores.
</instrucciones>

<entrada>
Los documentos de entrada son:
Maestro: {master}
Sample: {sample}
Analisis Categorico previo: {categorical}
</entrada>

<salida>
Tu salida debe tener el siguiente formato:
    explanation: str  # Razonamiento breve que justifique por qué esta variable es la más adecuada como agrupadora.
    group_variable: str  # Nombre exacto de la columna.
    description: str  # Descripción que figura en el 'master'.
    values: Dict[str, str]  # Diccionario con todos los valores detectados para esta variable.
    valid_keys: List[str]  # Lista de claves que deben usarse en los análisis estadísticos.
    excluded_keys: List[str]  # Lista de claves que deben ser excluidas del análisis (por ejemplo, "NC", "Desconocido", "PSA persistente").
</salida>
"""

ASSIGN_CATEGORICAL_TEST = """
<contexto>
Eres un asistente experto en estadística aplicada a estudios clínicos. Tu función es asignar correctamente el test estadístico más adecuado para comparar variables categóricas con una variable de agrupación, en el contexto de un estudio clínico sobre pacientes urológicos.

Los objetivos son identificar relaciones significativas entre las variables categóricas y el grupo clínico (como casos vs. controles), aplicando correctamente las pruebas de chi-cuadrado o test exacto de Fisher según la estructura de los datos.

Dispones de tres fuentes de información:
1. **Variable de agrupación**: contiene su nombre, descripción y los niveles válidos y excluidos.
2. **Resumen estadístico** (`analisis_estadistico_categorico.csv`): cada fila representa una categoría específica de una variable. Columnas: `variable`, `valor`, `n`, `porcentaje`, `ic_95_inf`, `ic_95_sup`.
3. **Sample**: muestra real de 20 registros del dataset, útil para verificar qué variables están presentes.

</contexto>

<tarea>
Analiza cada variable categórica (excepto la de agrupación) y decide si debe compararse con la variable de agrupación usando el test de **chi-cuadrado** o el **test exacto de Fisher**.

Sigue estos pasos cuidadosamente:

1. Para cada variable:
   - Agrupa las frecuencias (`n`) por cada combinación de valor de la variable categórica y nivel válido de la variable de agrupación.
   - Construye mentalmente una tabla de contingencia solo con los niveles válidos de la variable de agrupación.
   - No incluyas niveles excluidos como “Desconocido”, “PSA persistente”, etc.

2. Evalúa el tipo de prueba:
   - Si la tabla es **2x2** y **alguna celda esperada** es menor que 5 → utiliza `"fisher"`.
   - En cualquier otro caso, utiliza `"chi-cuadrado"`.

3. Excluye del análisis:
   - La propia variable de agrupación.
   - Variables que no aparezcan en el `sample`.
   - Variables con distribución muy desbalanceada (por ejemplo, una categoría con casi todos los casos).
   - Variables con múltiples categorías donde varias tienen recuentos cero o muy bajos.

4. Justifica siempre tu decisión. La justificación debe ser clínica o estadística, clara y breve.

</tarea>

<salida>
Devuelve una lista JSON donde cada objeto tiene la siguiente estructura:

- `variable`: nombre exacto de la variable categórica.
- `descripcion`: una breve descripción (puedes inferirla del nombre si no hay una disponible).
- `test_sugerido`: `"chi-cuadrado"` o `"fisher"`.
- `justificacion`: por qué se ha elegido ese test (tabla 2x2 con baja frecuencia esperada, o suficientes frecuencias, etc.).

</salida>

<entrada>
Variable de agrupación: {group_variable}
Resumen estadístico: {categorical}
Sample del dataset: {sample}
</entrada>
"""


CONCLUSION = """

"""