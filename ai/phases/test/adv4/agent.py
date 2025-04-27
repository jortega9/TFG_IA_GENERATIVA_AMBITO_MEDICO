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

class TestAgentAdv4(Agent) :
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
        

    def calc_correlacion_resultados(self) -> dict:
        """Calculate correlation with t student, test chi y test fisher.

        Returns:
            dict: Dictionary with mean and standard deviation.
        """

        ejemplo_input = """
            Pensamiento: Primero es esencial cargar los datos clínicos, analíticos e histológicos desde el archivo para iniciar el análisis de recaídas.
            Ejecuta: read_excel('BD_recaidas.xlsx')

            Pensamiento: Revisar la estructura y tipos de datos para identificar correctamente las variables relevantes en el análisis de supervivencia.
            Ejecuta: info_df()

            Pensamiento: Limpiar los datos eliminando registros corruptos o incompletos que podrían comprometer la validez del análisis.
            Ejecuta: drop_corrupt_records()

            Pensamiento: Eliminar registros duplicados que puedan sesgar los resultados del modelo de supervivencia.
            Ejecuta: drop_duplicates()

            Pensamiento: Visualizar una muestra de los datos para comprender mejor la distribución de eventos de recaída y otras variables asociadas.
            Ejecuta: sample_df()

            Pensamiento: Confirmar cuáles variables son cualitativas (para prueba Logrank) y cuáles son cuantitativas (para el modelo de Cox).
            Ejecuta: view_column_description(['recaida', 'variable_clinica', 'variable_analitica', 'variable_histologica'])

            Pensamiento: Para las variables cualitativas, aplicar la prueba Logrank y evaluar si existen diferencias significativas en el tiempo hasta la recaída.
            Ejecuta: ask_question('¿Qué variables cualitativas están significativamente asociadas al riesgo de recaída según la prueba Logrank?')

            Pensamiento: Para las variables cuantitativas, ajustar un modelo de riesgos proporcionales de Cox para identificar predictores significativos de recaída.
            Ejecuta: ask_question('¿Qué variables cuantitativas influyen significativamente en el riesgo de recaída según el modelo de Cox?')

            Pensamiento: Guardar los datos procesados y resultados del análisis en un nuevo archivo para futuras consultas o informes clínicos.
            Ejecuta: save_files_in_processed_data('BD_recaidas_limpio.xlsx')
        """




        razonamiento_array = [line.strip() for line in ejemplo_input.strip().split("\n") if line.strip()]
        
        return {
            "razonamiento": razonamiento_array,
            "resultado": {
                "logrank": [
                    {
                        "variable": "grado_diferenciacion_tumoral",
                        "valor": 0.021,
                    },
                    {
                        "variable": "estado_margen_quirurgico",
                        "valor": 0.043,
                    },
                    {
                        "variable": "presencia_invasion_vascular",
                        "valor": 0.189,
                    }
                ],
                "cox": [
                    {
                        "variable": "nivel_pcr",
                        "valor": 0.009,
                    },
                    {
                        "variable": "edad_diagnostico",
                        "valor": 0.031,
                    },
                    {
                        "variable": "recuento_leucocitos",
                        "valor": 0.276,
                    }
                ]
            }
        }


    
    def run(self, max_turns) -> dict:
        """
        Run the agent.
        Returns:
            dict: Dictionary with the result.
        """
        return self.calc_correlacion_resultados()