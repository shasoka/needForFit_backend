import datetime

from src.schemas import MyBaseModel


class UserRead(MyBaseModel):
    id: int
    username: str
    registered_at: datetime.datetime


class StatsRead(MyBaseModel):
    id: int
    ttl_weight: int
    ttl_reps: int
    ttl_time: float
    max_weight: int
