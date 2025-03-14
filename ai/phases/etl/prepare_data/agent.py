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
from ai.phases.etl.prepare_data.prompts import AGENT_WORKFLOW

SETTINGS_PATH = "/home/joort/TFG/TFG_IA_GENERATIVA_AMBITO_MEDICO/ai/config.ini"

config = configparser.ConfigParser()

config.read(SETTINGS_PATH)

EXCEL_PATH=os.path.join(config["data_path"]["raw_path"], "BD.xlsx")
MASTER_PATH=os.path.join(config["data_path"]["processed_path"], "master.json")
OUTPUT_PATH=os.path.join(config["data_path"]["processed_path"], "dataset.json")

class PrepareDataAgent(Agent) :
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
            "read_excel": self.read_excel,
            "open_master": self.open_master,
            "sample_df": self.sample_df,
            "info_df": self.info_df,
            "view_column_description": self.view_column_description,
            "drop_column": self.drop_column,
            "ask_question": self.ask_question,
            "add_to_master": self.add_to_master,
            "update_master_description": self.update_master_description,
            "drop_corrupt_records": self.drop_corrupt_records,
            "drop_corrupt_columns": self.drop_corrupt_columns,
            "drop_duplicates": self.drop_duplicates,
        }
        
    
    def call(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.call_llm(messages=self.messages, temperature=0.3)
        self.messages.append({"role": "assistant", "content": result})
        return result
    

    def execute(self, max_turns=100) -> list:
        i = 0
        next_prompt = AGENT_WORKFLOW.format()
        all_results = []
        while i < max_turns:
            i += 1
            result = self.call(message=next_prompt)
            all_results.append(result)
            print("result: " + result)
            actions = [
                self.action_re.match(a)
                for a in result.split('\n')
                if self.action_re.match(a)
            ]
            print("actions: ", actions)
            if actions:
                action, action_input = actions[0].groups()
                if action not in self.known_actions:
                    raise Exception("Unknown action: {}: {}".format(action, action_input))
                print("-- running {} {}".format(action, action_input))
                input("texto")
                print(action_input)
                if action_input and len(action_input.strip()) > 1:
                    observation = self.known_actions[action](action_input)
                else:
                    observation = self.known_actions[action]()
                print("Observacion:\n", observation)
                next_prompt = "Observacion: {}".format(observation)
            else:
                break
        return all_results

    def read_excel(self):
        """Carga el archivo Excel en un DataFrame."""
        self.df = pd.read_excel(EXCEL_PATH, header=1, sheet_name=0, dtype=str)
        return "El Excel se ha cargado en un DataFrame."

    def open_master(self):
        """Carga el diccionario maestro desde un JSON y lo transforma en un diccionario con claves los nombres de las columnas."""
        with open(MASTER_PATH, "r", encoding="utf-8") as f:
            master_data = json.load(f)

        self.master = {
            entry["column_name"]: entry["column_info"]
            for entry in master_data.get("column", []) 
        }

        return "El maestro se ha cargado y transformado en un diccionario."

    def sample_df(self, n=10):
        """Muestra una muestra aleatoria de n registros del DataFrame."""
        return self.df.sample(n=n)

    def info_df(self):
        """Devuelve información general del DataFrame."""
        buffer = io.StringIO()
        self.df.info(buf=buffer)
        return buffer.getvalue()

    def view_column_description(self, column: str):
        """Devuelve el significado de una columna concreta usando el maestro."""
        result = self.master.get(column.strip())
        if result :
            return result
        else :
            columns = self.master.keys()
            return f"No se ha encontrado la columna: \"{column}\"\n¿Seguro que lo has escrito bien?\nEstas son las columnas disponibles: {columns}" 

    def drop_column(self, column: str):
        """Elimina una columna específica del DataFrame."""
        column=column.strip()
        if column in self.df.columns:
            self.df.drop(columns=[column], inplace=True)
            return f"La columna {column} ha sido eliminada."
        return f"La columna {column} no existe en el DataFrame."

    def ask_question(self, question: str):
        """Realiza una pregunta al usuario sobre el dataset o el maestro."""
        response = input(f"Pregunta al usuario: {question}")
        return response

    def add_to_master(self, column: str, description: str):
        """Añade una nueva variable al maestro con la descripción proporcionada."""
        column=column.strip()
        description=description.strip()
        self.master[column] = {"descripcion": description, "valores": {}}
        return f"La columna {column} ha sido añadida al maestro con la descripción: {description}."

    def update_master_description(self, column: str, new_description: str):
        """Actualiza la descripción de una variable en el maestro."""
        column=column.strip()
        new_description=new_description.strip()
        if column in self.master:
            self.master[column]["descripcion"] = new_description
            return f"La descripción de {column} ha sido actualizada a: {new_description}."
        return f"La columna {column} no existe en el maestro."

    def drop_corrupt_records(self):
        """Elimina registros corruptos con valores vacíos o inconsistentes."""
        initial_rows = len(self.df)
        self.df.dropna(inplace=True, how="all")
        removed_rows = initial_rows - len(self.df)
        return f"Se han eliminado {removed_rows} registros vacíos."

    def drop_corrupt_columns(self):
        """Elimina columnas con un alto porcentaje de valores faltantes."""
        initial_columns = len(self.df.columns)
        self.df.dropna(axis=1, thresh=int(0.9 * len(self.df)), inplace=True)
        removed_columns = initial_columns - len(self.df.columns)
        return f"Se han eliminado {removed_columns} columnas con un 90% de registros vacíos."

    def drop_duplicates(self):
        """Elimina registros duplicados del DataFrame."""
        initial_rows = len(self.df)
        self.df.drop_duplicates(inplace=True)
        removed_rows = initial_rows - len(self.df)
        return f"Se han eliminado {removed_rows} registros duplicados."
    

