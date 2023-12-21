from typing import List

from src.database.models import Approach
from src.schemas import MyBaseModel


class ExerciseBase(MyBaseModel):
    name: str
    description: str
    image: str | None


class ExerciseRead(ExerciseBase):
    id: int
