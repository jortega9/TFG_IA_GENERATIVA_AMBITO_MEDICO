import os
import sys

# Incluir ruta al proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))


# Categoric
from ai.phases.etl.identify_analysis.categorize.agent import CategorizeVariablesAgent


#########################################################################################
#                                   DELETE ME                                           #
#########################################################################################   
def main() :
    agent = CategorizeVariablesAgent()
    print(agent.execute())
    
if __name__ == "__main__":
    main()
            