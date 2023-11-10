from src.schemas import ORMBase


class ApproachRead(ORMBase):
    id: int
    eid: int
    wid: int
    reps: int | None
    weight: int | None
    time: float | None
