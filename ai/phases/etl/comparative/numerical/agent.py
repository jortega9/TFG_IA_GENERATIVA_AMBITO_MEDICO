"""Agent that make a comparative stadistic analysis with the categorical"""

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

from scipy.stats import ttest_ind, mannwhitneyu, shapiro

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from ai.agents.agent import Agent
from ai.phases.etl.comparative.numerical.prompts import (
    DECISION_TEST,
    CONCLUSION,
)
from ai.phases.etl.comparative.numerical.schemas import (
    DecisionTestSchema,
)

load_dotenv()

SETTINGS_PATH = os.getenv("SETTINGS_PATH")

config = configparser.ConfigParser()

config.read(SETTINGS_PATH)

MASTER_PATH = os.path.join(config["data_path"]["processed_path"], "master.json")
DF_PATH = os.path.join(config["data_path"]["processed_path"], "dataset.csv")
NUMERICAL_PATH = os.path.join(
    config["data_path"]["processed_path"], "analisis_estadistico_numerico.csv"
)

T_STUDENT_PATH = os.path.join(
    config["data_path"]["processed_path"], "analisis_numerico_t_student.csv"
)
MANN_WHITNEY_U_PATH = os.path.join(
    config["data_path"]["processed_path"], "analisis_numerico_mann_whitney.csv"
)
 
class ComparativeNumericalAgent(Agent):
    """Comparative Categorical Stadistic Analysis LLM Agent."""

    def __init__(self, group_variable:dict):
        super().__init__()
        self.df = pd.read_csv(DF_PATH)
        self.df_numerical = pd.read_csv(NUMERICAL_PATH)
        with open(MASTER_PATH, "r", encoding="utf-8") as f:
            self.master = json.load(f)
        self.group_variable = group_variable
        
        
    def execute(self) -> dict:
        """Main call to the LLM Agent.

        Returns:
            dict: _description_
        """
        decision_test = self.call_llm(
            prompt=DECISION_TEST.format(
                group_variable=self.group_variable["name"],
                numerical=self.df_numerical.to_string(),
                sample=self.df.to_string(),
                master=json.dumps(self.master),
            ),
            response_format=DecisionTestSchema
        )
        self.comparative_analysis(
            decision_test=decision_test,
        )
        return {
            "explanation": decision_test.explanation,
            "results" : {
                "csv_t_student_path": T_STUDENT_PATH,
                "csv_mann_whitney_path": MANN_WHITNEY_U_PATH,
            }
        }
        
    def comparative_analysis(self, decision_test:DecisionTestSchema) -> None:
        """Performs statistical comparison of numerical variables between two groups.

        Args:
            decision_test (DecisionTestSchema): Variables to test and suggested test.
        """

        results_ttest = []
        results_mannwhitney = []

        group_col = self.group_variable["name"]
        valid_keys = self.group_variable["valid_keys"]

        df = self.df.copy()
        df[group_col] = df[group_col].astype(str)
        df = df[df[group_col].isin(valid_keys)]

        df_numerical = self.df_numerical.set_index("variable")

        for var_schema in decision_test.list:
            var = var_schema.variable
            test = var_schema.test_sugerido
            description = var_schema.description

            if var not in df.columns or var not in df_numerical.index:
                continue

            grupo1 = df[df[group_col] == valid_keys[0]][var].dropna()
            grupo2 = df[df[group_col] == valid_keys[1]][var].dropna()

            if len(grupo1) < 3 or len(grupo2) < 3:
                continue

            row = {
                "variable": var,
                "descripcion": description,
                "n_casos": len(grupo1),
                "n_controles": len(grupo2),
                "media": df_numerical.loc[var, "media"],
                "mediana": df_numerical.loc[var, "mediana"],
                "desviacion": df_numerical.loc[var, "std"],
            }

            if test == "t-student":
                _, p = ttest_ind(grupo1, grupo2, equal_var=False)
                row.update({"p_value": p, "significativo": p < 0.05})
                results_ttest.append(row)

            elif test == "mann-whitney":
                _, p = mannwhitneyu(grupo1, grupo2, alternative="two-sided")
                row.update({"p_value": p, "significativo": p < 0.05})
                results_mannwhitney.append(row)

        pd.DataFrame(results_ttest).to_csv(T_STUDENT_PATH, index=False)
        pd.DataFrame(results_mannwhitney).to_csv(MANN_WHITNEY_U_PATH, index=False)
        