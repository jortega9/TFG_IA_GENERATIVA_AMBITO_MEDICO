IDENTIFY_WORKFLOW = """
<contexto>
Tu tarea es identificar **todas las variables categóricas** en un conjunto de datos clínicos. Para ello se te proporciona:

1. Un `sample` de 20 filas reales del dataset.
2. Un diccionario `master` que describe cada variable y, si aplica, sus posibles valores categóricos codificados.

Eres un asistente experto en análisis estadístico médico y debes ser muy preciso: muchas variables están mal documentadas, así que **el dataset tiene prioridad sobre el maestro** si hay contradicciones.
</contexto>

<instrucciones>
Una variable categórica representa clases, grupos o categorías finitas. Puede estar representada con números o texto, pero sus valores deben pertenecer a un conjunto limitado y discreto.

Para identificar correctamente una variable categórica:

- **Sí es categórica** si:
  - En el `master` tiene un mapeo `"valores"` que **coincide exactamente** con los valores únicos presentes en el dataset (por ejemplo: {{0: "No", 1: "Sí"}} y en el dataset solo hay 0 y 1).
  - En el dataset aparecen **muy pocos valores únicos (por ejemplo 2 a 6)** y **no hay decimales**, y esos valores representan claramente clases, estados o grupos distintos, aunque no estén definidos en el `master`.

- **NO es categórica** si:
  - Aunque en el `master` tenga `"valores"` definidos, en el dataset:
    - aparecen **valores decimales o continuos**,
    - hay **gran variabilidad numérica**,
    - o los valores no coinciden con el mapeo del `master`.
    Por ejemplo: `psapre` tiene un mapeo discreto en el `master`, pero en el dataset contiene valores como `4.23`, `6.85`, etc., lo que indica claramente un comportamiento **numérico continuo**.
  - Es una **fecha, identificador, porcentaje** o una **medida numérica continua**.
  - Tiene muchos valores únicos en el sample (por ejemplo, más de 10).

<requisitos>

1. Revisa **cada variable** comparando lo que dice el `master` con lo que muestran los datos reales.
2. Si hay discrepancia, **prioriza el comportamiento real en el dataset.**
3. Justifica tus decisiones: explica **por qué** incluyes cada variable categórica.
4. Devuelve un JSON con:
   - `"explicacion"`: razonamiento claro y conciso de cómo llegaste a la decisión.
   - `"variables"`: lista de nombres de columnas categóricas, sin repeticiones ni explicaciones adicionales.

</requisitos>

<entrada>
Master: {master}
Sample del dataset: {sample}
</entrada>
"""



CONCLUSION_WORKFLOW = """

"""