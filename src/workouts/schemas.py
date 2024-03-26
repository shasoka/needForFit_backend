import datetime

from src.schemas import MyBaseModel, TypesRead
from src.statistics.schemas import LocalStatsRead


class WorkoutBase(MyBaseModel):
    uid: int


class WorkoutRead(WorkoutBase):
    id: int
    name: str
    workout_type: TypesRead
    created_at: datetime.datetime


class WorkoutCreate(WorkoutBase):
    pass


class WorkoutWithStatsRead(WorkoutRead):
    stat: LocalStatsRead | None
