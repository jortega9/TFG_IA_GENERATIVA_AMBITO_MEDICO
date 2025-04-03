import os
import sys

# Incluir ruta al proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from ai.phases.etl.descriptive.agent import DescriptiveAgent

# Numeric
from ai.phases.etl.descriptive.numeric.context import DataContext as numeric_data_context
from ai.phases.etl.descriptive.numeric.tools import create_tools as numeric_create_tools
from ai.phases.etl.descriptive.numeric.prompts import AGENT_WORKFLOW as NUMERIC_WORKFLOW

# Categoric
from ai.phases.etl.descriptive.categoric.context import DataContext as categoric_data_context
from ai.phases.etl.descriptive.categoric.tools import create_tools as categoric_create_tools
from ai.phases.etl.descriptive.categoric.prompts import AGENT_WORKFLOW as CATEGORIC_WORKFLOW

def execute() -> dict:
	"""Main call to the API.

	Returns:
		dict: returns the reports and results.
	"""
	return {}

def run_numeric_analysis() -> dict:
	"""Call the LLM Agent for the numeric analysis.

	Returns:
		dict: returns the report and result of the numeric analysis.
	"""
	data_context = numeric_data_context()
	tools = numeric_create_tools(data_context)
	agent = DescriptiveAgent(
		data_context=data_context,
		tools=tools,
		agent_workflow=NUMERIC_WORKFLOW
	)
	response = agent.execute(user_input="Comienza el análisis descriptivo numérico.")
	return {"response" : response}

#########################################################################################
#                                   DELETE ME                                           #
#########################################################################################   
def main() :
	print(run_numeric_analysis())
    
if __name__ == "__main__":
    main()