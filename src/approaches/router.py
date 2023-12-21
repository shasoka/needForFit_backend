from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.approaches import service
from src.approaches.schemas import ApproachRead, ApproachCreate, ApproachGrouped
from src.database.database import get_async_session


router = APIRouter(prefix="/api/approaches", tags=["Approaches"])


@router.get("/{wid}", response_model=List[ApproachGrouped])
async def get_approaches_by_wid_grouped(wid: int, session: AsyncSession = Depends(get_async_session)):
    return await service.get_approaches_by_wid_grouped_by_eid(session, wid)


@router.post("/", response_model=ApproachRead)
async def create_approach(new_approach: ApproachCreate, session: AsyncSession = Depends(get_async_session)):
    return await service.create_approach(session, new_approach)


@router.post("/update", response_model=ApproachRead)
async def update_approach(approach_data: ApproachRead, session: AsyncSession = Depends(get_async_session)):
    return await service.update_approach(session, approach_data)


@router.delete("/{aid}", response_model=ApproachRead)
async def delete_approach(aid: int, session: AsyncSession = Depends(get_async_session)):
    return await service.delete_approach(session, aid)


@router.delete("/{wid}/{eid}", response_model=List[ApproachRead])
async def delete_exercise_from_workout(wid: int, eid: int, session: AsyncSession = Depends(get_async_session)):
    return await service.delete_exercise_from_workout(session, wid, eid)
