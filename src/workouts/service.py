from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Workout
from src.workouts.schemas import WorkoutCreate


async def get_workout(session: AsyncSession, id: int):
    workout = await session.execute(select(Workout).filter(Workout.id == id))
    return workout.scalar()


async def get_workouts(session: AsyncSession):
    return await session.execute(select(Workout))


async def create_workout(session: AsyncSession, to_create: WorkoutCreate):
    workout = Workout(uid=to_create.uid)
    session.add(workout)
    await session.commit()
    await session.refresh(workout)
    return workout


async def delete_workout(session: AsyncSession, to_delete: int):
    if workout := await get_workout(session, to_delete):
        stmt = delete(Workout).where(Workout.id == to_delete)
        await session.execute(stmt)
        await session.commit()
        return workout
    else:
        raise HTTPException(status_code=404, detail="Entity with such id not found")
