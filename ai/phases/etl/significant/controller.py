import os
import sys

# Incluir ruta al proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from ai.phases.etl.significant.agent import CollectSignificantVariables

def collect_significant_values() -> dict:
    """Calls the execute function of the LLM agent to do the t student test

    Returns:
        dict: returns the dict with the reports and results.
    """
    agent = CollectSignificantVariables()
    response = agent.execute()
    return response


#########################################################################################
#                                   DELETE ME                                           #
#########################################################################################   
def main() :
	print(collect_significant_values())
    
if __name__ == "__main__":
    main()