import os
import sys

# Incluir ruta al proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from ai.phases.etl.descriptive.agent import DescriptiveAgent

# Numeric
from ai.phases.etl.descriptive.numeric.agent import NumericDescriptiveAgent

# Categoric
from ai.phases.etl.descriptive.categoric.agent import CategoricalDescriptiveAgent

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
	agent = NumericDescriptiveAgent()
	response = agent.execute()
	return response

def run_categorical_analysis() -> dict:
	"""Call the LLM Agent for the categorical analysis.

	Returns:
		dict: returns the report and result of the categorical analysis.
	"""
	agent = CategoricalDescriptiveAgent()
	response = agent.execute()
	return response


#########################################################################################
#                                   DELETE ME                                           #
#########################################################################################   
def main() :
	print(run_numeric_analysis())
	print(run_categorical_analysis())
    
if __name__ == "__main__":
    main()