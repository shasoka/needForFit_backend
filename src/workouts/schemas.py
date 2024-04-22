import datetime

from src.schemas import MyBaseModel
from src.statistics.schemas import LocalStatsRead
from src.workout_types.schemas import WorkoutTypesRead


class WorkoutBase(MyBaseModel):
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
