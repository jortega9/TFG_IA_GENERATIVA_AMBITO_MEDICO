import configparser
import io
import json
import os
import re

import pandas as pd
import numpy as np

from dotenv import load_dotenv
from ai.agents.agent import Agent
from ai.phases.etl.prepare_data.prompts import AGENT_WORKFLOW1

load_dotenv()

SETTINGS_PATH = os.getenv("SETTINGS_PATH")
config = configparser.ConfigParser()
config.read(SETTINGS_PATH)

EXCEL_PATH = os.path.join(config["data_path"]["raw_path"], "BD.xlsx")
MASTER_PATH = os.path.join(config["data_path"]["processed_path"], "master.json")
OUTPUT_PATH = os.path.join(config["data_path"]["processed_path"], "dataset.csv")


class PrepareDataAgent(Agent):
    """
    Agente para preparar los datos.
    Ahora utiliza la función de tool_calls de OpenAI, esperando respuestas en formato JSON
    con la estructura: {"thought": ..., "action": ..., "parameters": { ... }}.
    """

    def __init__(self, system=""):
        super().__init__()
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": self.system})
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
            "save_files_in_processed_data": self.save_files_in_processed_data,
        }

    def call(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.call_llm(messages=self.messages, temperature=1)
        # Se espera que el resultado sea un JSON válido
        try:
            response = json.loads(result)
        except Exception as e:
            # En caso de error, se usa una estructura por defecto
            response = {"thought": "No se pudo interpretar la respuesta", "action": None, "parameters": {}}
        self.messages.append({"role": "assistant", "content": json.dumps(response)})
        return response

    def execute(self, max_turns=100):
        turn = 0
        next_prompt = AGENT_WORKFLOW1
        while turn < max_turns:
            turn += 1
            response = self.call(next_prompt)
            # Si no se especifica acción, se entiende que se ha finalizado el proceso
            if not response.get("action"):
                print("Respuesta final:", response.get("final", "El proceso ha finalizado."))
                return
            print("Pensamiento: ", response["thought"])
            action = response["action"]
            parameters = response.get("parameters", {})
            if action not in self.known_actions:
                raise Exception(f"Acción desconocida: {action}")
            print(f"-- Ejecutando {action} con parámetros: {parameters}")
            observation = self.known_actions[action](**parameters)
            input("Pulsa cualquier tecla para continuar...")
            print("Observación:", observation)
            next_prompt = f"Observación: {observation}"

    def standardize_name(self, name: str) -> str:
        """Estandariza un nombre: minúsculas, reemplaza espacios por guiones bajos y elimina caracteres no alfanuméricos."""
        name = name.lower()
        name = re.sub(r"[^\w\s]", "", name)
        name = re.sub(r"\s+", "_", name.strip())
        return name

    def read_excel(self):
        """Carga el archivo Excel en un DataFrame."""
        self.df = pd.read_excel(EXCEL_PATH, header=1, sheet_name=0, dtype=str)
        self.df.columns = [self.standardize_name(col) for col in self.df.columns]
        return "El Excel se ha cargado en un DataFrame."

    def open_master(self):
        """Carga el diccionario maestro desde un JSON."""
        with open(MASTER_PATH, "r", encoding="utf-8") as f:
            master_data = json.load(f)
        self.master = {
            self.standardize_name(key): value
            for key, value in master_data.items()
        }
        print(self.master)
        return "El maestro se ha cargado y transformado en un diccionario."


    def sample_df(self, n=10):
        """Devuelve una muestra de n registros del DataFrame en formato JSON."""
        return self.df.sample(n=n).to_json()

    def info_df(self):
        """Devuelve información general del DataFrame."""
        buffer = io.StringIO()
        self.df.info(buf=buffer)
        return buffer.getvalue()

    def view_column_description(self, column: str):
        """Devuelve el significado de una columna usando el maestro."""
        result = self.master.get(column.strip())
        if result:
            return result
        else:
            columns = list(self.master.keys())
            return f"No se ha encontrado la columna: \"{column}\". Columnas disponibles: {columns}"

    def drop_column(self, column: str):
        """Elimina una columna específica del DataFrame."""
        column = column.strip()
        if column in self.df.columns:
            self.df.drop(columns=[column], inplace=True)
            return f"La columna {column} ha sido eliminada."
        return f"La columna {column} no existe en el DataFrame."

    def ask_question(self, question: str):
        """Realiza una pregunta al usuario sobre el dataset o maestro."""
        response = input(f"Pregunta: {question}\nRespuesta: ")
        return response

    def add_to_master(self, column: str, description: str):
        """Añade una nueva variable al maestro con su descripción."""
        column = column.strip()
        description = description.strip()
        self.master[column] = {"descripcion": description, "valores": {}}
        return f"La columna {column} ha sido añadida al maestro con la descripción: {description}."

    def update_master_description(self, column: str, new_description: str):
        """Actualiza la descripción de una variable en el maestro."""
        column = column.strip()
        new_description = new_description.strip()
        if column in self.master:
            self.master[column]["descripcion"] = new_description
            return f"La descripción de {column} ha sido actualizada a: {new_description}."
        return f"La columna {column} no existe en el maestro."

    def drop_corrupt_records(self):
        """Elimina registros corruptos (vacíos)."""
        initial_rows = len(self.df)
        self.df.dropna(inplace=True, how="all")
        removed_rows = initial_rows - len(self.df)
        return f"Se han eliminado {removed_rows} registros vacíos."

    def drop_corrupt_columns(self):
        """Elimina columnas con alto porcentaje de valores faltantes."""
        initial_columns = len(self.df.columns)
        self.df.dropna(axis=1, thresh=int(0.9 * len(self.df)), inplace=True)
        removed_columns = initial_columns - len(self.df.columns)
        return f"Se han eliminado {removed_columns} columnas con un 90% de registros vacíos."

    def drop_duplicates(self):
        """Elimina registros duplicados."""
        initial_rows = len(self.df)
        self.df.drop_duplicates(inplace=True)
        removed_rows = initial_rows - len(self.df)
        return f"Se han eliminado {removed_rows} registros duplicados."

    def save_files_in_processed_data(self):
        """Guarda el DataFrame y el maestro en archivos de datos procesados."""
        self.df.to_csv(OUTPUT_PATH, index=False)
        with open(MASTER_PATH, "w", encoding="utf-8") as file:
            json.dump(self.master, file, indent=4)
        return "Se han guardado exitosamente los archivos."
