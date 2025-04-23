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

MASTER_PATH = os.path.join(config["data_path"]["processed_path"], "master.json")
GROUP_PATH = os.path.join(config["data_path"]["processed_path"], "variable_grupo.json")
TIME_PATH = os.path.join(config["data_path"]["processed_path"], "variable_time.json")

DF_PATH = os.path.join(config["data_path"]["processed_path"], "dataset.csv")
CHI_PATH = os.path.join(config["data_path"]["processed_path"], "analisis_categorico_chi_cuadrado.csv")

PROMPT = """
<contexto>
{context}

Tu funcion es analizar los resultados de la estadística comparativa de las variables categoricas
con el test de chi cuadrado. El analasis recibido está estructurado en formato CSV donde cada fila
es una variable categorica analizada con la variable objetivo y cada columna es:
variable,tabla de contingencia, chi2, dof, p_value y si la variable es significativa
</contexto>

<seccion>
La seccion en LaTex que vas a crear se conforma de:

Titulo:
Analisis comparativo usando el test Chi-Cuadrado

Tabla del analisis del contenido:
Mostrar la tabla con los resultados del analisis comparativo. 
Muy importante que no incluyas la columna de la tabla de contingencia!
Si la tabla es muy larga, elimina aquellas variables que sean menos significativas dejando algunas
que a pesar de no ser significativas estaban cerca de serlo.

Conclusiones:
Analiza los resultados y da conclusiones de lo más relevante en funcion al contexto
y lo que encuentres importante estadísticamente hablando. Usa el dataset y el maestro
(descripcion de las variables) para analizar los resultados en cuestion al comportamiento 
de la variable con el dataset.
</seccion>

<entrada>
Resultados estadísticos en CSV: {analisis}
Muestra del dataset original: {dataset}
Descripcion de las variables: {master}
</entrada>

<salida>
Devuelve únicamente un JSON válido con el siguiente formato:

{{
  "latex_code": "<aquí va el contenido en LaTeX como string>"
}}

IMPORTANTE: la seccion y subsecciones (si las hay) deben ser directamente integrable en un documento LaTeX.
</salida>
"""

class ChiSquareSummaryAgent(Agent):
    """"""
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv(DF_PATH)
        try:
            self.df_chi = pd.read_csv(CHI_PATH)
        except Exception:
            self.df_chi = None
        with open(MASTER_PATH, "r", encoding="utf-8") as f:
            self.master = json.load(f)
        with open(GROUP_PATH, "r", encoding="utf-8") as f:
            group_config = json.load(f)
            self.group_variable = group_config["group_variable"]
        with open(TIME_PATH, "r", encoding="utf-8") as f:
            time_config = json.load(f)
            self.time_variable = time_config["time_variable"]

    def generate(self) -> str:
        if self.df_chi is None:
            return ""
        response = self.call_llm(
            prompt=PROMPT.format(
                context= CONTEXT.format(target=self.group_variable, time=self.time_variable),
                analisis=self.df_chi.to_string(),
                dataset=self.df.sample(n=20).to_string(),
                master=json.dumps(self.master)
            ),
            response_format=LaTexResponse,
            temperature=0.8
        )
        return response.latex_code

def generate_chi_squared() -> str:
    """"""
    agent = ChiSquareSummaryAgent()
    response = agent.generate()
    return response