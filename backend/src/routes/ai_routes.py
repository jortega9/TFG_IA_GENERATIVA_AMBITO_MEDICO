import os
import sys
import shutil
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from backend.src.schemas.ai import PrepareDataRequest
import backend.src.controllers.ai_controller as controller
import ai.phases.etl.prepare_data.controller as prepare_data_controller
import ai.phases.test.desc1.controller as test_controller_desc1
import ai.phases.test.desc2.controller as test_controller_desc2
import ai.phases.test.desc3.controller as test_controller_desc3
import ai.phases.test.adv1.controller as test_controller_adv1
import ai.phases.test.adv2.controller as test_controller_adv2
import ai.phases.test.adv3.controller as test_controller_adv3
import ai.phases.test.adv4.controller as test_controller_adv4
import ai.phases.test.executeData.controller as test_controller_executeData

router = APIRouter()

@router.post('/prepare-data')
async def prepare_data(request: PrepareDataRequest):
    prepare_data_controller.controller(
        master_path=request.master_path,
        excel_path=request.excel_path
    )
    print(request)
    return {"message": "Datos preparados exitosamente"}

@router.post('/testExecuteData')
async def execute_data():
    # result = prepare_data_controller.execute(max_turns=100)

    result = test_controller_executeData.execute(max_turns=100)
    return {"result": result}

@router.post('/testDescStatistics1')
async def calc_media_desv_normal() :
    """
    Media y Desviación Típica siguiendo una Distribución Normal

    """

    result = test_controller_desc1.execute(max_turns=100)
    return {"result": result}

@router.post('/testDescStatistics2')
async def calc_mediana_rangoI() :
    """
    Mediana y Rango Intercuartílico sin swguir una Distribución Normal

    """

    result = test_controller_desc2.execute(max_turns=100)
    return {"result": result}

@router.post('/testDescStatistics3')
async def calc_porcentajes_frecuencias() :
    """
    Mediana y Rango Intercuartílico sin swguir una Distribución Normal

    """

    result = test_controller_desc3.execute(max_turns=100)
    return {"result": result}

@router.post('/testAdvStatistics1')
async def calc_correlacion_resultados() :
    """
    Determinar correlación entre resultados inmunohistoquímicos y resto de variables.

    Mediante t student, Test chi cuadrado de Pearson y Test exacto de Fisher

    """

    result = test_controller_adv1.execute(max_turns=100)
    return {"result": result}

@router.post('/testAdvStatistics2')
async def calc_recaida_tiempo() :
    """
    Determinar correlación entre resultados inmunohistoquímicos y resto de variables.

    Mediante t student, Test chi cuadrado de Pearson y Test exacto de Fisher

    """

    result = test_controller_adv2.execute(max_turns=100)
    return {"result": result}

@router.post('/testAdvStatistics3')
async def calc_porcentajes_frecuencias() :
    """
    Determinar correlación entre resultados inmunohistoquímicos y resto de variables.

    Mediante t student, Test chi cuadrado de Pearson y Test exacto de Fisher

    """

    result = test_controller_adv3.execute(max_turns=100)
    return {"result": result}

@router.post('/testAdvStatistics4')
async def calc_porcentajes_frecuencias() :
    """
    Determinar correlación entre resultados inmunohistoquímicos y resto de variables.

    Mediante t student, Test chi cuadrado de Pearson y Test exacto de Fisher

    """

    result = test_controller_adv4.execute(max_turns=100)
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