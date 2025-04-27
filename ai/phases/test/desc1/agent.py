"""_summary_
"""
import configparser
import io
import json
import os
import re

import pandas as pd
import numpy as np

from ai.agents.agent import Agent
from ai.phases.test.desc1.prompts import CALC_MEDIA, CALC_DESV


from dotenv import load_dotenv
load_dotenv()


SETTINGS_PATH = os.getenv("SETTINGS_PATH")

config = configparser.ConfigParser()

config.read(SETTINGS_PATH)

EXCEL_PATH=os.path.join(config["data_path"]["processed_path"], "BD.xlsx")
MASTER_PATH=os.path.join(config["data_path"]["processed_path"], "master.json")
OUTPUT_PATH=os.path.join(config["data_path"]["processed_path"], "dataset.json")

class TestAgentDesc1(Agent) :
    """_summary_
    """
    
    def __init__(self, system=""):
        super().__init__() 
        
        self.system = system
        self.messages = []
        self.action_re = re.compile(r'^Ejecuta: (\w+): (.*)$') 
        if self.system:
            self.messages.append({"role": "system", "content": system})
        self.df = pd.DataFrame()
        self.master = dict()

        self.known_actions = {
        }
        

    def calc_media_desv_normal(self) -> dict:
        """Calculate mean and standard deviation assuming normal distribution.

        Returns:
            dict: Dictionary with mean and standard deviation.
        """

        ejemplo_input = """
            Pensamiento: Antes de iniciar el análisis, es fundamental cargar los datos clínicos desde el archivo correspondiente para poder trabajar con información válida.
            Ejecuta: read_excel('datos_clinicos_urologia.xlsx')

            Pensamiento: Una vez cargados los datos, es necesario revisar su estructura general para entender qué columnas están disponibles y qué tipo de datos contiene cada una.
            Ejecuta: info_df()

            Pensamiento: Para garantizar la integridad del análisis, se deben eliminar registros corruptos o inconsistentes que puedan introducir ruido en los cálculos estadísticos.
            Ejecuta: drop_corrupt_records()

            Pensamiento: También se deben eliminar duplicados que puedan alterar las medidas de tendencia central y dispersión.
            Ejecuta: drop_duplicates()

            Pensamiento: Una vez que los datos están limpios, se puede explorar una muestra representativa para identificar rápidamente las variables clínicas relevantes.
            Ejecuta: sample_df()

            Pensamiento: Para contextualizar el análisis, se revisarán las descripciones de columnas relacionadas con volumen prostático, PSA total y flujo urinario máximo.
            Ejecuta: view_column_description(['volumen_prostatico', 'psa_total', 'flujo_urinario_max'])

            Pensamiento: Considerando que estas variables tienden a seguir una distribución normal en la mayoría de los pacientes, es adecuado calcular la media y la desviación típica para cada una.
            Ejecuta: ask_question('¿Cuál es la media y la desviación típica de volumen prostático, PSA total y flujo urinario máximo?')

            Pensamiento: Por último, se guarda esta versión limpia y procesada del archivo para su uso en reportes posteriores o modelos estadísticos.
            Ejecuta: save_files_in_processed_data('datos_clinicos_urologia_limpios.xlsx')
            """


        razonamiento_array = [line.strip() for line in ejemplo_input.strip().split("\n") if line.strip()]
        
        return {
            "razonamiento": razonamiento_array,
            "resultado": {
                "media": [{
                    "variable": "Variable1",
                    "valor": 1.20,
                },
                {
                    "variable": "Variable2",
                    "valor": 2.23,
                },
                {
                    "variable": "Variable3",
                    "valor": 3.24,
                }],
                "desviacion_tipica": [{
                    "variable": "Variable1",
                    "valor": 0.66,
                },
                {
                    "variable": "Variable2",
                    "valor": 0.75,
                },
                {
                    "variable": "Variable3",
                    "valor": 0.12,
                }],
            }
        }
    
    def run(self, max_turns) -> dict:
        """
        Run the agent.
        Returns:
            dict: Dictionary with the result.
        """
        return self.calc_media_desv_normal()