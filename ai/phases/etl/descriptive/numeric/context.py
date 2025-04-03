import json

import pandas as pd

class DataContext:
	def __init__(self):
		self.df = pd.DataFrame()
		self.master = {}
		self.summary = pd.DataFrame(columns=["variable", "n", "media", "std", "mediana", "ric", "rango"])