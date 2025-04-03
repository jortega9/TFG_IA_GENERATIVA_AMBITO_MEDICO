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

MASTER_PATH=os.path.join(config["data_path"]["processed_path"], "master.json")
DF_PATH=os.path.join(config["data_path"]["processed_path"], "dataset.csv")

OUTPUT_PATH=os.path.join(config["data_path"]["processed_path"], "analisis_estadistico_numerico.csv")

class NumericDescriptiveAgent(Agent):
    
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv(DF_PATH)
        with open(MASTER_PATH, "r", encoding="utf-8") as f:
            self.master = json.load(f)
        self.summary = pd.DataFrame(columns=["variable", "n", "media", "std", "mediana", "ric", "rango"])
        
        
    def execute(self) -> dict:
        """Main call to the LLM Agent.

        Returns:
            dict: 
        """
        identify_variable = self.call_llm(
            prompt=IDENTIFY_WORKFLOW.format(
                sample=self.df.sample(n=20).to_string(),
                master=json.dumps(self.master)   
            ), 
            response_format=IdentifySchema,
            temperature=0
        )
        print(identify_variable)
        self.descriptive_analysis(identify_variable.list)
        return {}
        
    def descriptive_analysis(self, variables: List[str]) -> None:
        
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