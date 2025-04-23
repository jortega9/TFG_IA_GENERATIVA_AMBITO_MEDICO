"""Agent that makes a Kaplan-Meier survival test."""

import configparser
import json
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lifelines import CoxPHFitter
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))
from ai.agents.agent import Agent

load_dotenv()

SETTINGS_PATH = os.getenv("SETTINGS_PATH")

config = configparser.ConfigParser()
config.read(SETTINGS_PATH)

DF_PATH = os.path.join(config["data_path"]["processed_path"], "dataset.csv")
VARIABLE_PATH = os.path.join(config["data_path"]["processed_path"], "variables_significativas_totales.csv")
GROUP_PATH = os.path.join(config["data_path"]["processed_path"], "variable_grupo.json")
TIME_PATH = os.path.join(config["data_path"]["processed_path"], "variable_time.json")
LOG_RANK_PATH = os.path.join(config["data_path"]["processed_path"], "log_rank.csv")

OUTPUT_UNI_PATH = os.path.join(config["data_path"]["processed_path"], "cox_univariante.csv")
OUTPUT_MUL_PATH = os.path.join(config["data_path"]["processed_path"], "cox_multivariante.csv")

class COXAgent(Agent):
    """"""
    
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv(DF_PATH)
        try:
            self.df_var = pd.read_csv(VARIABLE_PATH)
            self.df_log = pd.read_csv(LOG_RANK_PATH)
        except Exception:
            self.df_var = pd.DataFrame(columns=["variable"])
        try:
            self.df_log = pd.read_csv(LOG_RANK_PATH)
        except Exception:
            self.df_log = pd.DataFrame(columns=["variable"])
        with open(GROUP_PATH, "r", encoding="utf-8") as f:
            group_config = json.load(f)
            self.group_variable = group_config["group_variable"]
            self.valid_keys = group_config.get("valid_keys", [])
        with open(TIME_PATH, "r", encoding="utf-8") as f:
            time_config = json.load(f)
            self.time_variable = time_config["time_variable"]
            
    def execute(self) -> dict:
        """"""
        df_filtered = self.df_var[(self.df_var['tipo'].isin(['numérica']))]
        var_list = df_filtered['variable'].to_list()
        print(var_list)
        log_filtered = self.df_log[(self.df_log['significative'].isin([True]))]
        log_list = log_filtered['variable'].to_list()
        print(log_list)
        var = list(set(var_list + log_list))
        print(var)
        
        ret = self.cox_univariate_analysis(variables=var)
        
        ret.to_csv(OUTPUT_UNI_PATH, index=False)
        
        mul = self.cox_multivariate_analysis(variables=var)
        
        mul.to_csv(OUTPUT_MUL_PATH, index=False)
        
        return {
            "explanation": "Cox explanation",
            "results": {
                "cox_univariante": OUTPUT_UNI_PATH,
                "cox_multivariante": OUTPUT_MUL_PATH,
            }
        }
        
    def cox_univariate_analysis(self, variables: list[str]) -> pd.DataFrame:

        df_filtered = self.df[[self.time_variable, self.group_variable] + variables].copy()
        df_filtered.columns = ['time', 'event'] + variables

        df_filtered['time'] = pd.to_numeric(df_filtered['time'], errors='coerce')
        df_filtered['event'] = pd.to_numeric(df_filtered['event'], errors='coerce')
        df_filtered['event_occurred'] = df_filtered['event'] == 1
        df_filtered = df_filtered.dropna(subset=['time', 'event_occurred'])

        results = []

        for var in variables:
            df_var = df_filtered[['time', 'event_occurred', var]].dropna()
            if df_var[var].nunique() < 2:
                continue

            cph = CoxPHFitter()
            try:
                cph.fit(df_var, duration_col='time', event_col='event_occurred')
                summary = cph.summary.loc[var]
                results.append({
                    "variable": var,
                    "coef": summary["coef"],
                    "HR": summary["exp(coef)"],
                    "p": summary["p"],
                    "ci_lower": summary["exp(coef) lower 95%"],
                    "ci_upper": summary["exp(coef) upper 95%"],
                    "c_index": cph.concordance_index_
                })
            except Exception as e:
                print(f"❌ Error en Cox para '{var}': {e}")
                continue

        return pd.DataFrame(results)
    
    def cox_multivariate_analysis(self, variables: list[str]) -> pd.DataFrame:
        df_filtered = self.df[[self.time_variable, self.group_variable] + variables].copy()
        df_filtered.columns = ['time', 'event'] + variables

        df_filtered['time'] = pd.to_numeric(df_filtered['time'], errors='coerce')
        df_filtered['event'] = pd.to_numeric(df_filtered['event'], errors='coerce')
        df_filtered['event_occurred'] = df_filtered['event'] == 1
        df_filtered = df_filtered.dropna(subset=['time', 'event_occurred'] + variables)

        cph = CoxPHFitter()
        try:
            cph.fit(df_filtered[['time', 'event_occurred'] + variables], duration_col='time', event_col='event_occurred')
            summary = cph.summary.reset_index().rename(columns={
                'index': 'variable',
                'exp(coef)': 'HR',
                'exp(coef) lower 95%': 'ci_lower',
                'exp(coef) upper 95%': 'ci_upper'
            })
            summary['c_index'] = cph.concordance_index_
            return summary[['variable', 'coef', 'HR', 'p', 'ci_lower', 'ci_upper', 'c_index']]
        except Exception as e:
            print(f"❌ Error en modelo multivariante: {e}")
            return pd.DataFrame([])
        