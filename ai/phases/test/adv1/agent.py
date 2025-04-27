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

class TestAgentAdv1(Agent) :
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
    Pensamiento: Primero es esencial cargar los datos clínicos, incluyendo los resultados inmunohistoquímicos y otras variables clínicas, desde el archivo.
    Ejecuta: read_excel('BD.xlsx')

    Pensamiento: Se debe revisar la estructura y tipos de datos para identificar claramente las variables inmunohistoquímicas y clínicas disponibles.
    Ejecuta: info_df()

    Pensamiento: Limpiar los datos eliminando registros corruptos para asegurar validez en el análisis estadístico posterior.
    Ejecuta: drop_corrupt_records()

    Pensamiento: Eliminar registros duplicados que podrían afectar negativamente la precisión de los tests estadísticos.
    Ejecuta: drop_duplicates()

    Pensamiento: Revisar una muestra de los datos limpios para entender la relación potencial entre variables inmunohistoquímicas y otras variables clínicas.
    Ejecuta: sample_df()

    Pensamiento: Confirmar cuáles son las variables categóricas y continuas relevantes, especialmente identificando claramente las variables inmunohistoquímicas que suelen ser categóricas.
    Ejecuta: view_column_description(['resultado_inmunohistoquimico', 'variable_clinica_1', 'variable_clinica_2'])

    Pensamiento: Para las variables continuas se debe aplicar la prueba t de Student para determinar diferencias significativas según el resultado inmunohistoquímico.
    Ejecuta: ask_question('¿Qué variables continuas muestran diferencias significativas según los resultados inmunohistoquímicos aplicando t de Student?')

    Pensamiento: Para variables categóricas con suficientes datos, aplicar el Test de Chi cuadrado de Pearson.
    Ejecuta: ask_question('¿Qué variables categóricas están significativamente asociadas a los resultados inmunohistoquímicos según el Test Chi cuadrado de Pearson?')

    Pensamiento: Para variables categóricas con conteos bajos o grupos pequeños, utilizar el Test exacto de Fisher.
    Ejecuta: ask_question('¿Qué variables categóricas presentan asociaciones significativas con resultados inmunohistoquímicos al aplicar el Test exacto de Fisher?')

    Pensamiento: Finalmente, guardar los datos procesados y analizados en un nuevo archivo para futuras referencias o reportes.
    Ejecuta: save_files_in_processed_data('BD_limpio.xlsx')
"""



        razonamiento_array = [line.strip() for line in ejemplo_input.strip().split("\n") if line.strip()]
        
        return {
    "razonamiento": razonamiento_array,
    "resultado": {
        "t_student": [
            {
                "variable": "volumen_prostatico",
                "valor": 0.034,
            },
            {
                "variable": "psa_total",
                "valor": 0.012,
            },
            {
                "variable": "flujo_urinario_max",
                "valor": 0.245,
            }
        ],
        "chi_cuadrado": [
            {
                "variable": "antecedentes_familiares",
                "valor": 0.045,
            },
            {
                "variable": "presencia_sintomas_urinarios",
                "valor": 0.068,
            }
        ],
        "fisher_exacto": [
            {
                "variable": "tipo_lesion",
                "valor": 0.007,
            },
            {
                "variable": "tratamiento_previo",
                "valor": 0.102,
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