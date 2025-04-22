from pydantic import BaseModel

class LaTexResponse(BaseModel):
    latex_code: str