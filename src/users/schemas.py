import datetime
from typing import List

from src.schemas import MyBaseModel
from src.statistics.schemas import GlobalStatsRead
from src.workouts.schemas import WorkoutWithStatsRead


class UserRead(MyBaseModel):
    id: int
    username: str
    registered_at: datetime.datetime


class UserLogin(MyBaseModel):
    username: str
    password: str


class UserWithStats(UserRead):
    stat: GlobalStatsRead


class UserWithWorkoutsAndStats(MyBaseModel):
    user: UserWithStats
    workouts: List[WorkoutWithStatsRead]
