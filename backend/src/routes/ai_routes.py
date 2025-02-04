import os
from fastapi import APIRouter
from fastapi.responses import FileResponse
from schemas.ai import XLSXRequest
import controllers.ai_controller as controller

router = APIRouter()

@router.get("/convert-xlsx")
def convert_xlsx_endpoint(request: XLSXRequest):
    """TODO: Comment this docstring
    """
    
    csv_path = controller.convert_xlsx(request.file_path)

    return FileResponse(csv_path, filename=os.path.basename(csv_path), media_type="text/csv")