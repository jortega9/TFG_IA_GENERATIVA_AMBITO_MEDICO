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
from ai.phases.test.desc3.prompts import CALC_MEDIA, CALC_DESV


from dotenv import load_dotenv
load_dotenv()


SETTINGS_PATH = os.getenv("SETTINGS_PATH")

config = configparser.ConfigParser()

config.read(SETTINGS_PATH)

EXCEL_PATH=os.path.join(config["data_path"]["processed_path"], "BD.xlsx")
MASTER_PATH=os.path.join(config["data_path"]["processed_path"], "master.json")
OUTPUT_PATH=os.path.join(config["data_path"]["processed_path"], "dataset.json")

class TestAgentDesc3(Agent) :
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
        

    def calc_porcentajes_frecuencias(self) -> dict:
        """Calculate mean and standard deviation assuming normal distribution.

        Returns:
            dict: Dictionary with mean and standard deviation.
        """

        ejemplo_input = """
        Pensamiento: Antes de comenzar el análisis, es necesario cargar el archivo con los datos clínicos de pacientes para trabajar con variables cualitativas.
        Ejecuta: read_excel('DB.xlsx')

        Pensamiento: Para asegurar la calidad del análisis, se revisa la estructura general del archivo para verificar que las variables estén correctamente tipadas y no haya inconsistencias.
        Ejecuta: info_df()

        Pensamiento: Eliminamos registros corruptos que puedan generar errores o afectar la validez de los cálculos estadísticos.
        Ejecuta: drop_corrupt_records()

        Pensamiento: También se eliminan duplicados que puedan inflar artificialmente las frecuencias de ciertas categorías.
        Ejecuta: drop_duplicates()

        Pensamiento: Para tener una primera idea de los valores presentes en las variables cualitativas, se obtiene una muestra de los datos.
        Ejecuta: sample_df()

        Pensamiento: Se revisan las descripciones de variables cualitativas como diagnóstico de HPB, presencia de síntomas, uso de medicamentos y antecedentes familiares.
        Ejecuta: view_column_description(['diagnostico_hpb', 'psa_alto', 'nicturia', 'tratamiento_actual'])

        Pensamiento: Ahora se procede a calcular las frecuencias absolutas y los porcentajes con su intervalo de confianza al 95% para cada una de las variables cualitativas seleccionadas.
        Ejecuta: ask_question('¿Cuáles son las frecuencias absolutas y los porcentajes con IC95% para las variables: diagnóstico de HPB, PSA alto, nicturia y tratamiento actual?')

        Pensamiento: Finalmente, se guarda esta versión limpia y validada del archivo para su uso en futuras fases del estudio clínico.
        Ejecuta: save_files_in_processed_data('DB_limpios.xlsx')
        """


        razonamiento_array = [line.strip() for line in ejemplo_input.strip().split("\n") if line.strip()]
        
        return {
            "razonamiento": razonamiento_array,
            "resultado": {
                "porcentajes": [
                    {
                        "variable": "Pacientes con Hiperplasia Prostática Benigna (HPB)",
                        "valor": "62.5%"
                    },
                    {
                        "variable": "Pacientes con PSA elevado (>4 ng/ml)",
                        "valor": "28.4%"
                    },
                    {
                        "variable": "Pacientes con síntomas urinarios severos",
                        "valor": "15.7%"
                    }
                ],
                "frecuencias": [
                    {
                        "variable": "Uso de Alfa-bloqueantes",
                        "valor": 142
                    },
                    {
                        "variable": "Diagnóstico confirmado de Cáncer de Próstata",
                        "valor": 38
                    },
                    {
                        "variable": "Pacientes que reportan nicturia frecuente",
                        "valor": 97
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
        return self.calc_porcentajes_frecuencias()