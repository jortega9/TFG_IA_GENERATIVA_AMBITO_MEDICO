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

class TestAgentAdv3(Agent) :
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
        

    def analiz_curvas_supervivencia(self) -> dict:
        """Calculate correlation with t student, test chi y test fisher.

        Returns:
            dict: Dictionary with mean and standard deviation.
        """

        ejemplo_input = """
    Pensamiento: Inicialmente, cargar los datos clínicos incluyendo tiempos de supervivencia global y cáncer específica desde el archivo.
    Ejecuta: read_excel('datos_supervivencia_global_especifica.xlsx')

    Pensamiento: Revisar la estructura general y tipos de datos para asegurar que las variables relacionadas con supervivencia están claramente definidas.
    Ejecuta: info_df()

    Pensamiento: Limpiar el conjunto de datos eliminando registros corruptos o incompletos para garantizar precisión en los análisis posteriores.
    Ejecuta: drop_corrupt_records()

    Pensamiento: Eliminar posibles duplicados para evitar sesgos en los análisis de supervivencia.
    Ejecuta: drop_duplicates()

    Pensamiento: Explorar una muestra representativa de los datos para confirmar que la limpieza fue efectiva y que las variables necesarias están correctamente disponibles.
    Ejecuta: sample_df()

    Pensamiento: Confirmar que las variables de tiempo de supervivencia global y cáncer específica, así como el estado del evento (muerte, recaída), están correctamente descritas.
    Ejecuta: view_column_description(['tiempo_supervivencia_global', 'evento_global', 'tiempo_supervivencia_cancer_especifica', 'evento_cancer_especifico'])

    Pensamiento: Aplicar análisis de supervivencia mediante curvas de Kaplan-Meier tanto para supervivencia global como cáncer específica.
    Ejecuta: ask_question('¿Cuáles son las curvas estimadas de supervivencia global y cáncer específica utilizando Kaplan-Meier?')

    Pensamiento: Finalmente, guardar los resultados del análisis en un archivo para futuras referencias o generación de reportes.
    Ejecuta: save_files_in_processed_data('datos_supervivencia_global_especifica_analizados.xlsx')
    """




        razonamiento_array = [line.strip() for line in ejemplo_input.strip().split("\n") if line.strip()]
        
        return {
            "razonamiento": razonamiento_array,
            "resultado": {
                "supGlobal": [
                    {
                        "variable": "12 MESES",
                        "valor": 0.92
                    },
                    {
                        "variable": "24 MESES",
                        "valor": 0.84
                    },
                    {
                        "variable": "36 MESES",
                        "valor": 0.76
                    }
                ],
                "supEspecifica": [
                    {
                        "variable": "12 MESES",
                        "valor": 0.97
                    },
                    {
                        "variable": "24 MESES",
                        "valor": 0.91
                    },
                    {
                        "variable": "36 MESES",
                        "valor": 0.85
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
        return self.analiz_curvas_supervivencia()