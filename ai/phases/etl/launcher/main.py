import os
import sys

# Incluir ruta al proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from ai.phases.etl.prepare_data.agent import PrepareDataAgent
from ai.phases.etl.identify_analysis.group_variable.agent import IdentifyGroupVariableAgent
from ai.phases.etl.identify_analysis.categorize.agent import CategorizeVariablesAgent
from ai.phases.etl.descriptive.numeric.agent import NumericDescriptiveAgent
from ai.phases.etl.descriptive.categoric.agent import CategoricalDescriptiveAgent
from ai.phases.etl.comparative.categorical.chi_square import ChiSquareComparativeAgent
from ai.phases.etl.comparative.categorical.fisher import FisherExactComparativeAgent
from ai.phases.etl.comparative.numerical.t_student import TStudentComparativeAgent
from ai.phases.etl.comparative.numerical.mann_whitney import MannWhitneyComparativeAgent
from ai.phases.etl.identify_analysis.time_variable.agent import IdentifyTimeVariableAgent
from ai.phases.etl.significant.agent import CollectSignificantVariables
from ai.phases.etl.survival.kaplan_meier.agent import KaplanMeierAgent


def main() :
    """A full execute run of the stadistic analysis."""
    print("=========================")
    # Prepara el dataset
    PrepareDataAgent().execute_prepare_data()
    print("=========================")
    # Identifica la variable de grupo
    IdentifyGroupVariableAgent().execute()
    input("Antes de continuar, revisa la variable de grupo (o variable objetivo), si está mal, cámbiala.")
    print("=========================")
    # Categoriza las variables por tipo y test
    CategorizeVariablesAgent().execute()
    print("=========================")
    # Realiza el analisis estadistico descriptivo numerico
    NumericDescriptiveAgent().execute()
    print("=========================")
    # Realiza el analisis estadistico descriptivo categorico
    CategoricalDescriptiveAgent().execute()
    print("=========================")
    # Realiza el test de chi cuadrado
    ChiSquareComparativeAgent().execute()
    print("=========================")
    # Realiza el test exacto de fisher
    FisherExactComparativeAgent().execute()
    print("=========================")
    # Realiza el test t Student
    TStudentComparativeAgent().execute()
    print("=========================")
    # Realiza el test mann whitney u
    MannWhitneyComparativeAgent().execute()
    print("=========================")
    # Realiza la elección de variable de tiempo o de seguimiento
    IdentifyTimeVariableAgent().execute()
    input("Antes de continuar, revisa la variable de tiempo (o variable de seguimiento), si está mal, cámbiala.")
    print("=========================")
    # Recolecta todas las variables significativas
    CollectSignificantVariables().execute()
    print("=========================")
    # Realiza el analisis de supervivencia mediante curvas de supervivencia Kaplan Meier
    KaplanMeierAgent().execute()

if __name__ == "__main__":
    main()