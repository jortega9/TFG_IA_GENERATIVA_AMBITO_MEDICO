"""Agent that make a comparative stadistic analysis with the categorical"""

"""Agent that identify the categorical variables and make a csv summary.
"""
import configparser
import json
import os
import sys

import pandas as pd
from dotenv import load_dotenv
from scipy.stats import chi2_contingency

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from ai.agents.agent import Agent
from ai.phases.etl.comparative.categorical.prompt import CONCLUSION
from ai.phases.etl.comparative.categorical.schemas import (
    GroupVariableSchema,
)

load_dotenv()

SETTINGS_PATH = os.getenv("SETTINGS_PATH")

config = configparser.ConfigParser()

config.read(SETTINGS_PATH)

INFO_PATH = os.path.join(config["data_path"]["processed_path"], "master.json")
DF_PATH = os.path.join(config["data_path"]["processed_path"], "dataset.csv")
OUTPUT_PATH = os.path.join(
    config["data_path"]["processed_path"], "analisis_categorico_chi_cuadrado.csv"
)

class ChiSquareComparativeAgent(Agent):
    """Comparative categorical with chi square test."""
    
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv(DF_PATH)
        with open(INFO_PATH, "r", encoding="utf-8") as f:
            self.variable_info = json.load(f)