import os
import sys

# Incluir ruta al proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))


# Categoric
from ai.phases.etl.comparative.categorical.agent import ComparativeCategoricalAgent
from ai.phases.etl.comparative.numerical.agent import ComparativeNumericalAgent

from ai.phases.etl.comparative.categorical.chi_square import ChiSquareComparativeAgent
from ai.phases.etl.comparative.categorical.fisher import FisherExactComparativeAgent

def execute() -> dict:
    """Main call to the API. EXECUTE THIS FUNCTION!"""
    categorical_response = run_categorical_analysis()
    print(categorical_response)
    numerical_response = run_numerical_analysis({ 
        "name": categorical_response["results"]["group_variable"], 
        "valid_keys": categorical_response["results"]["valid_keys"],
        }
    )
    return {
        "categorical_analysis": categorical_response,
        "numerical_analysis": numerical_response
    }


def run_categorical_analysis() -> dict:
	"""Call the LLM Agent for the numeric analysis.

	Returns:
		dict: returns the report and result of the numeric analysis.
	"""
	agent = ComparativeCategoricalAgent()
	response = agent.execute()
	return response

def run_numerical_analysis(group_variable: dict) -> dict:
    if not group_variable :
        return { "error" : "You have to execute run_categorical_analysis first"}
    agent = ComparativeNumericalAgent(group_variable=group_variable)
    response = agent.execute()
    return response

def run_chi_square_analysis() -> dict:
    """Calls the execute function of the LLM agent to do the chi square test

    Returns:
        dict: returns the dict with the reports and results.
    """
    agent = ChiSquareComparativeAgent()
    response = agent.execute()
    return response

def run_fisher_exact_analysis() -> dict:
    """Calls the execute function of the LLM agent to do the fisher exact test

    Returns:
        dict: returns the dict with the reports and results.
    """
    agent = FisherExactComparativeAgent()
    response = agent.execute()
    return response  

#########################################################################################
#                                   DELETE ME                                           #
#########################################################################################   
def main() :
	print(run_fisher_exact_analysis())
    
if __name__ == "__main__":
    main()