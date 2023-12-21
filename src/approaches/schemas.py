from typing import List

from src.exercises.schemas import ExerciseRead
from src.schemas import MyBaseModel


class ApproachRead(MyBaseModel):
    id: int
    eid: int
    wid: int
    reps: int | None
    weight: int | None
    time: float | None


class ApproachCreate(MyBaseModel):
    eid: int
    wid: int
    reps: int = None
    weight: int = None
    time: float = None


class ApproachGrouped(MyBaseModel):
    exercise: ExerciseRead
    approaches: List[ApproachRead]
