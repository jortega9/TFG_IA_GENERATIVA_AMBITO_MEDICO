"""Agent that identify the continous numeric variables and make a csv summary.
"""
import configparser
import io
import json
import os
import re
import sys

import pandas as pd
import numpy as np

from typing import List

from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))


from ai.agents.agent import Agent
from ai.phases.etl.descriptive.numeric.prompts import IDENTIFY_WORKFLOW, CONCLUSION_WORKFLOW
from ai.phases.etl.descriptive.numeric.schemas import IdentifySchema, ConclusionSchema

load_dotenv()

SETTINGS_PATH = os.getenv("SETTINGS_PATH")

config = configparser.ConfigParser()

config.read(SETTINGS_PATH)

DF_PATH=os.path.join(config["data_path"]["processed_path"], "dataset.csv")
INFO_PATH=os.path.join(config["data_path"]["processed_path"], "variable_info.json")

OUTPUT_PATH=os.path.join(config["data_path"]["processed_path"], "analisis_estadistico_numerico.csv")

class NumericDescriptiveAgent(Agent):
    
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv(DF_PATH)
        with open(INFO_PATH, "r", encoding="utf-8") as f:
            self.variable_info = json.load(f)
        self.summary = pd.DataFrame(columns=["variable", "n", "media", "std", "mediana", "ric", "rango"])
        
        
    def execute(self) -> dict:
        """Main call to the LLM Agent.

        Returns:
            dict: 
        """
        
        variable_list = []
        
        for var, info in self.variable_info.items():
            if info["type"] == "numerical" and var in self.df.columns:
                variable_list.append(var)
                datos = pd.to_numeric(self.df[var], errors="coerce").dropna()
                
                if datos.empty:
                    continue

                n = len(datos)
                media = round(datos.mean(), 2)
                std = round(datos.std(), 2)
                mediana = round(datos.median(), 2)
                q1 = round(datos.quantile(0.25), 2)
                q3 = round(datos.quantile(0.75), 2)
                ric = round(q3 - q1, 2)
                minimo = round(datos.min(), 2)
                maximo = round(datos.max(), 2)
                rango = f"{minimo}-{maximo}"

                self.summary.loc[len(self.summary)] = [var, n, media, std, mediana, ric, rango]
                
        self.summary.to_csv(OUTPUT_PATH, index=False)
        
        # TODO: Hacer el LLM que hace la conclusion del summary 
        
        return {
            "explanation": "TODO",
            "results": {
                "variables": variable_list,
                "csv_path": OUTPUT_PATH
            }
        }
        
    def descriptive_analysis(self, variables: List[str]) -> None:
        """Make the descriptive analysis.

        Args:
            variables (List[str]): List of numeric continuos variables.
        """
        
        for column in variables:
            
            if column not in self.df.columns:
                continue
            
            col = self.df[column].dropna()
            # Media
            count = col.count()
            mean = round(col.mean(), 2)
            # Desviacion Típica
            std = round(col.std(), 2)
            # Mediana
            median = round(col.median(), 2)
            # Rango intercuartílico
            minimo = round(col.min(), 2)
            maximo = round(col.max(), 2)
            q1 = round(col.quantile(0.25), 2)
            q3 = round(col.quantile(0.75), 2)
            ric = round(q3 - q1, 2)
            rango = f"{minimo}-{maximo}"
            
            nueva_fila = {
                "variable": column,
                "n": count,
                "media": mean,
                "std": std,
                "mediana": median,
                "ric": ric,
                "rango": rango
            }
            
            self.summary = pd.concat([self.summary, pd.DataFrame([nueva_fila])], ignore_index=True)
            
        self.summary.to_csv(OUTPUT_PATH, index=False)