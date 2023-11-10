from src.schemas import ORMBase


class ExerciseCreate(ORMBase):
    name: str
    description: str
    image: str | None


class ExerciseRead(ORMBase):
    id: int
    name: str
    description: str
    image: str | None
