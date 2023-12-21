from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.approaches.schemas import ApproachCreate, ApproachRead
from src.database.models import Approach


async def get_approaches_by_wid_grouped_by_eid(session: AsyncSession, wid: int):
    query = select(Approach).where(Approach.wid == wid).options(selectinload(Approach.exercise))
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


async def update_approach(session: AsyncSession, aid: int, approach_data: ApproachRead):
    # Проверка, существует ли подход с указанным ID
    existing_approach = await session.get(Approach, aid)

    if existing_approach is None:
        raise HTTPException(status_code=404, detail="Approach not found")

    # Обновление данных подхода
    for key, value in approach_data.model_dump().items():
        setattr(existing_approach, key, value)

    try:
        await session.commit()
        await session.refresh(existing_approach)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating approach: {str(e)}")

    return existing_approach


async def delete_approach(session: AsyncSession, aid: int):
    # existing_approach = await session.execute(select(Approach).where((Approach.eid == eid) & (Approach.wid == wid)))
    existing_approach = await session.get(Approach, aid)

    if existing_approach is None:
        raise HTTPException(status_code=404, detail="Approach not found")

    stmt = delete(Approach).where(Approach.id == aid)
    await session.execute(stmt)
    await session.commit()
    return existing_approach
