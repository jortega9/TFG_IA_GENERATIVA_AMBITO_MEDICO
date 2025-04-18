"""Agent that make a Kaplan-Meier survival test."""

import configparser
import json
import os
import sys

import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
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
OUTPUT_DIR = os.path.join(config["data_path"]["processed_path"], "kaplan_meier")

class KaplanMeierAgent(Agent):
    """Kaplan-Meier survival analysis agent."""

    def __init__(self):
        super().__init__()
        self.df = pd.read_csv(DF_PATH)
        try:
            self.df_var = pd.read_csv(VARIABLE_PATH)
        except Exception as e:
            self.df_var = pd.DataFrame(columns=["variable"])
        with open(GROUP_PATH, "r", encoding="utf-8") as f:
            group_config = json.load(f)
            self.group_variable = group_config["group_variable"]
            self.valid_keys = group_config.get("valid_keys", [])
        with open(TIME_PATH, "r", encoding="utf-8") as f:
            time_config = json.load(f)
            self.time_variable = time_config["time_variable"]
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    def execute(self) -> dict:
        """Ejecuta el análisis de supervivencia de Kaplan-Meier."""
        
        df_filtered = self.df_var[(self.df_var['tipo'].isin(['categórica']))]
        var_list = df_filtered['variable'].to_list()
        for var in var_list:
            self.stratified_km_plot(var=var)
        return {}

    def kaplan_meier_plot(self) -> dict:
        """Ejecuta el análisis de supervivencia de Kaplan-Meier."""
        df_filtered = self.df[[self.time_variable, self.group_variable]].copy()
        df_filtered.columns = ['time', 'event']
        
        df_filtered['time'] = pd.to_numeric(df_filtered['time'], errors='coerce')
        df_filtered['event'] = pd.to_numeric(df_filtered['event'], errors='coerce')
        
        df_filtered = df_filtered[(df_filtered['event'].isin([1, 2]))]
        
        df_filtered['event_occurred'] = df_filtered['event'] == 1
        
        
        df_filtered = df_filtered.dropna(subset=['time', 'event_occurred'])
        
        kmf = KaplanMeierFitter()
        kmf.fit(df_filtered['time'], event_observed=df_filtered['event_occurred'])

        plt.figure()
        kmf.plot()
        plt.title('Curva de Supervivencia (Kaplan-Meier)')
        plt.xlabel('Tiempo (meses)')
        plt.ylabel('Probabilidad de supervivencia')
        plt.grid(True)
        plt.tight_layout()
        
        output_path = os.path.join(OUTPUT_DIR, "kaplan_meier_plot.png")
        plt.savefig(output_path)
        
        return {
            "n_observations": kmf.event_table.shape[0],
            "median_survival_time": kmf.median_survival_time_,
            "survival_table": kmf.survival_function_.reset_index().to_dict(orient='records'),
            "path": output_path,
        }

    def stratified_km_plot(self, var:str) -> dict:
        """"""
        # Se hace una copia del df original con solo las columnas rbq, trbq, variable
        df_filtered = self.df[[self.time_variable, self.group_variable, var]].copy()
        # Se renombran las columnas en orden
        df_filtered.columns = ['time', 'event', var]
        
        # Se transforman a numericas las variables de cada columna para el analisis
        df_filtered['time'] = pd.to_numeric(df_filtered['time'], errors='coerce')
        df_filtered['event'] = pd.to_numeric(df_filtered['event'], errors='coerce')
        df_filtered[var] = pd.to_numeric(df_filtered[var], errors='coerce')
        
        # Se filtran las filas que tengan el valor 1 (caso), 2 (control)
        df_filtered = df_filtered[(df_filtered['event'].isin([1, 2]))]
        
        # Se añade una nueva columna que es true si el evento se ha cumplido (es decir, es un caso)
        df_filtered['event_occurred'] = df_filtered['event'] == 1
        
        # Se eliminan los nulos ya que el Fitter no los admite
        df_filtered = df_filtered.dropna(subset=['time', 'event_occurred', var])
        
        # Se instancia el Fitter y se inicializa el plot
        kmf = KaplanMeierFitter()
        plt.figure()
        
        # Para cada valor unico de la variable a analizar se hace una iteracion
        for group in sorted(df_filtered[var].dropna().unique()):
            # Se hace una columna en donde es true si la fila tiene como valor el valor actual del for
            mask = df_filtered[var] == group
            # Se hace la curva de supervivencia para ese grupo
            kmf.fit(df_filtered[mask]['time'], event_observed=df_filtered[mask]['event_occurred'], label=f"{var} {int(group)}")
            # Se crea el plot
            kmf.plot()
        
        plt.title(f"Curvas de Supervivencia por {var}")
        plt.xlabel("Tiempo (meses)")
        plt.ylabel("Probabilidad de supervivencia")
        plt.grid(True)
        plt.tight_layout()
        
        output_path = os.path.join(OUTPUT_DIR, f"kaplan_meier_plot_{var}.png")
        plt.savefig(output_path)
        
        
