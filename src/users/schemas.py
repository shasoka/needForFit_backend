import datetime

from src.schemas import ORMBase


class UserRead(ORMBase):
    id: int
    username: str
    registered_at: datetime.datetime


class StatsRead(ORMBase):
    id: int
    ttl_weight: int
    ttl_reps: int
    ttl_time: float
    max_weight: int
