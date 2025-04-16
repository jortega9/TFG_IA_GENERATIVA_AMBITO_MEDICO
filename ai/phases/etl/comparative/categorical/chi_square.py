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

load_dotenv()

SETTINGS_PATH = os.getenv("SETTINGS_PATH")

config = configparser.ConfigParser()

config.read(SETTINGS_PATH)

INFO_PATH = os.path.join(config["data_path"]["processed_path"], "variable_info.json")
DF_PATH = os.path.join(config["data_path"]["processed_path"], "dataset.csv")
GROUP_PATH = os.path.join(config["data_path"]["processed_path"], "variable_grupo.json")
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
        with open(GROUP_PATH, "r", encoding="utf-8") as f:
            self.group_variable = json.load(f)
        self.df_chi = pd.DataFrame(columns=["variable", "tabla", "chi2", "dof", "p_value", "significativo"])
            
    def execute(self) -> dict:
        """Main call to the Chi-Square Agent."""

        group_var = self.group_variable["group_variable"]
        valid_keys = set(float(k) for k in self.group_variable["valid_keys"])

        # Asegurar consistencia de tipos
        self.df[group_var] = self.df[group_var].astype(float)
        df = self.df[self.df[group_var].isin(valid_keys)]

        chi_data = []

        for var, info in self.variable_info.items():
            if info["type"] == "categorical" and info["test"] == "chi-cuadrado":
                if var not in df.columns or var == group_var:
                    continue

                df_valid = df[[group_var, var]].dropna()

                if df_valid.empty:
                    continue

                contingency = pd.crosstab(df_valid[group_var], df_valid[var])
                if contingency.shape[0] < 2 or contingency.shape[1] < 2:
                    continue  # Evitar tablas inválidas

                try:
                    chi2, p, dof, expected = chi2_contingency(contingency)
                    chi_data.append({
                        "variable": var,
                        "tabla": contingency.to_dict(),
                        "chi2": round(chi2, 4),
                        "dof": dof,
                        "p_value": round(p, 4),
                        "significativo": p < 0.05
                    })
                except Exception as e:
                    chi_data.append({
                        "variable": var,
                        "tabla": contingency.to_dict(),
                        "chi2": None,
                        "dof": None,
                        "p_value": None,
                        "significativo": None,
                        "error": str(e)
                    })

        self.df_chi = pd.DataFrame(chi_data)
        self.df_chi.to_csv(OUTPUT_PATH, index=False)

        return {
            "explanation": "TODO",
            "results": {
                "csv_chi_path": OUTPUT_PATH
            }
        }

        