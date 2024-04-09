import datetime

from src.schemas import MyBaseModel, TypesRead, TypeCreate
from src.statistics.schemas import LocalStatsRead


class WorkoutBase(MyBaseModel):
    uid: int


class WorkoutTypesRead(TypesRead):
    uid: int


class WorkoutRead(WorkoutBase):
    id: int
    name: str
    workout_type: WorkoutTypesRead
    created_at: datetime.datetime


class WorkoutCreate(WorkoutBase):
    pass


class WorkoutWithStatsRead(WorkoutRead):
    stat: LocalStatsRead | None


class WorkoutTypeCreate(TypeCreate):
    uid: int
