from itertools import groupby
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from approaches.models import Approach
from approaches.schemas import ApproachRead, ApproachCreate, ApproachUpdate
from database.database import get_async_session

router = APIRouter(prefix="/api/approaches", tags=["Approaches"])


@router.get("/", response_model=List[ApproachRead])
async def get_approaches(session: AsyncSession = Depends(get_async_session)):
    query = select(Approach).order_by(Approach.id)  # добавил order потому что после put запись дропается вниз
    result = await session.execute(query)
    approaches = [{"id": approach.id, "wid": approach.wid, "eid": approach.eid,
                   "reps": approach.reps, "weight": approach.weight,
                   "time": approach.time} for approach in
                  result.scalars().all()]
    return approaches


@router.get("/{wid}")
async def get_approaches_by_wid(wid: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Approach).where(Approach.wid == wid)
    result = await session.execute(query)
    approaches = result.scalars().all()

    grouped_approaches = {}
    for key, group in groupby(approaches, key=lambda x: x.eid):
        grouped_approaches[key] = [
            {"id": approach.id, "wid": approach.wid, "eid": approach.eid,
             "reps": approach.reps, "weight": approach.weight,
             "time": approach.time} for approach in group]

    return grouped_approaches


@router.post("/", response_model=ApproachRead)
async def create_approach(new_approach: ApproachCreate,
                          session: AsyncSession = Depends(get_async_session)):
    # Создание объекта Approach с переданными значениями
    approach_data = new_approach.model_dump()
    approach = Approach(**approach_data)

    # Добавление и фиксация в базе данных
    session.add(approach)
    await session.commit()
    await session.refresh(approach)

    return approach


@router.put("/{aid}")
async def update_approach(aid: int, approach_data: ApproachUpdate,
                          session: AsyncSession = Depends(get_async_session)):
    # Проверка, существует ли подход с указанным ID
    existing_approach = await session.get(Approach, aid)

    # Обновление данных подхода
    for key, value in approach_data.dict(exclude_unset=True).items():
        setattr(existing_approach, key, value)

    # Выполнение транзакции для сохранения изменений
    try:
        await session.commit()
        await session.refresh(existing_approach)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating approach: {str(e)}")

    return {"message": "Approach updated successfully"}


@router.delete("/{aid}")
async def delete_approach(aid: int, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(Approach).where(Approach.id == aid)
    await session.execute(stmt)
    await session.commit()
    return {"message": "Approach deleted successfully"}


@router.delete("/{wid}/{eid}")
async def delete_exercise_in_workout(wid: int, eid: int, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(Approach).where((Approach.eid == eid) & (
            Approach.wid == wid))
    await session.execute(stmt)
    await session.commit()
    return {
        "message": f"All approaches with eid={eid} in workout wid={wid} deleted successfully"}


@router.post("/huge_seed")
async def huge_seed_approaches(session: AsyncSession = Depends(get_async_session)):
    to_seed = []
    for i in range(500000):
        to_seed.append({"eid": 345960 + i, "wid": 11 + i, "reps": i, "weight": i, "time": i})

    stmt = insert(Approach)
    await session.execute(stmt, to_seed)

    await session.commit()
    return {"message": "Successfully seeded"}
