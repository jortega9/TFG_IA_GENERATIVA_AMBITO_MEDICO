import os
import sys

# Incluir ruta al proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))


from ai.phases.etl.survival.kaplan_meier.agent import KaplanMeierAgent 
from ai.phases.etl.survival.cox.agent import COXAgent 

def run_kaplan_meier_analysis() -> dict:
    """Run Kaplan-Meier survival analysis."""
    agent = KaplanMeierAgent()
    response = agent.execute()
    return response

def run_cox_analysis() -> dict:
    """Run regetion COX analysis"""
    agent = COXAgent()
    response = agent.execute()
    return response

#########################################################################################
#                                   DELETE ME                                           #
#########################################################################################   
def main() :
	print(run_cox_analysis())
    
if __name__ == "__main__":
    main()