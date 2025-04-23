import os
import sys
import shutil
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from backend.src.schemas.ai import PrepareDataRequest
from backend.src.schemas.statistics import DescRequest, AdvRequest, KaplanVRequest
import backend.src.controllers.ai_controller as controller
import ai.phases.etl.prepare_data.controller as prepare_data_controller
import ai.phases.etl.descriptive.controller as descriptive_controller
import ai.phases.etl.comparative.controller as comparative_controller
import ai.phases.test.adv1.controller as test_controller_adv1
import ai.phases.test.adv2.controller as test_controller_adv2
import ai.phases.test.adv3.controller as test_controller_adv3
import ai.phases.test.adv4.controller as test_controller_adv4
# import ai.phases.test.executeData.controller as test_controller_executeData
import ai.phases.etl.identify_analysis.controller as identify_analysis_controller
import ai.phases.etl.significant.controller as significant_controller

import ai.phases.etl.survival.controller as survival_controller

from backend.src.controllers.statistics_controller import obtener_media_std, obtener_mediana_rangoI, obtener_freq_ic95
from backend.src.controllers.statistics_controller import obtener_chi_cuadrado, obtener_fisher, obtener_mann_withney, obtener_t_student, obtener_significativas
from backend.src.controllers.statistics_controller import obtener_kaplan_general, obtener_kaplan_vars
import time
import json
from fastapi import Body

router = APIRouter()

DOC_DATA = "descripcion.docx"

@router.post('/prepare-data')
async def prepare_data(request: PrepareDataRequest):
    prepare_data_controller.execute(max_turns=100)
    return {"message": "Datos preparados exitosamente"}

@router.post('/identify-group-variable')
async def identify_group_variable():
    groupVar = identify_analysis_controller.runIdentifyGroupVariable()
    return {"result": groupVar}

@router.post('/identify-time-variable')
async def identify_time_variable():
    timeVar = identify_analysis_controller.runIdentifyTimeVariable()
    return {"result": timeVar}

@router.post("/save-config")
def save_group_config(payload: dict = Body(...), jsonPath: str = Body(...)):
    try:
        os.makedirs(os.path.dirname(jsonPath), exist_ok=True)
        with open(jsonPath, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post('/categorize-variables')
async def categorize_variables():
    categorize = identify_analysis_controller.runCategorizeVariables()
    return {"result": categorize}

@router.post('/executeDataDesc')
async def execute_data_desc():

    result = descriptive_controller.execute()
    # time.sleep(5)
    return {"result": result}

@router.post('/executeDataAdv')
async def execute_data_adv():

    chi = comparative_controller.run_chi_square_analysis()
    fisher = comparative_controller.run_fisher_exact_analysis()
    tStudent = comparative_controller.run_t_student_analysis()
    mann = comparative_controller.run_mann_whitney_u_analysis()
    significant = significant_controller.collect_significant_values()
    kaplan = survival_controller.run_kaplan_meier_analysis()
    # cox = survival_controller.run_cox_analysis()

    print("kaplan", kaplan)
    # time.sleep(5)
    return {"result": {
        "chi": chi,
        "fisher": fisher,
        "tStudent": tStudent,
        "mann": mann,
        "significant": significant,
        "kaplan": kaplan,
    }}

@router.post('/descStatistics1')
async def calc_media_desv_normal(request: DescRequest) :
    """
    Media y Desviación Típica siguiendo una Distribución Normal

    """

    result = obtener_media_std(request.excel_path)
    
    return { "result": result }

@router.post('/descStatistics2')
async def calc_mediana_rangoI(request: DescRequest) :
    """
    Mediana y Rango Intercuartílico sin swguir una Distribución Normal

    """

    result = obtener_mediana_rangoI(request.excel_path)
    return {"result": result}

@router.post('/descStatistics3')
async def calc_porcentajes_frecuencias(request: DescRequest) :
    """
    Mediana y Rango Intercuartílico sin swguir una Distribución Normal

    """

    result = obtener_freq_ic95(request.excel_path)
    return {"result": result}

@router.post('/advStatistics1')
async def calc_chi_cuadrado(request: AdvRequest) :
    """
    Realizar Análisis Categórico Chi Cuadrado

    """

    result = obtener_chi_cuadrado(request.excel_path)
    return {"result": result}

@router.post('/advStatistics2')
async def calc_fisher(request: AdvRequest) :
    """
    Realizar Análisis Categórico Fisher
    """

    result = obtener_fisher(request.excel_path)
    return {"result": result}

@router.post('/advStatistics3')
async def calc_mann_whitney(request: AdvRequest) :
    """
    Realizar Análisis Categórico Mann Whitney
    """

    result = obtener_mann_withney(request.excel_path)
    return {"result": result}

@router.post('/advStatistics4')
async def calc_t_student(request: AdvRequest) :
    """
    Realizar Análisis Categórico T Student
    """

    result = obtener_t_student(request.excel_path)
    return {"result": result}

@router.post('/advStatistics5')
async def calc_t_student(request: AdvRequest) :
    """
    Realizar Análisis Categórico T Student
    """

    result = obtener_significativas(request.excel_path)
    return {"result": result}

@router.post('/kaplanStatistics1')
async def calc_kaplan_general(request: AdvRequest) :
    """
    Realizar Análisis Categórico T Student
    """
    excel_path = request.excel_path + "/median_summary.csv"
    result = obtener_kaplan_general(excel_path)
    return {"result": result}

@router.post('/kaplanStatisticsVars')
async def calc_kaplan_vars(request: KaplanVRequest) :
    """
    Realizar Análisis Categórico T Student
    """
    excel_path = request.excel_path + f"/{request.name}_median_summary.csv"
    result = obtener_kaplan_vars(excel_path)
    return {"result": result}

@router.post('/copyDocs')
async def copy_docs(files: list[UploadFile] = File(...)):
    raw_data_path = os.path.join(os.path.dirname(__file__), '../../../data/raw')
    os.makedirs(raw_data_path, exist_ok=True)
    
    new_paths = []
    for file in files:
        if file.filename.endswith('.docx'):
            new_filename = 'descripcion.docx'
        elif file.filename.endswith('.xlsx'):
            new_filename = 'BD.xlsx'
        else:
            new_filename = file.filename

        file_path = os.path.join(raw_data_path, new_filename)
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        new_paths.append(file_path)
    
    return {"message": "Archivos copiados exitosamente", "paths": new_paths}