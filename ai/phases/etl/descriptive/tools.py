"""Tools that the ReAct Agent will use."""

import configparser
import io
import json
import os
import re
import sys

import pandas as pd
import numpy as np
from scipy import stats

from dotenv import load_dotenv
from langchain.tools import tool

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from ai.phases.etl.descriptive.context import DataContext

load_dotenv()

SETTINGS_PATH = os.getenv("SETTINGS_PATH")

config = configparser.ConfigParser()

config.read(SETTINGS_PATH)

MASTER_PATH=os.path.join(config["data_path"]["processed_path"], "master.json")
DF_PATH=os.path.join(config["data_path"]["processed_path"], "dataset.csv")

OUTPUT_PATH=os.path.join(config["data_path"]["processed_path"], "analisis_estadistico_numerico.csv")

def create_tools(ctx: DataContext):
	
	@tool
	def read_csv() -> str:
		"""Abre y almacena en la variable df el dataframe."""
		ctx.df = pd.read_csv(DF_PATH)
		return "DataFrame cargado correctamente."
	
	@tool
	def open_master() -> str:
		"""Abre el maestro y lo almacena en master."""
		with open(MASTER_PATH, "r", encoding="utf-8") as f:
			ctx.master = json.load(f)
		return "Maestro cargado correctamente."
	
	@tool
	def sample_df(n:int=10) -> str:
		"""Muestra una muestra aleatoria de n registros del DataFrame."""
		return ctx.df.sample(n=n).to_string()
	
	@tool
	def info_df() -> str:
		"""Devuelve información general del DataFrame."""
		buffer = io.StringIO()
		ctx.df.info(buf=buffer)
		return buffer.getvalue()
	
	@tool
	def show_master():
		"""Devuelve el maestro para su analisis."""
		return json.dumps(ctx.master)
	
	@tool
	def check_distribution_normality(nombre_columna:str):
		"""Verifica si la variable sigue una distribucion normal."""
		data = ctx.df[nombre_columna].dropna()
		if len(data) < 3:
			return False
		_, p_value = stats.shapiro(data)
		return p_value > 0.05
	
	@tool
	def calculate_mean_std(nombre_columna:str):
		"""Calcula la media y la desviación típica."""
		media = ctx.df[nombre_columna].mean()
		std = ctx.df[nombre_columna].std()
		return {"media": media, "std": std}
	
	@tool
	def calculate_median_iqr(nombre_columna:str):
		"""Calcula la mediana y el rango intercuartilico para las variables discretas."""
		mediana = ctx.df[nombre_columna].median()
		ric = ctx.df[nombre_columna].quantile(0.75) - ctx.df[nombre_columna].quantile(0.25)
		return {"mediana": mediana, "ric": ric}
	
	@tool
	def add_to_summary(nombre_columna:str, media=None, std=None, mediana=None, ric=None):
		"""Añade una nueva columna con la información obtenida."""
		nueva_fila = {
			"variable": nombre_columna,
			"media": media,
			"std": std,
			"mediana": mediana,
			"ric": ric
		}
		ctx.summary = pd.concat([ctx.summary, pd.DataFrame([nueva_fila])], ignore_index=True)
		return f"Variable '{nombre_columna}' añadida al resumen."
	
	@tool
	def save_summary():
		"""Guarda el summary en un csv"""
		ctx.summary.to_csv(OUTPUT_PATH, index=False)
		return f"Resumen guardado en '{OUTPUT_PATH}'."

	return [
        read_csv,
        open_master,
        sample_df,
        info_df,
        show_master,
        check_distribution_normality,
        calculate_mean_std,
        calculate_median_iqr,
        add_to_summary,
        save_summary
    ]