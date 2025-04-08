from pydantic import BaseModel
from typing import Literal, List

class VariableDecisionSchema(BaseModel):
    variable: str
    description: str
    test_sugerido: Literal["t-student", "mann-whitney"]

class DecisionTestSchema(BaseModel):
    """Pydantic schema."""
    explanation: str
    list: List[VariableDecisionSchema]