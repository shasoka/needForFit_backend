from itertools import groupby
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from approaches.models import Approach
from approaches.schemas import ApproachRead
from database.database import get_async_session


router = APIRouter(
    prefix="/api/approaches",
    tags=["Approaches"]
)


@router.get("/", response_model=List[ApproachRead])
async def get_approaches(session: AsyncSession = Depends(get_async_session)):
    query = select(Approach)
    result = await session.execute(query)
    approaches = [{"id": approach.id,
                   "wid": approach.wid,
                   "eid": approach.eid,
                   "reps": approach.reps,
                   "weight": approach.weight,
                   "time": approach.time} for approach in result.scalars().all()]
    return approaches


@router.get("/{wid}", response_model=List[ApproachRead])
async def get_approaches_by_wid(wid: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Approach).where(Approach.wid == wid)
    result = await session.execute(query)
    approaches = [{"id": approach.id, "wid": approach.wid, "eid": approach.eid,
                   "reps": approach.reps, "weight": approach.weight,
                   "time": approach.time} for approach in result.scalars().all()]
    return approaches
