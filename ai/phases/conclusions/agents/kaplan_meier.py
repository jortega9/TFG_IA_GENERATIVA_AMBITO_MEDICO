import configparser
import json
import os
import sys

import pandas as pd
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

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

Tu trabajo es analizar clinicamente la curva de supervivencia Kaplan Meier estratificada que se te proporciona.
La curva es de la variable objetivo con la variable de seguimiento añadiendole la mascara de la siguiente variable : {var}
Se te van a dar tres herramientas: 
-El path a la imagen que contiene la grafica de la curva que solo la usaras para mostrarla
-La curva en formato csv, que usaras para analizarla.
</contexto>

<seccion>
tu trabajo es crear una **SUBSECCION** perteneciente a una subseccion ya hecha.


Subsección:
Utiliza subsection con: Curva de supervivencia Kaplan-Meier estratificada de {var}

Imagen: 
Adjuntaras la imagen de este path {image} y la mostraras con un encabezado 

Importante: NO uses comandos que cambien el tipo o tamaño de fuente como \\small, \\textsf, \\tt, etc.

Conclusiones:
Analiza la curva dada en formato csv y saca conclusiones clinicas sobre la misma curva,
es importante que se haga este analisis a fondo y a profundidad. 
NO INCLUYAS EN LAS CONCLUSIONES NINGUN NOMBRE DE PATH.
</seccion>

<entrada>
Analizaras la curva dada en este CSV: {csv}
</entrada>

<salida>
Tu única tarea es generar el código en LaTeX para esta SUBSECCION. 
Devuelve un JSON válido que cumpla este esquema:

{{
  "latex_code": "<aquí va el contenido de la SUBSECCION en LaTeX como string>"
}}

IMPORTANTE: la subseccion debe ser directamente integrable en un documento LaTeX.
</salida>
"""

class KaplanMeierAgent(Agent):
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

        df_filtered = self.df_var[(self.df_var['tipo'].isin(['categórica']))]
        var_list = df_filtered['variable'].to_list()
        results = []

        def process_var(var):
            image_path = os.path.join(IMAGE_DIR, f"{var}_kaplan_meier_plot.png")
            csv_path = os.path.join(INFO_DIR, f"{var}_survival_curve.csv")
            summary_path = os.path.join(INFO_DIR, f"{var}_median_summary.csv")

            if not (os.path.exists(image_path) and os.path.exists(csv_path) and os.path.exists(summary_path)):
                return ""

            return self.call(var=var, image=image_path, csv=csv_path, summary=summary_path)

        with ThreadPoolExecutor() as executor:
            results = list(executor.map(process_var, var_list))

        return "".join(results)

        
    
    def call(self, var:str, image:str, csv:str, summary:str) -> str:
        response = self.call_llm(
            prompt=PROMPT.format(
                context= CONTEXT.format(target=self.group_variable, time=self.time_variable),
                var=var,
                image=image,
                csv=csv,
                summary=summary,
            ),
            response_format=LaTexResponse,
            temperature=0.8
        )
        return response.latex_code

def generate_kaplan_meier() -> str:
    """"""
    agent = KaplanMeierAgent()
    response = agent.generate()
    return response