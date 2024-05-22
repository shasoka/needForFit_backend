from src.schemas import MyBaseModel


class DayPhraseRead(MyBaseModel):
    id: int
    phrase: str
    uid: int | None


class DayPhraseCreate(MyBaseModel):
    uid: int
    phrase: str


class DayPhraseUpdate(MyBaseModel):
    phrase: str
