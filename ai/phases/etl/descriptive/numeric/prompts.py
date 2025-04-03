AGENT_WORKFLOW = """
<contexto>
Tu objetivo es construir un resumen estadístico de las variables numéricas continuas del DataFrame `df`,
usando también un diccionario `master` que describe las variables.

Definición precisa:
Una variable numérica continua es una magnitud cuantitativa que puede asumir un número infinito de valores dentro de un rango. Proviene de un subconjunto de los números reales y permite operaciones como media, desviación estándar, mediana o percentiles. Estas variables no tienen categorías predefinidas y sus valores no están limitados a opciones discretas.

Ejemplos típicos: edad, peso, altura, tiempo, concentraciones, porcentajes, medidas continuas de laboratorio, etc.

Ejemplos que NO son variables numéricas continuas:
- Fechas o identificadores (e.g. `fecha`, `nhis`)
- Variables binarias o dicotómicas
- Códigos que representan categorías (aunque usen números)
- Variables con menos de 10 valores únicos

Identificación correcta:
Para detectar correctamente estas variables, debes combinar la información de:
- El diccionario `master` (clave: `"valores": null`)
- Una muestra real del DataFrame (`sample_df`)
y analizar ambos para comprobar que las variables son verdaderamente numéricas continuas.

NO incluyas variables dudosas. Si tienes dudas, **omite la variable**.
</contexto>

<instrucciones>

Sigue este ciclo de razonamiento paso a paso:

1. Escribe un "Thought" describiendo lo que vas a hacer.
2. Ejecuta una única herramienta.
3. Pasa los parámetros requeridos en "Action Input".

Formato ESTRICTO:

Thought: descripción del paso.
Action: nombre_de_la_función
Action Input: {{ "param1": "valor", ... }}

Cuando termines, responde con:

Thought: He terminado el análisis.
Final Answer: El resumen estadístico ha sido generado y guardado correctamente.
</instrucciones>

<reglas>

REGLAS IMPORTANTES:
- Una sola acción por paso.
- Nunca dejes "Action Input" vacío si la función necesita parámetros.
- Procesa las variables numéricas continuas de UNA EN UNA.
- Siempre incluye el campo "nombre_columna".
- NO uses lenguaje natural fuera del formato definido.
- NO finalices tras una acción aislada. Continúa con el flujo completo hasta el Final Answer.

</reglas>

<flujo>
FLUJO DETALLADO DEL ANÁLISIS:

0. Abre el dataset:
Action: read_csv
Action Input: {{}}

1. Abre el archivo maestro:
Action: open_master
Action Input: {{}}

2. Muestra el contenido del maestro:
Action: show_master
Action Input: {{}}

3. Analiza tanto el contenido del maestro (`show_master`) como la muestra del dataset (`sample_df`) y genera una lista de TODAS las variables numéricas continuas que cumplen las siguientes condiciones:

   - Tienen `"valores": null` en el maestro.
   - Contienen muchos valores distintos en la muestra (`sample_df`), típicamente más de 10.
   - Representan medidas cuantitativas (no fechas, IDs, ni codificaciones categóricas).
   - NO deben tener descripciones que impliquen codificación categórica o estados fijos (como "riesgo", "positivo/negativo", etc).

   Escribe la lista explícita con este formato:

   Thought: Las siguientes variables cumplen criterios de variable numérica continua: ["edad", "psalt", "volumen", ...]

   Luego comienza el análisis para cada una de ellas.

4. Utiliza tanto el maestro como la muestra para identificar TODAS las variables numéricas continuas. (Aplica la definición anterior con cuidado.)

5. Para cada variable continua detectada:

   a. Verifica si sigue una distribución normal:
   Action: check_distribution_normality
   Action Input: {{ "nombre_columna": "..." }}

   b. Si es normal:
      - Calcula:
        Action: calculate_mean_std
        Action Input: {{ "nombre_columna": "..." }}

      - Guarda:
        Action: add_to_summary
        Action Input: {{
            "nombre_columna": "...",
            "n": valor,
            "media": valor,
            "std": valor,
            "mediana": null,
            "ric": null,
            "rango": "null"
        }}

   c. Si NO es normal:
      - Calcula:
        Action: calculate_median_iqr
        Action Input: {{ "nombre_columna": "..." }}

      - Guarda:
        Action: add_to_summary
        Action Input: {{
            "nombre_columna": "...",
            "n": valor,
            "media": null,
            "std": null,
            "mediana": valor,
            "ric": valor,
            "rango": "x1-x2"
        }}

6. Repite el paso 5 para todas las variables continuas detectadas.

7. Guarda el resumen final:
Action: save_summary
Action Input: {{}}

8. Finaliza el proceso:
Thought: He terminado el análisis.
Final Answer: El resumen estadístico ha sido generado y guardado correctamente.
</flujo>
"""
