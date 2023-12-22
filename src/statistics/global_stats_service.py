from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Approach, Workout, GlobalStats
from src.workouts import service as workout_service


class GlobalStatsService:

    session: AsyncSession = None
    uid: int = None

    @classmethod
    async def calculate_stats(cls, session: AsyncSession, uid: int):
        cls.session = session
        cls.uid = uid

        ttl_weight = await cls.get_ttl_weight()
        ttl_reps = await cls.get_ttl_reps()
        max_weight = await cls.get_max_weight()
        ttl_workouts = await cls.get_ttl_workouts()

        await cls.save_stats_to_database(ttl_weight, ttl_reps, max_weight, ttl_workouts)

    @classmethod
    async def save_stats_to_database(cls, ttl_weight: int, ttl_reps: int, max_weight: int, ttl_workouts: int):
        # Проверяем, существует ли запись с таким uid
        existing_stats = await cls.session.execute(select(GlobalStats).where(GlobalStats.uid == cls.uid))
        existing_stats = existing_stats.scalar()

        if existing_stats:
            # Если запись существует, обновляем ее
            existing_stats.ttl_weight = ttl_weight
            existing_stats.ttl_reps = ttl_reps
            existing_stats.max_weight = max_weight
            existing_stats.ttl_workouts = ttl_workouts
        else:
            # Если записи нет, добавляем новую
            new_stats = GlobalStats(
                uid=cls.uid,
                ttl_weight=ttl_weight,
                ttl_reps=ttl_reps,
                max_weight=max_weight,
                ttl_workouts=ttl_workouts
            )
            cls.session.add(new_stats)

        await cls.session.commit()

    @classmethod
    async def get_ttl_weight(cls):
        stmt = select(func.sum(Approach.weight)).join(Workout, Approach.wid == Workout.id).where(Workout.uid == cls.uid)
        result = await cls.session.execute(stmt)
        weight_sum = result.scalar()
        return weight_sum if weight_sum is not None else 0

    @classmethod
    async def get_ttl_reps(cls):
        stmt = select(func.sum(Approach.reps)).join(Workout, Approach.wid == Workout.id).where(Workout.uid == cls.uid)
        result = await cls.session.execute(stmt)
        reps_sum = result.scalar()
        return reps_sum if reps_sum is not None else 0

    @classmethod
    async def get_max_weight(cls):
        stmt = select(func.max(Approach.weight)).join(Workout, Approach.wid == Workout.id).where(Workout.uid == cls.uid)
        result = await cls.session.execute(stmt)
        weight_sum = result.scalar()
        return weight_sum if weight_sum is not None else 0

    @classmethod
    async def get_ttl_workouts(cls):
        return len(await workout_service.get_workouts(cls.session, cls.uid))
