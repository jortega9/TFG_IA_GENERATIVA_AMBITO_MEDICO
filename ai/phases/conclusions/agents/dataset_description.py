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

MASTER_PATH = os.path.join(config["data_path"]["processed_path"], "master.json")
DF_PATH = os.path.join(config["data_path"]["processed_path"], "dataset.csv")

PROMPT = """
<context>
{context}

La seccion en la que vas a trabajar será el analisis del dataset en el que se ha realizado el estudio.
</context>

<seccion>
La seccion en LaTex que vas a crear se conforma de:

Titulo: 
Descripcion del conjunto de datos clinicos

Descripcion:
Una descripcion profunda de las variables analizadas del dataset dado afianzandote del maestro que 
contiene la descripcion de las variables tanto numericas como categoricas.
</seccion>

<entrada>
Descripcion de las variables de la base de datos: {master}
Base de datos de la poblacion de estudio: {dataset}
</entrada>

<salida>
Devuelve únicamente un JSON válido con este formato:

{{
  "latex_code": "<aquí va el contenido en LaTeX como string>"
}}

IMPORTANTE: la seccion y subsecciones (si las hay) deben ser directamente integrable en un documento LaTeX.
</salida>
"""

class DatasetAgent(Agent):
    """"""
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv(DF_PATH)
        with open(GROUP_PATH, "r", encoding="utf-8") as f:
            group_config = json.load(f)
            self.group_variable = group_config["group_variable"]
        with open(TIME_PATH, "r", encoding="utf-8") as f:
            time_config = json.load(f)
            self.time_variable = time_config["time_variable"]
        with open(MASTER_PATH, "r", encoding="utf-8") as f:
            self.master = json.load(f)

    def generate(self) -> str:
        response = self.call_llm(
            prompt=PROMPT.format(
                context= CONTEXT.format(target=self.group_variable, time=self.time_variable),
                master=self.master,
                dataset=self.df.to_string()
            ),
            response_format=LaTexResponse,
            temperature=0.8
        )
        return response.latex_code


def generate_dataset_description() -> str:
    """"""
    agent = DatasetAgent()
    response = agent.generate()
    return response
