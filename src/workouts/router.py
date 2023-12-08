from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_async_session
from workouts.models import Workout
from workouts.schemas import WorkoutRead, WorkoutCreate

router = APIRouter(prefix="/api/workouts", tags=["Workouts"])


@router.get("/", response_model=List[WorkoutRead])
async def get_workouts(session: AsyncSession = Depends(get_async_session)):
    query = select(Workout)
    result = await session.execute(query)
    workouts = [{"id": workout.id, "uid": workout.uid,
                 "created_at": workout.created_at} for workout in
                result.scalars().all()]
    return workouts


@router.post("/", response_model=WorkoutRead)
async def create_workout(new_workout: WorkoutCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Пробую доки. Тут оказывается MD
    \nСЕМА СЮДА ТОЛЬКО **2** ПЕРЕДАВАЙ ПО БРАТСКИ СПС ПОТОМУ ЧТО У НАС ТОЛЬКО ОДИН ЮЗЕР
    """

    # тут должен быть try except на случай если uid'а нет в таблице users
    workout = Workout(uid=new_workout.uid)
    session.add(workout)
    await session.commit()
    await session.refresh(workout)
    return workout


@router.post("/huge_seed")
async def huge_seed_workouts(session: AsyncSession = Depends(get_async_session)):
    to_seed = []
    for i in range(500000):
        to_seed.append({"uid": 2})

    stmt = insert(Workout)
    await session.execute(stmt, to_seed)

    await session.commit()
    return {"message": "Successfully seeded"}
