from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_async_session
from workouts.models import Workout
from workouts.schemas import WorkoutRead


router = APIRouter(
    prefix="/api/workouts",
    tags=["Workouts"]
)


@router.get("/", response_model=List[WorkoutRead])
async def get_workouts(session: AsyncSession = Depends(get_async_session)):
    query = select(Workout)
    result = await session.execute(query)
    workouts = [{"id": workout.id,
                 "uid": workout.uid,
                 "created_at": workout.created_at} for workout in result.scalars().all()]
    return workouts
