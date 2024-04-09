from fastapi import HTTPException
from sqlalchemy import select, delete, exists, update, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Workout, LocalStats, Approach, WorkoutTypes
from src.schemas import TypesRead, TypeCreate
from src.workouts.schemas import WorkoutCreate, WorkoutRead, WorkoutTypesRead

from src.config import TYPES_PRESET


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


# ---------------- # ---------------- # ---------------- # ---------------- # ---------------- #


async def get_types_with_ids(session: AsyncSession, uid: int):
    types = await session.execute(select(WorkoutTypes).where(or_(WorkoutTypes.uid == uid, WorkoutTypes.uid == 1)))
    return types.scalars().all()


async def create_type(session: AsyncSession, new_type: TypeCreate):
    to_add = WorkoutTypes(name=new_type.name, uid=new_type.uid)
    session.add(to_add)
    await session.commit()
    await session.refresh(to_add)
    return to_add


async def update_type(tid: int, upd_type: WorkoutTypesRead, session: AsyncSession):
    if workout_type := await session.get(WorkoutTypes, tid):
        if workout_type.id > TYPES_PRESET:
            workout_type.name = upd_type.name
            workout_type.uid = upd_type.uid
            await session.commit()
            await session.refresh(workout_type)
            return workout_type
        else:
            raise HTTPException(status_code=403, detail="Access denied. You can't edit pre-installed workout types.")
    else:
        raise HTTPException(status_code=404, detail="Entity with such id not found")


async def delete_type(tid: int, session: AsyncSession):
    if tid <= TYPES_PRESET:
        raise HTTPException(status_code=403, detail="Access denied. You can't edit pre-installed workout types.")

    workout_type = await session.get(WorkoutTypes, tid)
    if workout_type is None:
        raise HTTPException(status_code=404, detail="Entity with such id not found")
    to_return = WorkoutTypesRead(id=workout_type.id, name=workout_type.name, uid=workout_type.uid)

    # Проверяем, что тип тренировки не используется в таблице workouts
    used_in_workouts = await session.execute(select(exists().where(Workout.tid == tid)))
    if used_in_workouts.scalar():
        # Заменяем все вхождения типа тренировки на 3
        await session.execute(update(Workout).where(Workout.tid == tid).values(tid=3))
        await session.commit()

    try:
        # Удаляем тип тренировки
        await session.execute(delete(WorkoutTypes).where(WorkoutTypes.id == tid))
        await session.commit()
        return to_return
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Type is still used in some workouts, deletion failed")
