from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Workout, LocalStats, Approach
from src.workouts.schemas import WorkoutCreate


async def get_workout(session: AsyncSession, id: int):
    workout = await session.execute(select(Workout).filter(Workout.id == id))
    return workout.scalar()


async def get_workouts(session: AsyncSession):
    result = await session.execute(select(Workout))
    return result.scalars().all()


async def get_workouts_with_stats(session: AsyncSession):
    query = select(Workout).options(selectinload(Workout.stat))
    result = await session.execute(query)
    return result.scalars().all()


async def create_workout(session: AsyncSession, to_create: WorkoutCreate):
    workout = Workout(uid=to_create.uid)
    session.add(workout)
    await session.commit()
    await session.refresh(workout)
    return workout


async def delete_workout(session: AsyncSession, to_delete: int):
    if workout := await get_workout(session, to_delete):
        stmt_local_stats = delete(LocalStats).where(LocalStats.wid == to_delete)
        await session.execute(stmt_local_stats)

        stmt_approaches = delete(Approach).where(Approach.wid == to_delete)
        await session.execute(stmt_approaches)

        stmt_workout = delete(Workout).where(Workout.id == to_delete)
        await session.execute(stmt_workout)

        await session.commit()
        return workout
    else:
        raise HTTPException(status_code=404, detail="Entity with such id not found")
