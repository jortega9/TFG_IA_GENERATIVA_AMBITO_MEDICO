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
from ai.phases.test.desc2.prompts import CALC_MEDIA, CALC_DESV


from dotenv import load_dotenv
load_dotenv()


SETTINGS_PATH = os.getenv("SETTINGS_PATH")

config = configparser.ConfigParser()

config.read(SETTINGS_PATH)

EXCEL_PATH=os.path.join(config["data_path"]["processed_path"], "BD.xlsx")
MASTER_PATH=os.path.join(config["data_path"]["processed_path"], "master.json")
OUTPUT_PATH=os.path.join(config["data_path"]["processed_path"], "dataset.json")

class TestAgentDesc2(Agent) :
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
        

    def calc_mediana_rangoI(self) -> dict:
        """Calculate mean and standard deviation assuming normal distribution.

        Returns:
            dict: Dictionary with mean and standard deviation.
        """

        ejemplo_input = """
            Pensamiento: Antes de iniciar el análisis, es fundamental cargar los datos desde el archivo correspondiente para garantizar que se dispone de la información necesaria.
            Ejecuta: read_excel('DB.xlsx')

            Pensamiento: Una vez cargados los datos, es importante revisar su estructura general para conocer las columnas disponibles y el tipo de variables que contiene.
            Ejecuta: info_df()

            Pensamiento: Para asegurar la calidad del análisis, se deben eliminar los registros corruptos o con errores que puedan alterar los resultados estadísticos.
            Ejecuta: drop_corrupt_records()

            Pensamiento: También es recomendable eliminar registros duplicados que puedan distorsionar los cálculos de dispersión y tendencia central.
            Ejecuta: drop_duplicates()

            Pensamiento: Ahora que los datos están limpios, se puede tomar una muestra aleatoria para explorar rápidamente las variables clínicas de interés.
            Ejecuta: sample_df()

            Pensamiento: Para profundizar en el análisis, conviene revisar la descripción de las columnas relacionadas con variables clínicas relevantes como volumen prostático, PSA total y flujo urinario máximo.
            Ejecuta: view_column_description(['volumen_prostatico', 'psa_total', 'flujo_urinario_max'])

            Pensamiento: Dado que estas variables pueden no seguir una distribución normal, es preferible usar estadísticas robustas como la mediana y el rango intercuartílico en lugar de la media y desviación estándar.
            Ejecuta: ask_question('¿Cuál es la mediana y el rango intercuartílico de volumen prostático, PSA total y flujo urinario máximo?')

            Pensamiento: Para futuras referencias o análisis comparativos, es útil guardar esta versión limpia y estructurada del archivo.
            Ejecuta: save_files_in_processed_data('DB_limpio.xlsx')
            """


        razonamiento_array = [line.strip() for line in ejemplo_input.strip().split("\n") if line.strip()]
        
        return {
            "razonamiento": razonamiento_array,
            "resultado": {
                "mediana": [
                {
                    "variable": "Volumen Prostático (ml)",
                    "valor": 45,
                },
                {
                    "variable": "PSA Total (ng/ml)",
                    "valor": 4.2,
                },
                {
                    "variable": "Flujo Urinario Máximo (ml/s)",
                    "valor": 12.5,
                }
                ],
                "rangoI": [
                    {
                        "variable": "Volumen Prostático (ml)",
                        "valor": 18,
                    },
                    {
                        "variable": "PSA Total (ng/ml)",
                        "valor": 2.1,
                    },
                    {
                        "variable": "Flujo Urinario Máximo (ml/s)",
                        "valor": 6.4,
                    }
                ],
            }
        }
    
    def run(self, max_turns) -> dict:
        """
        Run the agent.
        Returns:
            dict: Dictionary with the result.
        """
        return self.calc_mediana_rangoI()