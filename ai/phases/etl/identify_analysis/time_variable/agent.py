"""Agent that identify the group varaibles"""

import configparser
import json
import os
import sys

import pandas as pd
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from ai.agents.agent import Agent
from ai.phases.etl.identify_analysis.time_variable.prompts import IDENTIFY_TIME_VARIABLE
from ai.phases.etl.identify_analysis.time_variable.schema import IdentifyTimeSchema

load_dotenv()

SETTINGS_PATH = os.getenv("SETTINGS_PATH")

config = configparser.ConfigParser()

config.read(SETTINGS_PATH)

MASTER_PATH = os.path.join(config["data_path"]["processed_path"], "master.json")
DF_PATH = os.path.join(config["data_path"]["processed_path"], "dataset.csv")
GROUP_PATH = os.path.join(config["data_path"]["processed_path"], "variable_grupo.json")

OUTPUT_PATH = os.path.join(config["data_path"]["processed_path"], "variable_time.json")

class IdentifyTimeVariableAgent(Agent):
    """Identify Time Variable LLM Agent."""

    def __init__(self):
        super().__init__()
        self.df = pd.read_csv(DF_PATH)
        with open(MASTER_PATH, "r", encoding="utf-8") as f:
            self.master = json.load(f)
        with open(GROUP_PATH, "r", encoding="utf-8") as f:
            self.group_variable = json.load(f)
            
    
    def execute(self) -> dict:
        """Main call to the LLM Agent

        Returns:
            dict: returns the reports and the results.
        """
        
        identify_time_variable = self.call_llm(
            prompt=IDENTIFY_TIME_VARIABLE.format(
                master=json.dumps(self.master),
                sample=self.df.sample(n=200).to_string(),
                group_variable=json.dumps(self.group_variable),
            ),
            response_format=IdentifyTimeSchema,
        )
        
        ret = {
            "time_variable" : identify_time_variable.name,
            "other_options" : identify_time_variable.other_options
        }
        
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(ret, f, ensure_ascii=False, indent=2)
        
        return {
            "explanation": identify_time_variable.explanation,
			"results": {
				"json_path": OUTPUT_PATH,
                "ret": ret
			}
        }