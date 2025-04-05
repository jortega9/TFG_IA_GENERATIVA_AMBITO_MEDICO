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
from scipy.stats import chi2_contingency, fisher_exact

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from ai.agents.agent import Agent
from ai.phases.etl.comparative.categorical.prompt import (
    IDENTIFY_GROUP_VARIABLE,
    ASSIGN_CATEGORICAL_TEST,
    CONCLUSION,
)
from ai.phases.etl.comparative.categorical.schemas import (
    GroupVariableSchema,
    AssignCategoricalTestSchema,
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

CHI_PATH = os.path.join(
    config["data_path"]["processed_path"], "analisis_categorico_chi_cuadrado.csv"
)
FISHER_PATH = os.path.join(
    config["data_path"]["processed_path"], "analisis_categorico_fisher.csv"
)


class ComparativeCategoricalAgent(Agent):
    """Comparative Categorical Stadistic Analysis LLM Agent."""

    def __init__(self):
        super().__init__()
        self.df = pd.read_csv(DF_PATH)
        self.df_categorical = pd.read_csv(CATEGORICAL_PATH)
        with open(MASTER_PATH, "r", encoding="utf-8") as f:
            self.master = json.load(f)
        df_chi_square = pd.DataFrame()
        df_fisher = pd.DataFrame()

    def execute(self) -> dict:
        """Main call to the LLM Agent.

        Returns:
            dict:
        """
        identify_group_variable = self.call_llm(
            prompt=IDENTIFY_GROUP_VARIABLE.format(
                master=json.dumps(self.master),
                sample=self.df.sample(n=20).to_string(),
                categorical=self.df_categorical.to_string(),
            ),
            response_format=GroupVariableSchema,
        )
        assign_categorical_test = self.call_llm(
            prompt=ASSIGN_CATEGORICAL_TEST.format(
                group_variable=identify_group_variable.model_dump(),
                categorical=self.df_categorical.to_string(),
                master=json.dumps(self.master),
                sample=self.df.sample(n=20).to_string(),
            ),
            response_format=AssignCategoricalTestSchema,
        )
        
        self.comparative_analysis(
            group_variable=identify_group_variable,
            list=assign_categorical_test,
        )
        explanation = self.append_explanation(
            expl1=identify_group_variable.explanation,
            expl2=assign_categorical_test.explanation,
        )
        return {
            "explanation": explanation, 
            "results" : {
                "group_variable": identify_group_variable.group_variable,
                "csv_chi_path": CHI_PATH,
                "csv_fisher_path": FISHER_PATH,
            }
        }


    def comparative_analysis(
        self, group_variable: GroupVariableSchema, list: AssignCategoricalTestSchema
    ) -> None:
        chi_data = []
        fisher_data = []

        group_col = group_variable.group_variable
        valid_groups = group_variable.valid_keys

        self.df[group_col] = self.df[group_col].astype(str)
        df = self.df[self.df[group_col].isin(valid_groups)]

        for cat in list.categorical_list:
            var = cat.variable
            test = cat.test_sugerido
            desc = cat.descripcion

            df_valid = df[[group_col, var]].dropna()
            contingency = pd.crosstab(df_valid[group_col], df_valid[var])
            row = {
                "variable": var,
                "descripcion": desc,
                "test_usado": test,
                "tabla": contingency.to_dict()
            }

            if test == "chi-cuadrado":
                try:
                    chi2, p, dof, expected = chi2_contingency(contingency)
                    row.update({
                        "chi2": chi2,
                        "p_value": p,
                        "dof": dof,
                        "significativo": p < 0.05
                    })
                    chi_data.append(row)
                except Exception as e:
                    row["error"] = str(e)
                    chi_data.append(row)

            elif test == "fisher":
                try:
                    if contingency.shape == (2, 2):
                        stat, p = fisher_exact(contingency)
                        row.update({
                            "stat": stat,
                            "p_value": p,
                            "significativo": p < 0.05
                        })
                    else:
                        row.update({
                            "stat": None,
                            "p_value": None,
                            "significativo": None,
                            "error": "Tabla no es 2x2"
                        })
                    fisher_data.append(row)
                except Exception as e:
                    row["error"] = str(e)
                    fisher_data.append(row)

        pd.DataFrame(chi_data).to_csv(CHI_PATH, index=False)
        pd.DataFrame(fisher_data).to_csv(FISHER_PATH, index=False)


    def append_explanation(self, expl1: str, expl2: str) -> str:
        """Appends the two explanations of the agents."""
        return f"Explicacion de la eleccion del grupo de control: \n {expl1} \n Explicacion de la eleccion de los tests categoricos: \n {expl2} \n"
