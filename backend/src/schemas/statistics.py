"""Schemas for the statistics."""
from pydantic import BaseModel

class DescRequest(BaseModel):
    excel_path: str

class AdvRequest(BaseModel):
    csvMannWhitneyPath: str
    csvTStudentPath: str
    csvChiPath: str
    csvFisherPath: str
    