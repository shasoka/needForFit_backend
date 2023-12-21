import datetime

from src.schemas import MyBaseModel


class WorkoutBase(MyBaseModel):
    uid: int


class WorkoutRead(WorkoutBase):
    id: int
    created_at: datetime.datetime


class WorkoutCreate(WorkoutBase):
    pass


class WorkoutWithStatsRead(WorkoutRead):
    stat: dict | None
