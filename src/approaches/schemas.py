from schemas import ORMBase


class ApproachRead(ORMBase):
    id: int
    eid: int
    wid: int
    reps: int | None
    weight: int | None
    time: float | None


class ApproachCreate(ORMBase):
    eid: int
    wid: int
    reps: int = None
    weight: int = None
    time: float = None


class ApproachUpdate(ORMBase):
    eid: int = None
    reps: int = None
    weight: int = None
    time: float = None
