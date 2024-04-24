from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.approaches.schemas import ApproachCreate, ApproachRead
from src.database.models import Approach, Exercise, Workout


async def get_uid_by_aid(aid: int, session: AsyncSession) -> int:
    stmt = select(Approach.wid).where(Approach.id == aid)
    result = await session.execute(stmt)
    wid = result.scalar()

    if not wid:
        raise HTTPException(status_code=404, detail="Approach not found")

    # Найти uid (идентификатор пользователя) по wid (идентификатор тренировки)
    stmt = select(Workout.uid).where(Workout.id == wid)
    result = await session.execute(stmt)
    uid = result.scalar()

    if not uid:
        raise HTTPException(status_code=404, detail="User not found")

    return uid


async def get_approaches_by_wid_grouped_by_eid(session: AsyncSession, wid: int):
    query = select(Approach).where(Approach.wid == wid).options(
        selectinload(Approach.exercise)
        .selectinload(Exercise.exercise_type)
    )
    result = await session.execute(query)
    approaches = result.scalars().all()

    grouped_approaches = {}

    for approach in approaches:
        exercise = approach.exercise
        if (id := exercise.id) not in grouped_approaches:
            grouped_approaches[id] = {"exercise": exercise, "approaches": []}

        grouped_approaches[id]["approaches"].append(approach.exclude("exercise"))

    return list(grouped_approaches.values())


async def create_approach(session: AsyncSession, new_approach: ApproachCreate):
    # Создание объекта Approach с переданными значениями
    approach_data = new_approach.model_dump()
    approach = Approach(**approach_data)

    # Добавление и фиксация в базе данных
    session.add(approach)
    await session.commit()
    await session.refresh(approach)

    return approach


async def update_approach(aid: int, upd_approach: ApproachRead, session: AsyncSession):
    if approach := await session.get(Approach, aid):
        approach.eid = upd_approach.eid
        approach.wid = upd_approach.wid
        approach.reps = upd_approach.reps
        approach.weight = upd_approach.weight
        approach.time = upd_approach.time
        await session.commit()
        await session.refresh(approach)
        return approach
    else:
        raise HTTPException(status_code=404, detail="Entity with such id not found")


async def delete_approach(session: AsyncSession, aid: int):
    existing_approach = await session.get(Approach, aid)

    if existing_approach is None:
        raise HTTPException(status_code=404, detail="Approach not found")

    stmt = delete(Approach).where(Approach.id == aid)
    await session.execute(stmt)
    await session.commit()
    return existing_approach


async def delete_exercise_from_workout(session: AsyncSession, wid: int, eid: int):
    existing_approaches = await session.execute(select(Approach).where((Approach.eid == eid) & (Approach.wid == wid)))

    if existing_approaches is None:
        raise HTTPException(status_code=404, detail="Approaches not found")

    stmt = delete(Approach).where((Approach.eid == eid) & (Approach.wid == wid))
    await session.execute(stmt)
    await session.commit()

    deleted_approaches = existing_approaches.scalars().all()

    eid = deleted_approaches[0].eid
    exercise = await session.execute(select(Exercise).options(selectinload(Exercise.exercise_type)).where(Exercise.id == eid))

    grouped_exercise = {"exercise": exercise.scalars().first(), "approaches": deleted_approaches}

    return grouped_exercise
