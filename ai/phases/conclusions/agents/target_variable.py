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

TIME_PATH = os.path.join(config["data_path"]["processed_path"], "variable_time.json")

DF_PATH = os.path.join(config["data_path"]["processed_path"], "dataset.csv")
TARGET_PATH = os.path.join(config["data_path"]["processed_path"], "variable_grupo.json")

PROMPT = """
<contexto>
{context}

La seccion en la que vas a trabajar será la definicion y descripcion de la variable objetivo.
</contexto>

<seccion>
La seccion en LaTex que vas a crear se conforma de:

Titulo:
Variable Objetivo

Contenido:
La definición y la descripción de la variable de objeto a estudio. este contenido se tiene que basar
en como se comporta en el dataset a estudiar y los conocimientos que tengas.
</seccion>

<entrada>
Variable objetivo del estudio: {target}
Descripcion del contenido de la variable de estudio: {valid_keys}
Base de datos de la poblacion de estudio: {dataset}
</entrada>

<salida>
Tu única tarea es generar el código en LaTeX para esta sección. 
Devuelve un JSON válido que cumpla este esquema:

{{
  "latex_code": "<aquí va el contenido LaTeX como string>"
}}

IMPORTANTE: la seccion y subsecciones (si las hay) deben ser directamente integrable en un documento LaTeX.
</salida>
"""

class TargetAgent(Agent):
    """"""
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv(DF_PATH)
        with open(TARGET_PATH, "r", encoding="utf-8") as f:
            self.target = json.load(f)
        with open(TIME_PATH, "r", encoding="utf-8") as f:
            time_config = json.load(f)
            self.time_variable = time_config["time_variable"]
    
    def generate(self) -> str:
        response = self.call_llm(
            prompt=PROMPT.format(
                context= CONTEXT.format(target=self.target["group_variable"], time=self.time_variable),
                target=self.target["group_variable"],
                valid_keys=self.target["valid_keys"],
                dataset=self.df.sample(n=60).to_string()
            ),
            response_format=LaTexResponse
        )
        return response.latex_code

def generate_target_variable() -> str:
    """"""
    agent = TargetAgent()
    response = agent.generate()
    return response