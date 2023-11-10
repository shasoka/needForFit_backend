import datetime

from src.schemas import ORMBase


class WorkoutRead(ORMBase):
    id: int
    uid: int
    created_at: datetime.datetime
