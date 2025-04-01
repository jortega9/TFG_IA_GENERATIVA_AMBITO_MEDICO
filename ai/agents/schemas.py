from pydantic import BaseModel, ValidationError
from typing import Optional, Dict, Union

ParameterValue = Union[str, int, float, bool, None]

class AgentResponse(BaseModel):
    thought: str
    action: Optional[str] 
    parameters: Optional[Dict[str, object]] 
    final: Optional[str] 