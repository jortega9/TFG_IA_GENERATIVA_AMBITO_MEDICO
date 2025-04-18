import os
import sys

# Incluir ruta al proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))


from ai.phases.etl.survival.kaplan_meier.agent import KaplanMeierAgent 

def run_kaplan_meier_analysis() -> dict:
    """Run Kaplan-Meier survival analysis."""
    agent = KaplanMeierAgent()
    response = agent.execute()
    return response


#########################################################################################
#                                   DELETE ME                                           #
#########################################################################################   
def main() :
	print(run_kaplan_meier_analysis())
    
if __name__ == "__main__":
    main()