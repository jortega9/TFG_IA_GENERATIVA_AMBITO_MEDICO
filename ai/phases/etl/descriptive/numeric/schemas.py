from typing import List

from pydantic import BaseModel

class IdentifySchema(BaseModel):
    
    list: List[str]
    
class ConclusionSchema(BaseModel):
    
    conclusion: str
    