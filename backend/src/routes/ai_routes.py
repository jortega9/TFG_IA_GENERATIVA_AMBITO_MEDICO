import os
import sys
import shutil
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from backend.src.schemas.ai import PrepareDataRequest
from backend.src.schemas.statistics import DescRequest, AdvRequest
import backend.src.controllers.ai_controller as controller
import ai.phases.etl.prepare_data.controller as prepare_data_controller
import ai.phases.etl.descriptive.controller as descriptive_controller
import ai.phases.etl.comparative.controller as comparative_controller
import ai.phases.test.adv1.controller as test_controller_adv1
import ai.phases.test.adv2.controller as test_controller_adv2
import ai.phases.test.adv3.controller as test_controller_adv3
import ai.phases.test.adv4.controller as test_controller_adv4
# import ai.phases.test.executeData.controller as test_controller_executeData

from backend.src.controllers.statistics_controller import obtener_media_std, obtener_mediana_rangoI, obtener_freq_ic95, det_corr_vars

import time

router = APIRouter()

DOC_DATA = "descripcion.docx"

@router.post('/prepare-data')
async def prepare_data(request: PrepareDataRequest):
    prepare_data_controller.execute(max_turns=100)
    print(request)
    return {"message": "Datos preparados exitosamente"}

@router.post('/executeDataDesc')
async def execute_data_desc():

    result = descriptive_controller.execute()
    # time.sleep(5)
    return {"result": result}

@router.post('/executeDataAdv')
async def execute_data_adv():

    result = comparative_controller.execute()
    print(result)
    # time.sleep(5)
    return {"result": result}

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
async def calc_correlacion_resultados(request: AdvRequest) :
    #TODO
    """
    Determinar correlación entre resultados inmunohistoquímicos y resto de variables.

    Mediante t student, Test chi cuadrado de Pearson y Test exacto de Fisher

    """

    result = det_corr_vars()
    time.sleep(5)
    return {"result": result}

@router.post('/testAdvStatistics2')
async def calc_recaida_tiempo() :
    """
    Determinar correlación entre resultados inmunohistoquímicos y resto de variables.

    Mediante t student, Test chi cuadrado de Pearson y Test exacto de Fisher

    """

    result = test_controller_adv2.execute(max_turns=100)
    time.sleep(5)
    return {"result": result}

@router.post('/testAdvStatistics3')
async def analiz_curvas_supervivencia() :
    """
    Determinar correlación entre resultados inmunohistoquímicos y resto de variables.

    Mediante t student, Test chi cuadrado de Pearson y Test exacto de Fisher

    """

    result = test_controller_adv3.execute(max_turns=100)
    time.sleep(5)
    return {"result": result}

@router.post('/testAdvStatistics4')
async def det_vars_riesgo_recaida() :
    """
    Determinar correlación entre resultados inmunohistoquímicos y resto de variables.

    Mediante t student, Test chi cuadrado de Pearson y Test exacto de Fisher

    """

    result = test_controller_adv4.execute(max_turns=100)
    time.sleep(5)
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