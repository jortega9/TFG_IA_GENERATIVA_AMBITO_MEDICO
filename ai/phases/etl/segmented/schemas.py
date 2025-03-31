from typing import Any, Optional
from pydantic import BaseModel

class Description(BaseModel):
    """Schema for the JSON master.

    Args:
        BaseModel (BaseModel): Pydantic model for validation.

    Attributes:
        descripcion (str): Description of the field.
        valores (Optional[Any]): Values associated with the field, can be None.

    Example:
        {
        	"descripcion": "Nº historia",
            "valores": null
        }
    """

    descripcion: str
    valores: Optional[Any] = None

class PrepareData(Description):
    """_summary_

     Args:
        Description (Description): JSON description.
    """
    
    name: str
    description: Description