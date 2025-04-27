import os
import sys
import subprocess
import configparser
from dotenv import load_dotenv

from concurrent.futures import ThreadPoolExecutor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

load_dotenv()

SETTINGS_PATH = os.getenv("SETTINGS_PATH")

config = configparser.ConfigParser()
config.read(SETTINGS_PATH)

OUTPUT_DIR = os.path.join(config["data_path"]["processed_path"], "output")
PDF_DIR = os.path.join(config["frontend_path"]["public_path"], "pdf")

from ai.phases.conclusions.agents.cover import generate_cover
from ai.phases.conclusions.agents.dataset_description import generate_dataset_description
from ai.phases.conclusions.agents.target_variable import generate_target_variable
from ai.phases.conclusions.agents.numeric_summary import generate_numeric_summary
from ai.phases.conclusions.agents.categorical_summary import generate_categorical_summary
from ai.phases.conclusions.agents.chi_squared import generate_chi_squared
from ai.phases.conclusions.agents.fisher_exact import generate_fisher_exact
from ai.phases.conclusions.agents.t_student import generate_t_student
from ai.phases.conclusions.agents.mann_whitney import generate_mann_whitney
from ai.phases.conclusions.agents.comparative_significance import generate_comparative_significance
from ai.phases.conclusions.agents.time_variable import generate_time_variable
from ai.phases.conclusions.agents.kaplan_meier import generate_kaplan_meier
from ai.phases.conclusions.agents.kaplan_meier_summary import generate_kaplan_meier_summary
from ai.phases.conclusions.agents.log_rank import generate_log_rank
from ai.phases.conclusions.agents.cox_regression import generate_cox_regression


AGENTS = {
    "cover": generate_cover,
    "dataset": generate_dataset_description,
    "target": generate_target_variable,
    "num_summary": generate_numeric_summary,
    "cat_summary": generate_categorical_summary,
    "chi2": generate_chi_squared,
    "fisher": generate_fisher_exact,
    "t_student": generate_t_student,
    "mann_whitney": generate_mann_whitney,
    "comparative_summary": generate_comparative_significance,  
    "time_variable": generate_time_variable,
    "km_summary": generate_kaplan_meier_summary,
    "km_analysis": generate_kaplan_meier,
    "log_rank": generate_log_rank,
    "cox": generate_cox_regression,
}

ORDER = [
    "cover",
    "dataset",
    "target",
    "num_summary",
    "cat_summary",
    "chi2",
    "fisher",
    "t_student",
    "mann_whitney",
    "comparative_summary",
    "time_variable",
    "km_summary",
    "km_analysis",
    "log_rank",
    "cox",
]

def generate_latex_document():
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(AGENTS[name]) for name in ORDER]
        sections = [future.result() for future in futures]

    latex_content = r"""
\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[spanish]{babel}
\usepackage{geometry}
\geometry{margin=2.5cm}
\usepackage{setspace}
\onehalfspacing
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{float}
\usepackage{amsmath}
\usepackage{caption}
\usepackage{hyperref}
\usepackage{lmodern}

\begin{document}

%s

\end{document}
""" % (''.join(sections))

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    tex_path = os.path.join(OUTPUT_DIR, "final_report.tex")
    with open(tex_path, "w") as f:
        f.write(latex_content)
        
    os.makedirs(PDF_DIR, exist_ok=True)

    subprocess.run(["pdflatex", "-interaction=nonstopmode", "-output-directory", PDF_DIR, tex_path])

if __name__ == "__main__":
    generate_latex_document()
