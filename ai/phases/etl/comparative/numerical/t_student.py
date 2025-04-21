"""Agent that identify the categorical variables and make a csv summary."""
import configparser
import json
import os
import sys

import pandas as pd
from dotenv import load_dotenv
from scipy.stats import ttest_ind

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from ai.agents.agent import Agent
from ai.phases.etl.comparative.numerical.prompts import CONCLUSION

load_dotenv()

SETTINGS_PATH = os.getenv("SETTINGS_PATH")

config = configparser.ConfigParser()

config.read(SETTINGS_PATH)

INFO_PATH = os.path.join(config["data_path"]["processed_path"], "variable_info.json")
DF_PATH = os.path.join(config["data_path"]["processed_path"], "dataset.csv")
GROUP_PATH = os.path.join(config["data_path"]["processed_path"], "variable_grupo.json")
OUTPUT_PATH = os.path.join(
config["data_path"]["processed_path"], "analisis_numerico_t_student.csv"
)

class TStudentComparativeAgent(Agent):
    """Comparative numerical with t student test."""
    
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv(DF_PATH)
        with open(INFO_PATH, "r", encoding="utf-8") as f:
            self.variable_info = json.load(f)
        with open(GROUP_PATH, "r", encoding="utf-8") as f:
            self.group_variable = json.load(f)
        self.df_ts = pd.DataFrame(columns=["variable", "n_casos", "n_controles", "p_value", "significativo"])
        
    def execute(self) -> dict:
        """Main call to the T Student Agent."""

        group_var = self.group_variable["group_variable"]
        valid_keys = set(float(k) for k in self.group_variable["valid_keys"])

        self.df[group_var] = self.df[group_var].astype(float)
        df = self.df[self.df[group_var].isin(valid_keys)]

        ts_data = []

        for var, info in self.variable_info.items():
            if info["type"] == "numerical" and info["test"] == "t_student":
                if var not in df.columns or var == group_var:
                    continue

                df_valid = df[[group_var, var]].dropna()
                if df_valid.empty:
                    continue

                try:
                    group1 = df_valid[df_valid[group_var] == list(valid_keys)[0]][var]
                    group2 = df_valid[df_valid[group_var] == list(valid_keys)[1]][var]

                    if len(group1) < 3 or len(group2) < 3:
                        continue
        
                    _, p = ttest_ind(group1, group2, equal_var=False)

                    ts_data.append({
                        "variable": var,
                        "n_casos": len(group1),
                        "n_controles": len(group2),
                        "p_value": round(p, 4),
                        "significativo": p < 0.05
                    })

                except Exception as e:
                    ts_data.append({
                        "variable": var,
                        "n_casos": len(group1) if 'group1' in locals() else None,
                        "n_controles": len(group2) if 'group2' in locals() else None,
                        "p_value": None,
                        "significativo": None,
                        "error": str(e)
                    })

        self.df_ts = pd.DataFrame(ts_data)
        self.df_ts.to_csv(OUTPUT_PATH, index=False)

        return {
            "explanation": "TODO",
            "results": {
                "csv_t_student": OUTPUT_PATH
            }
        }
