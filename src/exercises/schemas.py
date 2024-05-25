from src.schemas import MyBaseModel, TypesRead


class ExerciseRead(MyBaseModel):
    id: int
    name: str
    description: str
    image: str
    image_url: str
    video_url: str
    exercise_type: TypesRead
