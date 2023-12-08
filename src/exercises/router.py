from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_async_session
from src.exercises.models import Exercise
from src.exercises.schemas import ExerciseRead, ExerciseCreate

import time


router = APIRouter(
    prefix="/api/exercises",
    tags=["Exercises"]
)


@router.get("/", response_model=List[ExerciseRead])
async def get_exercises(session: AsyncSession = Depends(get_async_session)):
    query = select(Exercise)
    result = await session.execute(query)
    tmp = result.scalars().first()
    exercises = [{"id": exercise.id,
                  "name": exercise.name,
                  "description": exercise.description,
                  "image": exercise.image} for exercise in result.scalars().all()]
    return exercises


@router.post("/seed")
async def seed_exercises(session: AsyncSession = Depends(get_async_session)):
    to_seed = []
    for i in range(100):
        to_seed.append({"name": f"Упражнение {i}",
                        "description": f"Описание {i}",
                        "image": f"image{i}.jpg"})

    for value in to_seed:
        stmt = insert(Exercise).values(**value)
        await session.execute(stmt)

    await session.commit()
    return {"message": "Successfully seeded"}


@router.post("/huge_seed")
async def huge_seed_exercises(session: AsyncSession = Depends(get_async_session)):
    to_seed = []
    for i in range(500000):
        to_seed.append({"name": f"Упражнение {i}",
                        "description": f"Описание {i}",
                        "image": f"image{i}.jpg"})

    stmt = insert(Exercise)
    await session.execute(stmt, to_seed)

    await session.commit()
    return {"message": "Successfully seeded"}
