import os
import sys

# Incluir ruta al proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))


from ai.phases.etl.survival.agent import SurvivalAnalysisAgent

def execute() -> dict:
	"""Main call to the API.

	Returns:
		dict: Results of the API call.
	"""
	agent = SurvivalAnalysisAgent()
	response = agent.execute()
	return response


#########################################################################################
#                                   DELETE ME                                           #
#########################################################################################   
def main() :
	print(execute())
    
if __name__ == "__main__":
    main()