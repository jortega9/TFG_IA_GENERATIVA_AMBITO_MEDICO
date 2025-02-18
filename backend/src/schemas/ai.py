"""Schemas for the AI Module."""
from pydantic import BaseModel

class XLSXRequest(BaseModel):
    file_path: str