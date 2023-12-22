from sqlalchemy.ext.asyncio import AsyncSession

from src.approaches.service import get_approaches_by_wid_grouped_by_eid
from src.database.models import LocalStats
from src.statistics.global_stats_service import GlobalStatsService
from src.workouts import service as workout_service


class LocalStatsService:

    session: AsyncSession = None
    wid: int = None
    cur_workout: list = None

    @classmethod
    async def calculate_stats(cls, session: AsyncSession, wid: int):
        cls.session = session
        cls.wid = wid
        cls.cur_workout = await get_approaches_by_wid_grouped_by_eid(cls.session, cls.wid)

        exercises_count = await cls.get_exercises_count()
        max_wights = await cls.get_max_weights()
        max_reps = await cls.get_max_reps()
        favourite_exercise = await cls.get_favourite_exercise()
        total_weight = await cls.get_total_weight()

        return await cls.save_stats_to_database(exercises_count, max_wights, max_reps, favourite_exercise, total_weight)

    @classmethod
    async def save_stats_to_database(cls, exercises_count: int, max_weights: dict, max_reps: dict,
                                     favourite_exercise: str, total_weight: int):
        local_stats = LocalStats(
            wid=cls.wid,
            exercises_count=exercises_count,
            max_weights=max_weights,
            max_reps=max_reps,
            favorite_exercise=favourite_exercise,
            total_weight=total_weight
        )

        cls.session.add(local_stats)
        await cls.session.commit()
        await cls.session.refresh(local_stats)
        return local_stats

    @classmethod
    async def get_exercises_count(cls):
        return len(cls.cur_workout)

    @classmethod
    async def get_max_weights(cls):
        max_weights_dict = {}

        for exercise_data in cls.cur_workout:
            exercise_name = exercise_data["exercise"].name
            approaches = exercise_data["approaches"]

            max_weight = max(approach["weight"] for approach in approaches)
            max_weights_dict[exercise_name] = max_weight

        return max_weights_dict

    @classmethod
    async def get_max_reps(cls):
        max_reps_dict = {}

        for exercise_data in cls.cur_workout:
            exercise_name = exercise_data["exercise"].name
            approaches = exercise_data["approaches"]

            max_reps = max(approach["reps"] for approach in approaches)
            max_reps_dict[exercise_name] = max_reps

        return max_reps_dict

    @classmethod
    async def get_favourite_exercise(cls):
        max_approaches_count = 0
        favourite_exercise = None

        for exercise_data in cls.cur_workout:
            approaches_count = len(exercise_data["approaches"])

            if approaches_count > max_approaches_count:
                max_approaches_count = approaches_count
                favourite_exercise = exercise_data["exercise"].name

        return favourite_exercise

    @classmethod
    async def get_total_weight(cls):
        total_weight = sum(sum(approach["weight"] for approach in exercise_data["approaches"]) for exercise_data in cls.cur_workout)
        return total_weight
