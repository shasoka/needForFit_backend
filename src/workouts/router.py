from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_async_session
from src.workouts import service
from src.workouts.schemas import WorkoutRead, WorkoutCreate


router = APIRouter(
    prefix="/api/workouts",
    tags=["Workouts"]
)


@router.get("/", response_model=List[WorkoutRead])
async def get_workouts(session: AsyncSession = Depends(get_async_session)):
    workouts = await service.get_workouts(session)
    return workouts.scalars().all()


@router.post("/", response_model=WorkoutRead)
async def create_workout(new_workout: WorkoutCreate, session: AsyncSession = Depends(get_async_session)):
    workout = await service.create_workout(session, new_workout)
    return workout


@router.delete("/{id}", response_model=WorkoutRead)
async def delete_workout(id: int, session: AsyncSession = Depends(get_async_session)):
    workout = await service.delete_workout(session, id)
    return workout
