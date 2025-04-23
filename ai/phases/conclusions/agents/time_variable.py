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

PROMPT = """
<contexto>
{context}

La seccion en la que vas a trabajar será la definicion y descripcion de la variable 
de tiempo para el analisis de supervivencia.
</contexto>

<seccion>
La seccion en LaTex que vas a crear se conforma de:

Titulo:
Variable de Seguimiento.

Contenido:
La definición y la descripción de la variable de seguimiento para el estudio del analisis 
de supervivencia para la variable de objetivo. este contenido se tiene que basar
en como se comporta en el dataset a estudiar y los conocimientos que tengas, 
usa el dataset y el maestro (descripcion de variables) para hacer tu trabajo.
</seccion>

<entrada>
Variable de tiempo: {time}
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

class TimeAgent(Agent):
    """"""
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv(DF_PATH)
        with open(MASTER_PATH, "r", encoding="utf-8") as f:
            self.master = json.load(f)
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
                time=self.time_variable,
                dataset=self.df.sample(n=20).to_string(),
                master=json.dumps(self.master)
            ),
            response_format=LaTexResponse,
            temperature=0.8
        )
        return response.latex_code

def generate_time_variable() -> str:
    agent = TimeAgent()
    response = agent.generate()
    return response