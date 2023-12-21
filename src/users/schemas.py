import datetime

from src.schemas import MyBaseModel


class UserRead(MyBaseModel):
    id: int
    username: str
    registered_at: datetime.datetime




