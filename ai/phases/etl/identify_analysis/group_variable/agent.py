"""Agent that identify the group varaibles"""

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
from ai.phases.etl.identify_analysis.group_variable.prompts import (
    IDENTIFY_GROUP_VARIABLE,
)
from ai.phases.etl.identify_analysis.group_variable.schemas import GroupVariableSchema

load_dotenv()

SETTINGS_PATH = os.getenv("SETTINGS_PATH")

config = configparser.ConfigParser()

config.read(SETTINGS_PATH)

MASTER_PATH = os.path.join(config["data_path"]["processed_path"], "master.json")
DF_PATH = os.path.join(config["data_path"]["processed_path"], "dataset.csv")

OUTPUT_PATH = os.path.join(config["data_path"]["processed_path"], "variable_grupo.json")

class IdentifyGroupVariableAgent(Agent):
    """Comparative Categorical Stadistic Analysis LLM Agent."""

    def __init__(self):
        super().__init__()
        self.df = pd.read_csv(DF_PATH)
        with open(MASTER_PATH, "r", encoding="utf-8") as f:
            self.master = json.load(f)

    def execute(self) -> dict:
        """Main call to the LLM Agent.

        Returns:
            dict:
        """
        identify_group_variable = self.call_llm(
            prompt=IDENTIFY_GROUP_VARIABLE.format(
                master=json.dumps(self.master),
                sample=self.df.sample(n=200).to_string(),
            ),
            response_format=GroupVariableSchema,
        )
        
        ret = {
			"group_variable" : identify_group_variable.group_variable,
			"valid_keys": identify_group_variable.valid_keys
		}

        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(ret, f, ensure_ascii=False, indent=2)
            
        return {
			"explanation": identify_group_variable.explanation,
			"results": {
				"json_path": OUTPUT_PATH
			}
		}
