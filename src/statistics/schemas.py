from src.schemas import MyBaseModel


class LocalStatsRead(MyBaseModel):
    id: int
    wid: int
    exercises_count: int | None
    max_reps: dict | None
    max_weights: dict | None
    favorite_exercise: str | None
    total_weight: int | None


class GlobalStatsRead(MyBaseModel):
    id: int
    uid: int
    ttl_weight: int | None
    ttl_reps: int | None
    max_weight: int | None
    ttl_workouts: int | None
