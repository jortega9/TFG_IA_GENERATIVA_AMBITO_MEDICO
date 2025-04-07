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
from ai.phases.test.executeData.prompts import CALC_MEDIA, CALC_DESV


SETTINGS_PATH = "/home/joort/TFG/TFG_IA_GENERATIVA_AMBITO_MEDICO/ai/config.ini"

config = configparser.ConfigParser()

config.read(SETTINGS_PATH)

EXCEL_PATH=os.path.join(config["data_path"]["processed_path"], "BD.xlsx")
MASTER_PATH=os.path.join(config["data_path"]["processed_path"], "master.json")
OUTPUT_PATH=os.path.join(config["data_path"]["processed_path"], "dataset.json")

class TestAgentExecuteData(Agent) :
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
        

    def execute_data(self) -> dict:
        """Prepare data from DB and Maestro.

        Returns:
            dict: Dictionary with question or OK.
        """

        ejemplo_input = """
        Pensamiento: Antes de iniciar el análisis, es fundamental cargar los datos desde el archivo correspondiente para poder trabajar con ellos.
        Ejecuta: read_excel('demografia_2023.xlsx')

        Pensamiento: Una vez cargados los datos, es necesario revisar su estructura general para entender las columnas disponibles y el tipo de datos que contiene.
        Ejecuta: info_df()

        Pensamiento: Para garantizar la calidad de los datos, se deben eliminar los registros corruptos o con errores que puedan afectar el análisis posterior.
        Ejecuta: drop_corrupt_records()

        Pensamiento: También conviene eliminar posibles duplicados que puedan distorsionar los resultados estadísticos.
        Ejecuta: drop_duplicates()

        Pensamiento: Ahora que los datos están limpios, podemos obtener una muestra para explorar rápidamente las variables de interés.
        Ejecuta: sample_df()

        Pensamiento: Para conocer mejor cada variable, se puede consultar la descripción de las columnas relacionadas con edad, ingresos y tamaño del hogar.
        Ejecuta: view_column_description(['edad', 'ingresos', 'tamano_hogar'])

        Pensamiento: Una vez entendidas las variables clave, se procede a realizar una consulta para obtener promedios y desviaciones estándar de estas variables demográficas.
        Ejecuta: ask_question('¿Cuál es la media y desviación típica de la edad, ingresos y tamaño del hogar?')

        Pensamiento: Por último, se guarda una versión procesada del archivo para su uso en futuras fases del análisis.
        Ejecuta: save_files_in_processed_data('demografia_2023_limpia.xlsx')
        """


        razonamiento_array = [line.strip() for line in ejemplo_input.strip().split("\n") if line.strip()]
        
        return {
            "razonamiento": razonamiento_array,
            "resultado": {
                "isOK": True,
                "message": "Datos procesados correctamente",
            }
        }
    
    def run(self, max_turns) -> dict:
        """
        Run the agent.
        Returns:
            dict: Dictionary with the result.
        """
        return self.execute_data()