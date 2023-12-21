from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_async_session
from src.statistics.local_stats_service import LocalStatsService
from src.statistics.schemas import LocalStatsRead
from src.workouts import service
from src.workouts.schemas import WorkoutRead, WorkoutCreate, WorkoutWithStatsRead

router = APIRouter(
    prefix="/api/workouts",
    tags=["Workouts"]
)


@router.get("/", response_model=List[WorkoutRead])
async def get_workouts(session: AsyncSession = Depends(get_async_session)):
    return await service.get_workouts(session)


@router.get("/w_stats", response_model=WorkoutWithStatsRead)
async def get_workouts_with_stats(session: AsyncSession = Depends(get_async_session)):
    return await service.get_workouts_with_stats(session)


@router.post("/{wid}", response_model=LocalStatsRead)
async def save_workout(wid: int, session: AsyncSession = Depends(get_async_session)):
    return await LocalStatsService.calculate_stats(session, wid)


@router.post("/", response_model=WorkoutRead)
async def create_workout(new_workout: WorkoutCreate, session: AsyncSession = Depends(get_async_session)):
    return await service.create_workout(session, new_workout)


@router.delete("/{id}", response_model=WorkoutRead)
async def delete_workout(id: int, session: AsyncSession = Depends(get_async_session)):
    return await service.delete_workout(session, id)
