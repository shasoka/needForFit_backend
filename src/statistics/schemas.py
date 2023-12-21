from src.schemas import MyBaseModel


class StatsRead(MyBaseModel):
    id: int
    ttl_weight: int
    ttl_reps: int
    ttl_time: float
    max_weight: int


class LocalStatsRead(MyBaseModel):
    id: int
    wid: int
    exercises_count: int
    max_reps: dict
    max_weights: dict
    favorite_exercise: str
    total_weight: int
