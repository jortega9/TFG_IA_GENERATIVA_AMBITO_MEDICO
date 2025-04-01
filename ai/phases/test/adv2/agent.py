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


SETTINGS_PATH = "/home/joort/TFG/TFG_IA_GENERATIVA_AMBITO_MEDICO/ai/config.ini"

config = configparser.ConfigParser()

config.read(SETTINGS_PATH)

EXCEL_PATH=os.path.join(config["data_path"]["processed_path"], "BD.xlsx")
MASTER_PATH=os.path.join(config["data_path"]["processed_path"], "master.json")
OUTPUT_PATH=os.path.join(config["data_path"]["processed_path"], "dataset.json")

class TestAgentAdv2(Agent) :
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
        

    def calc_prob_recaida(self) -> dict:
        """Calculate correlation with t student, test chi y test fisher.

        Returns:
            dict: Dictionary with mean and standard deviation.
        """

        ejemplo_input = """
            Pensamiento: Inicialmente, se deben cargar los datos clínicos que incluyen información sobre recaída bioquímica y el tiempo de seguimiento.
            Ejecuta: read_excel('datos_recaida_bioquimica.xlsx')

            Pensamiento: Revisar la estructura de los datos para identificar claramente las variables necesarias como tiempo hasta recaída y estatus de recaída.
            Ejecuta: info_df()

            Pensamiento: Es fundamental limpiar los datos, eliminando registros corruptos o con información incompleta para obtener resultados confiables en el análisis de supervivencia.
            Ejecuta: drop_corrupt_records()

            Pensamiento: También se deben eliminar registros duplicados que puedan afectar la precisión del análisis estadístico.
            Ejecuta: drop_duplicates()

            Pensamiento: Observar una muestra aleatoria de los datos limpios para asegurar que están correctamente preparados para el análisis.
            Ejecuta: sample_df()

            Pensamiento: Confirmar que las variables relacionadas con el tiempo hasta recaída y el estado del evento están correctamente descritas.
            Ejecuta: view_column_description(['tiempo_recaida', 'evento_recaida'])

            Pensamiento: Realizar el análisis de supervivencia utilizando curvas de Kaplan-Meier para estimar la probabilidad de recaída bioquímica en función del tiempo.
            Ejecuta: ask_question('¿Cuál es la probabilidad estimada de recaída bioquímica en función del tiempo utilizando curvas de Kaplan-Meier?')

            Pensamiento: Finalmente, guardar el conjunto de datos analizados y procesados para futuros reportes y análisis.
            Ejecuta: save_files_in_processed_data('datos_recaida_bioquimica_supervivencia.xlsx')
        """




        razonamiento_array = [line.strip() for line in ejemplo_input.strip().split("\n") if line.strip()]
        
        return {
            "razonamiento": razonamiento_array,
            "resultado": {
                "recaida": [
                    {
                        "variable": "12 meses",
                        "valor": 0.95
                    },
                    {
                        "variable": "24 meses",
                        "valor": 0.87
                    },
                    {
                        "variable": "36 meses",
                        "valor": 0.78
                    },
                    {
                        "variable": "48 meses",
                        "valor": 0.69
                    },
                    {
                        "variable": "60 meses",
                        "valor": 0.61
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
        return self.calc_prob_recaida()