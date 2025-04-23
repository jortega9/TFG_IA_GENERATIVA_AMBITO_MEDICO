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

VARIABLE_PATH = os.path.join(config["data_path"]["processed_path"], "variables_significativas_totales.csv")
IMAGE_DIR = os.path.join(config["data_path"]["processed_path"], "kaplan_meier")
INFO_DIR = os.path.join(config["data_path"]["processed_path"], "kaplan_meier_csv")

PROMPT = """
<contexto>
{context}

Tu trabajo es analizar clinicamente la curva de supervivencia Kaplan Meier que se te proporciona.
La curva es de la variable objetivo con la variable de seguimiento.
Se te van a dar tres herramientas: 
-El path a la imagen que contiene la grafica de la curva que solo la usaras para mostrarla
-La curva en formato csv, que usaras para analizarla.
</contexto>

<seccion>
La seccion en LaTex que vas a crear se conforma de:

Titulo:
Analisis de curvas de supervivencia Kaplan-Meier

Imagen: 
Adjuntaras la imagen de este path {image} y la mostraras con un encabezado 

Conclusiones:
Analiza la curva dada en formato csv y saca conclusiones clinicas sobre la misma curva,
es importante que se haga este analisis a fondo y a profundidad. 
</seccion>

<entrada>
Analizaras la curva dada en este CSV: {csv}
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

class KaplanMeierSummaryAgent(Agent):
    """"""
    def __init__(self):
        super().__init__()
        try:
            self.df_var = pd.read_csv(VARIABLE_PATH)
        except Exception:
            self.df_var = None
        with open(MASTER_PATH, "r", encoding="utf-8") as f:
            self.master = json.load(f)
        with open(GROUP_PATH, "r", encoding="utf-8") as f:
            group_config = json.load(f)
            self.group_variable = group_config["group_variable"]
        with open(TIME_PATH, "r", encoding="utf-8") as f:
            time_config = json.load(f)
            self.time_variable = time_config["time_variable"]
    
    def generate(self) -> str:
        if self.df_var is None:
            return ""
        image_path = os.path.join(IMAGE_DIR, "kaplan_meier_plot.png")
        csv_path = os.path.join(INFO_DIR, "survival_curve.csv")
        summary_path = os.path.join(INFO_DIR, "median_summary.csv")
        """
        df_filtered = self.df_var[(self.df_var['tipo'].isin(['categórica']))]
        var_list = df_filtered['variable'].to_list()
        """
        response = self.call(image=image_path, csv=csv_path, summary=summary_path)
        return response
        
    
    def call(self, image:str, csv:str, summary:str) -> str:
        response = self.call_llm(
            prompt=PROMPT.format(
                context= CONTEXT.format(target=self.group_variable, time=self.time_variable),
                image=image,
                csv=csv,
                summary=summary,
            ),
            response_format=LaTexResponse,
            temperature=0.8
        )
        return response.latex_code

def generate_kaplan_meier_summary() -> str:
    """"""
    agent = KaplanMeierSummaryAgent()
    response = agent.generate()
    return response