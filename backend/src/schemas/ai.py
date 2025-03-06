"""Schemas for the AI Module."""
from pydantic import BaseModel

class PrepareDataRequest(BaseModel):
    master_path: str
    excel_path: str