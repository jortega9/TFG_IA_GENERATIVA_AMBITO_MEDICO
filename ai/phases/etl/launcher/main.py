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
from ai.phases.etl.survival.cox.agent import COXAgent


def main() :
    """A full execute run of the stadistic analysis."""
    print("=========================")
    # Prepara el dataset
    PrepareDataAgent().execute()
    print("=========================")
    # Identifica la variable de grupo
    print(IdentifyGroupVariableAgent().execute())
    input("Antes de continuar, revisa la variable de grupo (o variable objetivo), si está mal, cámbiala.")
    print("=========================")
    # Categoriza las variables por tipo y test
    print(CategorizeVariablesAgent().execute())
    print("=========================")
    # Realiza el analisis estadistico descriptivo numerico
    print(NumericDescriptiveAgent().execute())
    print("=========================")
    # Realiza el analisis estadistico descriptivo categorico
    print(CategoricalDescriptiveAgent().execute())
    print("=========================")
    # Realiza el test de chi cuadrado
    print(ChiSquareComparativeAgent().execute())
    print("=========================")
    # Realiza el test exacto de fisher
    print(FisherExactComparativeAgent().execute())
    print("=========================")
    # Realiza el test t Student
    print(TStudentComparativeAgent().execute())
    print("=========================")
    # Realiza el test mann whitney u
    print(MannWhitneyComparativeAgent().execute())
    print("=========================")
    # Realiza la elección de variable de tiempo o de seguimiento
    print(IdentifyTimeVariableAgent().execute())
    input("Antes de continuar, revisa la variable de tiempo (o variable de seguimiento), si está mal, cámbiala.")
    print("=========================")
    # Recolecta todas las variables significativas
    print(CollectSignificantVariables().execute())
    print("=========================")
    # Realiza el analisis de supervivencia mediante curvas de supervivencia Kaplan Meier
    print(KaplanMeierAgent().execute())
    # Realiza el analisis de supervivencia con regresion de COX
    print(COXAgent().execute())

if __name__ == "__main__":
    main()