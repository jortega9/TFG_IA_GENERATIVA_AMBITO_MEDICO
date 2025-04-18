from pydantic import BaseModel

from typing import List

class IdentifyTimeSchema(BaseModel):
    """Schema for the variable identified."""
    name:str
    other_options: List[str]