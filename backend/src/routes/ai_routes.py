import os
import sys
import shutil
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from backend.src.schemas.ai import PrepareDataRequest
# import backend.src.controllers.ai_controller as controller
# import ai.phases.etl.prepare_data.controller as prepare_data_controller

router = APIRouter()

@router.post('/prepare-data')
async def prepare_data(request: PrepareDataRequest):
    # prepare_data_controller.controller(
    #     master_path=request.master_path,
    #     excel_path=request.excel_path
    # )
    # print(request)
    return {"message": "Datos preparados exitosamente"}

@router.post('/copyDocs')
async def copy_docs(files: list[UploadFile] = File(...)):
    raw_data_path = os.path.join(os.path.dirname(__file__), '../../../data/raw')
    os.makedirs(raw_data_path, exist_ok=True)
    
    for file in files:
        file_path = os.path.join(raw_data_path, file.filename)
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
    
    return {"message": "Archivos copiados exitosamente"}