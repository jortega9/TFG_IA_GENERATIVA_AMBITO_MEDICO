"""_summary_
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
from ai.phases.etl.survival.prompts import (
    IDENTIFY_VARIABLES,
    CONCLUSION,
)
from ai.phases.etl.survival.schemas import (
    IdentifyVariableSchema,
)

load_dotenv()

SETTINGS_PATH = os.getenv("SETTINGS_PATH")

config = configparser.ConfigParser()

config.read(SETTINGS_PATH)

MASTER_PATH = os.path.join(config["data_path"]["processed_path"], "master.json")
DF_PATH = os.path.join(config["data_path"]["processed_path"], "dataset.csv")
CATEGORICAL_PATH = os.path.join(
    config["data_path"]["processed_path"], "analisis_estadistico_categorico.csv"
)
NUMERICAL_PATH = os.path.join(
    config["data_path"]["processed_path"], "analisis_estadistico_numerico.csv"
)
CHI_PATH = os.path.join(
    config["data_path"]["processed_path"], "analisis_categorico_chi_cuadrado.csv"
)
FISHER_PATH = os.path.join(
    config["data_path"]["processed_path"], "analisis_categorico_fisher.csv"
)
T_STUDENT_PATH = os.path.join(
    config["data_path"]["processed_path"], "analisis_numerico_t_student.csv"
)
MANN_WHITNEY_U_PATH = os.path.join(
    config["data_path"]["processed_path"], "analisis_numerico_mann_whitney.csv"
)

class SurvivalAnalysisAgent(Agent):
    """Class that make the survival analysis."""
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv(DF_PATH)
        self.df_categorical = pd.read_csv(CATEGORICAL_PATH)
        self.df_numerical = pd.read_csv(NUMERICAL_PATH)
        self.df_chi = pd.read_csv(CHI_PATH)
        self.df_fisher = pd.read_csv(FISHER_PATH)
        self.df_mann = pd.read_csv(MANN_WHITNEY_U_PATH)
        with open(MASTER_PATH, "r", encoding="utf-8") as f:
            self.master = json.load(f)
    
    def execute(self) -> dict:
        """Main class to the LLM Agent.
        
        Returns:
            dict
        """
        
        identify_variables = self.call_llm(
            model="gpt-4o",
            prompt=IDENTIFY_VARIABLES.format(
                master=json.dumps(self.master),
                analisis_estadistico_numerico=self.df_numerical.to_string(),
                analisis_estadistico_categorico=self.df_numerical.to_string(),
                chi2=self.df_chi.to_string(),
                fisher=self.df_fisher.to_string(),
                mannwhitney=self.df_mann.to_string(),
            ),
            response_format=IdentifyVariableSchema
        )
        
        return { "results" : identify_variables }
        
