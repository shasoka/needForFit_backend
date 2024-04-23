from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Workout, LocalStats, Approach
from src.workouts.workout_types.schemas import WorkoutTypesRead
from src.workouts.schemas import WorkoutCreate, WorkoutRead


async def get_uid_by_wid(wid: int, session: AsyncSession):
    stmt = select(Workout.uid).where(Workout.id == wid)
    result = await session.execute(stmt)
    uid = result.scalar()
    return uid


async def get_workout(session: AsyncSession, id: int):
    workout = await session.execute(select(Workout).filter(Workout.id == id).options(selectinload(Workout.workout_type)))
    return workout.scalar()


async def get_workouts(session: AsyncSession, uid: int):
    result = await session.execute(select(Workout).where(Workout.uid == uid).options(selectinload(Workout.workout_type)))
    return result.scalars().all()


async def get_workouts_with_stats(session: AsyncSession, uid: int):
    query = select(Workout).options(selectinload(Workout.stat), selectinload(Workout.workout_type)).where(Workout.uid == uid)
    result = await session.execute(query)
    return result.scalars().all()


async def create_workout(session: AsyncSession, to_create: WorkoutCreate):
    workout = Workout(uid=to_create.uid, tid=3)
    session.add(workout)
    await session.commit()
    await session.refresh(workout, attribute_names=["workout_type"])  # После обновления записи в бд подгружаем связанные поля
    return workout


async def delete_workout(session: AsyncSession, to_delete: int):
    if workout := await get_workout(session, to_delete):
        stmt_local_stats = delete(LocalStats).where(LocalStats.wid == to_delete)
        await session.execute(stmt_local_stats)

        stmt_approaches = delete(Approach).where(Approach.wid == to_delete)
        await session.execute(stmt_approaches)

        stmt_workout = delete(Workout).where(Workout.id == to_delete)
        await session.execute(stmt_workout)

        workout_copy = WorkoutRead(
            uid=workout.uid,
            id=workout.id,
            name=workout.name,
            workout_type=WorkoutTypesRead(id=workout.workout_type.id, name=workout.workout_type.name, uid=workout.workout_type.uid),
            created_at=workout.created_at
        )
        await session.commit()
        return workout_copy
    else:
        raise HTTPException(status_code=404, detail="Entity with such id not found")


async def update_workout(to_update: int, upd_workout: WorkoutRead, session: AsyncSession):
    if workout := await get_workout(session, to_update):
        for key, value in upd_workout.dict().items():
            if key != "workout_type" and hasattr(workout, key):
                setattr(workout, key, value)
            elif key == "workout_type":
                # Обновляем tid на основе идентификатора типа тренировки из запроса
                setattr(workout, "tid", value["id"])
        await session.commit()
        await session.refresh(workout, attribute_names=["workout_type"])
        return workout
    else:
        raise HTTPException(status_code=404, detail="Entity with such id not found")
