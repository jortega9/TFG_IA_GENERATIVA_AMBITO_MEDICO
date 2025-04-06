"""Schemas for the statistics."""
from pydantic import BaseModel

class DescRequest(BaseModel):
    excel_path: str