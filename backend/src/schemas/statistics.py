"""Schemas for the statistics."""
from pydantic import BaseModel

class DescRequest(BaseModel):
    excel_path: str

class AdvRequest(BaseModel):
    excel_path: str

class KaplanVRequest(BaseModel):
    excel_path: str
    name: str
    