import os
from fastapi import APIRouter
from fastapi.responses import FileResponse
from schemas.ai import PrepareDataRequest
import controllers.ai_controller as controller
import ai.phases.etl.prepare_data.controller as prepare_data_controller

router = APIRouter()

@router.get("/prepare-data")
def prepare_data_endpoint(
    request: PrepareDataRequest
    ) -> str:
    """Endpoint that receives the master path and the excel path and 
    prepare the data

    Args:
        request (PrepareDataRequest): file paths

    Returns:
        str: return message
    """
    prepare_data_controller.controller(
        master_path=PrepareDataRequest.master_path, 
        excel_path=PrepareDataRequest.excel_path
    )
    
    return "Data ready."
