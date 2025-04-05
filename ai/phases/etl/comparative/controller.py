import os
import sys

# Incluir ruta al proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))


# Categoric
from ai.phases.etl.comparative.categorical.agent import ComparativeCategoricalAgent

def execute() -> dict:
	"""Main call to the API.

	Returns:
		dict: returns the reports and results.
	"""
	return {}

def run_categorical_analysis() -> dict:
	"""Call the LLM Agent for the numeric analysis.

	Returns:
		dict: returns the report and result of the numeric analysis.
	"""
	agent = ComparativeCategoricalAgent()
	response = agent.execute()
	return response

#########################################################################################
#                                   DELETE ME                                           #
#########################################################################################   
def main() :
	print(run_categorical_analysis())
    
if __name__ == "__main__":
    main()