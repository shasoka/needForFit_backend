import datetime

from schemas import ORMBase


class WorkoutRead(ORMBase):
    id: int
    uid: int
    created_at: datetime.datetime


class WorkoutCreate(ORMBase):
    uid: int
