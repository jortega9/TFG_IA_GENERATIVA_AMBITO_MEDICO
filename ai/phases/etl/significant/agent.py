"""Agent that collect all the significant variables."""
import configparser
import json
import os
import sys

import pandas as pd
from dotenv import load_dotenv
from scipy.stats import mannwhitneyu

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from ai.agents.agent import Agent
from ai.phases.etl.comparative.numerical.prompts import CONCLUSION

load_dotenv()

SETTINGS_PATH = os.getenv("SETTINGS_PATH")

config = configparser.ConfigParser()

config.read(SETTINGS_PATH)

MASTER_PATH = os.path.join(config["data_path"]["processed_path"], "master.json")
CHI_PATH = os.path.join(config["data_path"]["processed_path"], "analisis_categorico_chi_cuadrado.csv")
FISHER_PATH = os.path.join(config["data_path"]["processed_path"], "analisis_categorico_fisher.csv")
MANN_PATH = os.path.join(config["data_path"]["processed_path"], "analisis_numerico_mann_whitney.csv")
STUDENT_PATH = os.path.join(config["data_path"]["processed_path"], "analisis_numerico_t_student.csv")

OUTPUT_PATH = os.path.join(config["data_path"]["processed_path"], "variables_significativas_totales.csv")

class CollectSignificantVariables(Agent):
    """ """
    
    def __init__(self):
        super().__init__()
        with open(MASTER_PATH, "r", encoding="utf-8") as f:
            self.master = json.load(f)
        self.df = pd.DataFrame(columns=["variable", "tipo", "test_aplicado", "valor"])
    
    def execute(self) -> dict:
        """Main call to the LLM agent."""
        self.collect_chi_square()
        self.collect_fisher()
        self.collect_mann_whitney()
        self.collect_t_student
        
        self.df.to_csv(OUTPUT_PATH, index=False)
        
        # Hacer aqui un LLM que saque conclusiones
        
        return {
            "explanation": "TODO",
            "results": {
                "csv_path": OUTPUT_PATH
            }
        }
        
    def collect_chi_square(self) -> None:
        try:
            df = pd.read_csv(CHI_PATH)
            if df.empty:
                return
            df = df[df["significativo"] == True]
            df["tipo"] = "categórica"
            df["test_aplicado"] = "chi-cuadrado"
            df["valor"] = df["p_value"]
            self.df = pd.concat([self.df, df[["variable", "tipo", "test_aplicado", "valor"]]])
        except Exception as e:
            print("Error en chi-cuadrado:", e)

    def collect_fisher(self) -> None:
        try:
            df = pd.read_csv(FISHER_PATH)
            if df.empty:
                return
            df = df[df["significativo"] == True]
            df["tipo"] = "categórica"
            df["test_aplicado"] = "fisher"
            df["valor"] = df["p_value"]
            self.df = pd.concat([self.df, df[["variable", "tipo", "test_aplicado", "valor"]]])
        except Exception as e:
            print("Error en fisher:", e)

    def collect_mann_whitney(self) -> None:
        try:
            df = pd.read_csv(MANN_PATH)
            if df.empty:
                return
            df = df[df["significativo"] == True]
            df["tipo"] = "numérica"
            df["test_aplicado"] = "mann-whitney"
            df["valor"] = df["p_value"]
            self.df = pd.concat([self.df, df[["variable", "tipo", "test_aplicado", "valor"]]])
        except Exception as e:
            print("Error en mann-whitney:", e)

    def collect_t_student(self) -> None:
        try:
            df = pd.read_csv(STUDENT_PATH)
            if df.empty:
                return
            df = df[df["significativo"] == True]
            df["tipo"] = "numérica"
            df["test_aplicado"] = "t-student"
            df["valor"] = df["p_value"]
            self.df = pd.concat([self.df, df[["variable", "tipo", "test_aplicado", "valor"]]])
        except Exception as e:
            print("Error en t-student:", e)
