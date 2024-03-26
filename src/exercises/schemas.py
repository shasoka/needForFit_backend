from src.schemas import MyBaseModel, TypesRead


class ExerciseRead(MyBaseModel):
    name: str
    description: str
    image: str | None
    id: int
    exercise_type: TypesRead
