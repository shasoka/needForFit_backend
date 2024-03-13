from src.schemas import MyBaseModel


class TypesRead(MyBaseModel):
    id: int
    name: str


class ExerciseRead(MyBaseModel):
    name: str
    description: str
    image: str | None
    id: int
    exercise_type: TypesRead
