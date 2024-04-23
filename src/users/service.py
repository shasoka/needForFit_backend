from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import User, Workout


async def get_user_by_uid(uid: int, session: AsyncSession):
    query = select(User).where(User.id == uid)
    result = await session.execute(query)
    user = result.scalar()
    if user is not None:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


async def get_user_by_username(username: str, session: AsyncSession) -> User:
    query = select(User).where(User.username == username)
    result = await session.execute(query)
    user = result.scalar()
    if user is not None:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


async def get_user_with_stats_and_workouts(session: AsyncSession, uid: int):
    user = await session.execute(select(User).where(User.id == uid).options(selectinload(User.stat)))
    workouts = await session.execute(select(Workout).where(Workout.uid == uid).options(selectinload(Workout.stat), selectinload(Workout.workout_type)))
    return {"user": user.scalar(), "workouts": workouts.scalars().all()}
