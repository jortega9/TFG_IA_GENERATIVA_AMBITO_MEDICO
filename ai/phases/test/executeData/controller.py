"""TODO: Comment"""
import pandas as pd
import configparser
import os
import json
import sys
from docx import Document
import numpy as np

from ai.phases.test.executeData.agent import TestAgentExecuteData
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from dotenv import load_dotenv
load_dotenv()


SETTINGS_PATH = os.getenv("SETTINGS_PATH")
RAW_DATA = "BD.xlsx"
JSON_DATA = "variables_dataset_actualizado.json"
DOC_DATA = "descripcion.docx"
MASTER_PATH = "master.json"

config = configparser.ConfigParser()

config.read(SETTINGS_PATH)   


def execute(max_turns: int) -> list:
    """Execute the agent workflow.

    Args:
        max_turns (int): Maximum number of turns.

    Returns:
        list: List of results.
    """
    agent = TestAgentExecuteData()
    return agent.run(max_turns=max_turns)
    
