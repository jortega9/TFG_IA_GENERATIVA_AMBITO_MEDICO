from pydantic import BaseModel, ValidationError
from typing import Optional, Dict, Union

ParameterValue = Union[str, int, float, bool, None]

class AgentResponse(BaseModel):
    thought: str
    action: Optional[str] = None
    parameters: Optional[Dict[str, ParameterValue]] = {}
    final: Optional[str] = None