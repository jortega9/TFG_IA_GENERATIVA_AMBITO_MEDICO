from typing import Optional, Dict, List
from pydantic import BaseModel

class Description(BaseModel):
    """Schema for the JSON master."""

    descripcion: str
    valores: Optional[Dict[str, str]] = None

class Variable(BaseModel):
    """Schema for the JSON master containing multiple descriptions."""

    column_name: str
    column_info: Description
    
class Master(BaseModel):
    """Schema for the json master."""
    column: List[Variable]