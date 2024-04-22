from src.schemas import TypesRead, TypesCreate


class WorkoutTypesRead(TypesRead):
    uid: int


class WorkoutTypeCreate(TypesCreate):
    uid: int
