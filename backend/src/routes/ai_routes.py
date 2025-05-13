import os
import sys
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse



sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from backend.src.schemas.ai import PrepareDataRequest
from backend.src.schemas.statistics import DescRequest, AdvRequest, KaplanVRequest
import ai.phases.etl.prepare_data.controller as prepare_data_controller
import ai.phases.etl.descriptive.controller as descriptive_controller
import ai.phases.etl.comparative.controller as comparative_controller
import ai.phases.etl.identify_analysis.controller as identify_analysis_controller
import ai.phases.etl.significant.controller as significant_controller

import ai.phases.etl.survival.controller as survival_controller

from backend.src.controllers.docs_controller import get_kaplanImage, zip_download, upload_files
from backend.src.controllers.statistics_controller import obtener_media_std, obtener_mediana_rangoI, obtener_freq_ic95
from backend.src.controllers.statistics_controller import obtener_chi_cuadrado, obtener_fisher, obtener_mann_withney, obtener_t_student, obtener_significativas
from backend.src.controllers.statistics_controller import obtener_kaplan_general, obtener_kaplan_vars, obtener_cox_uni
from ai.phases.conclusions.orchestrator import generate_latex_document

import time
import json
from fastapi import Body
import configparser
from dotenv import load_dotenv

router = APIRouter()

load_dotenv()

SETTINGS_PATH = os.getenv("SETTINGS_PATH")
KAPLAN = os.getenv("KAPLAN")
PROC = os.getenv("PROC")

config = configparser.ConfigParser()
config.read(SETTINGS_PATH)

DOC_DATA = "descripcion.docx"
MASTER_DIR = os.path.join(config["frontend_path"]["public_path"], "master")

@router.post('/prepare-data')
async def prepare_data(request: PrepareDataRequest):
    """
    Preparar los datos para el análisis
    """
    prepare_data_controller.execute(max_turns=100)
    return {"message": "Datos preparados exitosamente"}

@router.post('/identify-group-variable')
async def identify_group_variable():
    """
    Identificar la variable de grupo
    """
    groupVar = identify_analysis_controller.runIdentifyGroupVariable()
    return {"result": groupVar}

@router.post('/identify-time-variable')
async def identify_time_variable():
    """
    Identificar la variable de tiempo
    """
    timeVar = identify_analysis_controller.runIdentifyTimeVariable()
    return {"result": timeVar}

@router.post("/save-config")
def save_group_config(payload: dict = Body(...), jsonPath: str = Body(...)):
    """
    Guardar configuración de variables en un archivo JSON
    """
    try:
        os.makedirs(os.path.dirname(jsonPath), exist_ok=True)
        with open(jsonPath, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post('/categorize-variables')
async def categorize_variables():
    """
    Ejecutar Categorización de variables
    """
    categorize = identify_analysis_controller.runCategorizeVariables()
    return {"result": categorize}

@router.post('/executeDataDesc')
async def execute_data_desc():
    """
    Ejecutar análisis estadísticos descriptivos
    Entre ellos:
    - Media
    - Desviación Típica
    - Mediana
    - Rango Intercuartílico
    - Frecuencias Absolutas
    - Intervalos de Confianza al 95%
    """

    result = descriptive_controller.execute()
    # time.sleep(5)
    return {"result": result}

@router.post('/executeDataAdv')
async def execute_data_adv():
    """
    Ejecutar análisis estadísticos comparativos y de supervivencia
    Entre ellos:
    - Chi Cuadrado
    - Fisher
    - T Student
    - Mann Whitney
    - Significativas
    - Kaplan Meier
    - Cox
    """

    chi = comparative_controller.run_chi_square_analysis()
    fisher = comparative_controller.run_fisher_exact_analysis()
    tStudent = comparative_controller.run_t_student_analysis()
    mann = comparative_controller.run_mann_whitney_u_analysis()
    significant = significant_controller.collect_significant_values()
    kaplan = survival_controller.run_kaplan_meier_analysis()
    cox = survival_controller.run_cox_analysis()

    print("cox", cox)
    # time.sleep(5)
    return {"result": {
        "chi": chi,
        "fisher": fisher,
        "tStudent": tStudent,
        "mann": mann,
        "significant": significant,
        "kaplan": kaplan,
        "cox": cox
    }}

@router.post('/descStatistics1')
async def calc_media_desv_normal(request: DescRequest) :
    """
    Obtener resultados de media y desviación típica siguiendo una Distribución Normal de las variables numéricas

    """

    result = obtener_media_std(request.excel_path)
    
    return { "result": result }

@router.post('/descStatistics2')
async def calc_mediana_rangoI(request: DescRequest) :
    """
    Obtener resultados de mediana y rango intercuartílico sin seguir una Distribución Normal de las variables numéricas

    """

    result = obtener_mediana_rangoI(request.excel_path)
    return {"result": result}

@router.post('/descStatistics3')
async def calc_porcentajes_frecuencias(request: DescRequest) :
    """
    Obtener resultados de frecuencias absolutas e intervalos de confianza al 95% para las variables categóricas

    """

    result = obtener_freq_ic95(request.excel_path)
    return {"result": result}

@router.post('/advStatistics1')
async def calc_chi_cuadrado(request: AdvRequest) :
    """
    Obtener resultados de análisis categórico Chi Cuadrado

    """

    result = obtener_chi_cuadrado(request.excel_path)
    return {"result": result}

@router.post('/advStatistics2')
async def calc_fisher(request: AdvRequest) :
    """
    Obtener resultados de análisis categórico Fisher
    """

    result = obtener_fisher(request.excel_path)
    return {"result": result}

@router.post('/advStatistics3')
async def calc_mann_whitney(request: AdvRequest) :
    """
    Obtener resultados de análisis numérico Mann Whitney
    """

    result = obtener_mann_withney(request.excel_path)
    return {"result": result}

@router.post('/advStatistics4')
async def calc_t_student(request: AdvRequest) :
    """
    Obtener resultados de los análisis numérico de T Student
    """

    result = obtener_t_student(request.excel_path)
    return {"result": result}

@router.post('/advStatistics5')
async def calc_t_student(request: AdvRequest) :
    """
    Obtener resultados de los análisis de las variables significativas
    """

    result = obtener_significativas(request.excel_path)
    return {"result": result}

@router.post('/kaplanStatistics1')
async def calc_kaplan_general(request: AdvRequest) :
    """
    Obtener resultados del análisis de supervivencia de Kaplan-Meier general
    """
    excel_path = request.excel_path + "/median_summary.csv"
    result = obtener_kaplan_general(excel_path)
    return {"result": result}

@router.post('/kaplanStatisticsVars')
async def calc_kaplan_vars(request: KaplanVRequest) :
    """
    Obtener resultados del análisis de supervivencia de Kaplan-Meier para cada variable estratificada
    """
    excel_path = request.excel_path + f"/{request.name}_median_summary.csv"
    result = obtener_kaplan_vars(excel_path)
    return {"result": result}

@router.post('/coxStatistics')
async def calc_cox_uni(request: AdvRequest) :
    """
    Obtener resultados del modelo de regresión de Cox Univariante
    """

    result = obtener_cox_uni(request.excel_path)
    return {"result": result}

@router.post('/documentGenerator')
async def generate_document():
    """
    Generar Documento PDF con los resultados de los análisis estadísticos realizados
    """

    generate_latex_document()
    return {"result": "http://localhost:5173/pdf/final_report.pdf"}

@router.post('/copyDocs')
async def copy_docs(files: list[UploadFile] = File(...)):
    """
    Copiar archivos proporcionados por el usuario a la carpeta de trabajo.
    """
    return await upload_files(files)

@router.post('/download-zip')
async def download_zip():
    """
    Generar un archivo ZIP con los resultados de las estadisticas y descargarlo
    """
    return await zip_download()

@router.get('/kaplan-image/{image_name}')
async def get_kaplan_image(image_name: str):
    """
    Obtener imagen de Kaplan-Meier
    """
    return await get_kaplanImage(image_name)
