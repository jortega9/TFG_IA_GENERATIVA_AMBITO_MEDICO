import os
import sys

# Incluir ruta al proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))


from ai.phases.etl.comparative.categorical.chi_square import ChiSquareComparativeAgent
from ai.phases.etl.comparative.categorical.fisher import FisherExactComparativeAgent

from ai.phases.etl.comparative.numerical.mann_whitney import MannWhitneyComparativeAgent
from ai.phases.etl.comparative.numerical.t_student import TStudentComparativeAgent

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

def run_mann_whitney_u_analysis() -> dict:
    """Calls the execute function of the LLM agent to do the mann whitney u test

    Returns:
        dict: returns the dict with the reports and results.
    """
    agent = MannWhitneyComparativeAgent()
    response = agent.execute()
    return response

def run_t_student_analysis() -> dict:
    """Calls the execute function of the LLM agent to do the t student test

    Returns:
        dict: returns the dict with the reports and results.
    """
    agent = TStudentComparativeAgent()
    response = agent.execute()
    return response

#########################################################################################
#                                   DELETE ME                                           #
#########################################################################################   
def main() :
	print(run_t_student_analysis())
    
if __name__ == "__main__":
    main()