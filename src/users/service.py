from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from src.approaches.models import Approach
from src.users.models import GlobalStats, User
from src.workouts.models import Workout


class StatsService:

    @classmethod
    async def get_stats_by_uid(cls, uid: int, session: AsyncSession):
        query = select(GlobalStats).where(GlobalStats.uid == uid)
        result = await session.execute(query)
        stats = result.scalars().first()
        return stats

    @classmethod
    async def get_user_by_uid(cls, uid: int, session: AsyncSession):
        query = select(User).where(User.id == uid)
        result = await session.execute(query)
        user = result.scalars().first()
        return user

    @classmethod
    async def update_global_stats(cls, session: AsyncSession, uid: int):

        global_stats = await cls.get_stats_by_uid(uid, session)

        global_stats.ttl_weight = await cls.calculate_weight_sum_for_user(uid, session)
        global_stats.ttl_reps = await cls.calculate_reps_sum_for_user(uid, session)
        global_stats.ttl_time = await cls.calculate_time_sum_for_user(uid, session)
        global_stats.max_weight = await cls.calculate_weight_max_for_user(uid, session)

        session.add(global_stats)
        await session.commit()

    @staticmethod
    async def calculate_weight_sum_for_user(uid: int, session: AsyncSession):
        stmt = (select(func.sum(Approach.weight)).join(Workout, Approach.wid == Workout.id).where(Workout.uid == uid))
        result = await session.execute(stmt)
        weight_sum = result.scalar()
        return weight_sum if weight_sum is not None else 0

    @staticmethod
    async def calculate_weight_max_for_user(uid: int, session: AsyncSession):
        stmt = (select(func.max(Approach.weight)).join(Workout, Approach.wid == Workout.id).where(Workout.uid == uid))
        result = await session.execute(stmt)
        weight_sum = result.scalar()
        return weight_sum if weight_sum is not None else 0

    @staticmethod
    async def calculate_reps_sum_for_user(uid: int, session: AsyncSession):
        stmt = (select(func.sum(Approach.reps)).join(Workout, Approach.wid == Workout.id).where(Workout.uid == uid))
        result = await session.execute(stmt)
        reps_sum = result.scalar()
        return reps_sum if reps_sum is not None else 0

    @staticmethod
    async def calculate_time_sum_for_user(uid: int, session: AsyncSession):
        stmt = (select(func.sum(Approach.time)).join(Workout, Approach.wid == Workout.id).where(Workout.uid == uid))
        result = await session.execute(stmt)
        time_sum = result.scalar()
        return time_sum if time_sum is not None else 0
