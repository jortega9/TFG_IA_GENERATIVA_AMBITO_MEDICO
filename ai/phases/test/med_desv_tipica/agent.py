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
from ai.phases.test.med_desv_tipica.prompts import CALC_MEDIA, CALC_DESV


SETTINGS_PATH = "/home/joort/TFG/TFG_IA_GENERATIVA_AMBITO_MEDICO/ai/config.ini"

config = configparser.ConfigParser()

config.read(SETTINGS_PATH)

EXCEL_PATH=os.path.join(config["data_path"]["processed_path"], "BD.xlsx")
MASTER_PATH=os.path.join(config["data_path"]["processed_path"], "master.json")
OUTPUT_PATH=os.path.join(config["data_path"]["processed_path"], "dataset.json")

class TestAgent(Agent) :
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
            Pensamiento: Antes de realizar el análisis, es crucial verificar que los datos demográficos estén completos y sin valores atípicos significativos.
            Ejecuta: Realiza un análisis exploratorio inicial de las variables demográficas edad, ingresos y tamaño del hogar, identificando valores faltantes y atípicos.

            Pensamiento: Ahora que los datos han sido limpiados y los valores atípicos identificados, procedemos a calcular las estadísticas descriptivas básicas.
            Ejecuta: Calcula la media y la desviación típica para cada una de las variables demográficas: edad, ingresos y tamaño del hogar.

            Pensamiento: La interpretación de estas estadísticas es fundamental para comprender las características poblacionales y tomar decisiones basadas en datos sólidos.
            Ejecuta: Genera gráficos de distribución para edad, ingresos y tamaño del hogar, destacando la media y la desviación típica obtenidas anteriormente.

            Pensamiento: Finalmente, es recomendable comparar estas estadísticas con datos históricos para evaluar posibles cambios o tendencias a lo largo del tiempo.
            Ejecuta: Compara las medias y desviaciones típicas actuales con las registradas en años anteriores y presenta un informe con las conclusiones obtenidas.
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