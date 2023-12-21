from itertools import groupby
from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.approaches import service
from src.database.models import Approach
from src.approaches.schemas import ApproachRead, ApproachCreate, ApproachUpdate, ApproachGrouped
from src.database.database import get_async_session


router = APIRouter(prefix="/api/approaches", tags=["Approaches"])


@router.get("/{wid}", response_model=List[ApproachGrouped])
async def get_approaches_by_wid_grouped(wid: int, session: AsyncSession = Depends(get_async_session)):
    return await service.get_approaches_by_wid_grouped_by_eid(session, wid)


@router.post("/", response_model=ApproachRead)
async def create_approach(new_approach: ApproachCreate, session: AsyncSession = Depends(get_async_session)):
    return await service.create_approach(session, new_approach)


@router.put("/{aid}", response_model=ApproachRead)
async def update_approach(aid: int, approach_data: ApproachRead, session: AsyncSession = Depends(get_async_session)):
    return await service.update_approach(session, aid, approach_data)


@router.delete("/{aid}", response_model=ApproachRead)
async def delete_approach(aid: int, session: AsyncSession = Depends(get_async_session)):
    return await service.delete_approach(session, aid)


@router.delete("/{wid}/{eid}")
async def delete_exercise_in_workout(wid: int, eid: int, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(Approach).where((Approach.eid == eid) & (
            Approach.wid == wid))
    await session.execute(stmt)
    await session.commit()
    return {
        "message": f"All approaches with eid={eid} in workout wid={wid} deleted successfully"}
