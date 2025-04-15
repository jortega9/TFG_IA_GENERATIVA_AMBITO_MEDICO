from pydantic import BaseModel
from typing import Literal, List

class VariableSchema(BaseModel):
    variable: str
    descripcion: str
    tipo: Literal["numérica", "categórica"]
    test_usado: str
    p_valor: float
    significativa: bool
    justificacion: str
    
class IdentifyVariableSchema(BaseModel):
    list: List[VariableSchema]