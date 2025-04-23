import configparser
import json
import os
import sys

import pandas as pd
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from ai.agents.agent import Agent
from ai.phases.conclusions.schema import LaTexResponse
from ai.phases.conclusions.context import CONTEXT

load_dotenv()

SETTINGS_PATH = os.getenv("SETTINGS_PATH")

config = configparser.ConfigParser()
config.read(SETTINGS_PATH)

GROUP_PATH = os.path.join(config["data_path"]["processed_path"], "variable_grupo.json")
TIME_PATH = os.path.join(config["data_path"]["processed_path"], "variable_time.json")

DF_PATH = os.path.join(config["data_path"]["processed_path"], "dataset.csv")
CAT_PATH = os.path.join(config["data_path"]["processed_path"], "analisis_estadistico_categorico.csv")

PROMPT = """
<contexto>
{context}

Tu función es analizar los resultados de estadística descriptiva para las variables categoricas de una base de datos clínica. 
El análisis recibido está estructurado en formato CSV, donde cada fila corresponde a una variable, e incluye: 
valor de la variable categorica, número de observaciones (n), porcentaje del valor, intervalo de confianza 95%.
</contexto>

<seccion>
La seccion en LaTex que vas a crear se conforma de:

Titulo:
Analisis descriptivo de variables categoricas

Tabla del analisis del contenido:
Mostrar la tabla con los resultados del analisis descriptivo. Si es muy grande la tabla busca una forma de recortarla y hacer que
la organizacion del documento no se vea afectada.

Conclusiones:
Analiza los resultados y da conclusiones de lo más relevante en funcion al contexto
y lo que encuentres importante estadísticamente hablando.
</seccion>

<entrada>
Resultados estadísticos en CSV: {analisis}
Muestra del dataset original: {dataset}
</entrada>

<salida>
Devuelve únicamente un JSON válido con el siguiente formato:

{{
  "latex_code": "<aquí va el contenido en LaTeX como string>"
}}

IMPORTANTE: la seccion y subsecciones (si las hay) deben ser directamente integrable en un documento LaTeX.
</salida>
"""

class CategoricalSummaryAgent(Agent):
    """"""
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv(DF_PATH)
        self.df_cat = pd.read_csv(CAT_PATH)
        with open(GROUP_PATH, "r", encoding="utf-8") as f:
            group_config = json.load(f)
            self.group_variable = group_config["group_variable"]
        with open(TIME_PATH, "r", encoding="utf-8") as f:
            time_config = json.load(f)
            self.time_variable = time_config["time_variable"]

    def generate(self) -> str:
        response = self.call_llm(
            prompt=PROMPT.format(
                context= CONTEXT.format(target=self.group_variable, time=self.time_variable),
                analisis=self.df_cat.to_string(),
                dataset=self.df.sample(n=20).to_string(),
            ),
            response_format=LaTexResponse,
            temperature=0.8
        )
        return response.latex_code


def generate_categorical_summary() -> str:
    """"""
    agent = CategoricalSummaryAgent()
    response = agent.generate()
    return response