from fastapi import HTTPException
from sqlalchemy import select, delete, exists, update, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import TYPES_PRESET
from src.database.models import Workout, WorkoutTypes
from src.schemas import TypesCreate
from src.workouts.workout_types.schemas import WorkoutTypesRead


async def get_types_with_ids(session: AsyncSession, uid: int):
    types = await session.execute(select(WorkoutTypes).where(or_(WorkoutTypes.uid == uid, WorkoutTypes.uid == 1)))
    return types.scalars().all()


async def create_type(session: AsyncSession, new_type: TypesCreate):
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
