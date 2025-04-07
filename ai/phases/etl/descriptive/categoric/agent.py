"""Agent that identify the categorical variables and make a csv summary.
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
from statsmodels.stats.proportion import proportion_confint

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))


from ai.agents.agent import Agent
from ai.phases.etl.descriptive.categoric.prompts import IDENTIFY_WORKFLOW, CONCLUSION_WORKFLOW
from ai.phases.etl.descriptive.categoric.schemas import IdentifySchema, ConclusionSchema

load_dotenv()

SETTINGS_PATH = os.getenv("SETTINGS_PATH")

config = configparser.ConfigParser()

config.read(SETTINGS_PATH)

MASTER_PATH=os.path.join(config["data_path"]["processed_path"], "master.json")
DF_PATH=os.path.join(config["data_path"]["processed_path"], "dataset.csv")

OUTPUT_PATH=os.path.join(config["data_path"]["processed_path"], "analisis_estadistico_categorico.csv")

class CategoricalDescriptiveAgent(Agent):
    
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv(DF_PATH)
        with open(MASTER_PATH, "r", encoding="utf-8") as f:
            self.master = json.load(f)
        self.summary = pd.DataFrame(columns=["variable", "valor", "n", "porcentaje", "ic_95_inf", "ic_95_sup"])
            
    def execute(self) -> dict:
        """Main call to the LLM Agent.

        Returns:
            dict: 
        """
        identify_variable = self.call_llm(
            prompt=IDENTIFY_WORKFLOW.format(
                master=json.dumps(self.master),  
                sample=self.df.sample(n=20).to_string()
            ), 
            response_format=IdentifySchema,
            temperature=0
        )
        self.descriptive_analysis(identify_variable.list)
        return {
            "explanation": identify_variable.explanation,
            "results": {
                "variables": identify_variable.list,
                "csv_path": OUTPUT_PATH
            }
        }
    
    def descriptive_analysis(self, variables: List[str]) -> None:
        """Make the descriptive analysis.

        Args:
            variables (List[str]): List of categorical variables.
        """
        
        for column in variables:
            
            if column not in self.df.columns:
                continue
            
            df = self.df[column].dropna()
            total = len(df)

            resumen = []
            for valor, conteo in df.value_counts().items():
                porcentaje = conteo / total * 100
                ic_low, ic_up = proportion_confint(conteo, total, alpha=0.05, method='wilson')
                resumen.append({
                    "variable": column,
                    "valor": valor,
                    "n": conteo,
                    "porcentaje": round(porcentaje, 2),
                    "ic_95_inf": round(ic_low * 100, 2),
                    "ic_95_sup": round(ic_up * 100, 2)
                })

            self.summary = pd.concat([self.summary, pd.DataFrame(resumen)], ignore_index=True)
            
        self.summary.to_csv(OUTPUT_PATH, index=False)