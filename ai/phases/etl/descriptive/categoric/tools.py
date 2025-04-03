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

from ai.phases.etl.descriptive.numeric.context import DataContext

load_dotenv()

SETTINGS_PATH = os.getenv("SETTINGS_PATH")

config = configparser.ConfigParser()

config.read(SETTINGS_PATH)

MASTER_PATH=os.path.join(config["data_path"]["processed_path"], "master.json")
DF_PATH=os.path.join(config["data_path"]["processed_path"], "dataset.csv")

OUTPUT_PATH=os.path.join(config["data_path"]["processed_path"], "analisis_estadistico_categorico.csv")

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
	

	return [
        read_csv,
        open_master,
        sample_df,
        info_df,
        show_master,
    ]