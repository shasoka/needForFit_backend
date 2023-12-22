from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import User, Workout


async def get_user_by_uid(session: AsyncSession, uid: int):
    query = select(User).where(User.id == uid)
    result = await session.execute(query)
    user = result.scalar()
    return user.exclude("password")


async def get_user_with_stats_and_workouts(session: AsyncSession, uid: int):
    user = await session.execute(select(User).where(User.id == uid).options(selectinload(User.stat)))
    workouts = await session.execute(select(Workout).where(Workout.uid == uid).options(selectinload(Workout.stat)))
    return {"user": user.scalar().exclude("password"), "workouts": workouts.scalars().all()}
