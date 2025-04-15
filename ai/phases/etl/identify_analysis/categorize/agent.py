"""Agent that make a categorization of all the columns of the dataset."""
import configparser
import io
import json
import os
import re
import sys

import pandas as pd
import numpy as np
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from ai.agents.agent import Agent
from ai.phases.etl.identify_analysis.categorize.prompts import AGENT_WORKFLOW
from ai.phases.etl.identify_analysis.categorize.schemas import CategorizeSchema

load_dotenv()

SETTINGS_PATH = os.getenv("SETTINGS_PATH")

config = configparser.ConfigParser()

config.read(SETTINGS_PATH)

MASTER_PATH = os.path.join(config["data_path"]["processed_path"], "master.json")
DF_PATH = os.path.join(config["data_path"]["processed_path"], "dataset.csv")
OUTPUT_PATH = os.path.join(config["data_path"]["processed_path"], "variable_info.json")

class CategorizeVariablesAgent(Agent):
    """This is the most important agent of the stadistic analysis
    For each columns the LLM agent identify wich type of variable it is,
    wich test should be do it to the column.
    
    This is the brain of the analysis.
    """
    
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv(DF_PATH) 
        with open(MASTER_PATH, "r", encoding="utf-8") as f:
            self.master = json.load(f)
            
    def execute(self) -> dict:
        """Main call to the LLM Agent.
        
        For each column the LLM call will return:
        
        column_name : {
            type: numerical / categorical / irrelevant
            assign_test: t_student / fisher / mann_whitney, ...
        }
        
        All this components will be in the return statement.

        Returns:
            dict: Returns a dict with all the information of all the columns
        """
        
        ret = {}
        
        for col in self.df.columns:
            data_column = self.df[col].dropna().tolist()
            info_column = self.master.get(col, {})
            description = info_column.get("descripcion", "Sin descripción")
            values = info_column.get("valores", None)
            
            input_llm = {
                "nombre_variable": col,
                "descripcion": description,
                "valores_posibles": values,
                "datos_columna": data_column 
            }
            
            if input_llm is None: 
                continue
            
            response = self.call_llm(
                prompt=AGENT_WORKFLOW.format(
                    col=col,
                    descripcion=description,
                    valores_posibles=values,
                    datos_columna=data_column,
                ),
                response_format=CategorizeSchema
            )
            
            ret[response.name] = {
                "type": response.type,
                "test": response.test
            }
        
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(ret, f, ensure_ascii=False, indent=2)
        
        return ret
            
            
            
            
#########################################################################################
#                                   DELETE ME                                           #
#########################################################################################   
def main() :
    agent = CategorizeVariablesAgent()
    print(agent.execute())
    
if __name__ == "__main__":
    main()
            