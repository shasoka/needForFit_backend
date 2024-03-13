from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Exercise, ExerciseTypes


async def get_exercises(session: AsyncSession):
    exercises = await session.execute(select(Exercise).options(selectinload(Exercise.exercise_type)))
    return exercises.scalars().all()


async def get_exercises_filtered_by_tid(tid: int, session: AsyncSession):
    exercises = await session.execute(select(Exercise).where(Exercise.tid == tid).options(selectinload(Exercise.exercise_type)))
    return exercises.scalars().all()


async def get_types_without_ids(session: AsyncSession):
    types = await session.execute(select(ExerciseTypes.name))
    return types.scalars().all()


async def get_types_with_ids(session: AsyncSession):
    types = await session.execute(select(ExerciseTypes))
    return types.scalars().all()
