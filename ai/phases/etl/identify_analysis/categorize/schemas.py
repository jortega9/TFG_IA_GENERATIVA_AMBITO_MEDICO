from pydantic import BaseModel
from typing import Literal

class CategorizeSchema(BaseModel):
    name: str
    type: Literal["categorical", "numerical", "irrelevant"]
    test: Literal[
        "t_student",
        "mann_whitney",
        "anova",
        "kruskal-wallis",
        "chi-cuadrado",
        "fisher",
        "mcnemar",
    ]
