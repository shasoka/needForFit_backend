from src.schemas import MyBaseModel


class LocalStatsRead(MyBaseModel):
    id: int
    wid: int
    exercises_count: int | None
    max_reps: dict | None
    max_weights: dict | None
    favorite_exercise: str | None
    total_weight: int | None
