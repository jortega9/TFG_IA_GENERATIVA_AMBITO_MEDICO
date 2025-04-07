"""Agent class for the Stadistic Advanced part."""
import configparser
import io
import json
import os
import re

import pandas as pd
import numpy as np

from dotenv import load_dotenv

from ai.agents.agent import Agent
from ai.phases.etl.advance.prompts import AGENT_WORKFLOW

load_dotenv()

SETTINGS_PATH = os.getenv("SETTINGS_PATH")