from typing import Any, Optional, Dict
from pydantic import BaseModel

class Description(BaseModel):
    """Schema for the JSON master."""

    descripcion: str
    valores: Optional[Any] = None

class Master(BaseModel):
    """Schema for the JSON master containing multiple descriptions."""

    column_name: str
    column_info: Description