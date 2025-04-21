"""Responses format for the categorical comparative analysis."""

from pydantic import BaseModel
from typing import List

class GroupValue(BaseModel):
    key: str
    label: str

class GroupVariableSchema(BaseModel):
	"""Schema for the identify group response format."""
	explanation: str
	group_variable: str
	description: str
	values: List[GroupValue]
	valid_keys: List[str]
	excluded_keys: List[str]