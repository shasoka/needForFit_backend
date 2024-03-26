from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_async_session
from src.exercises import service
from src.exercises.schemas import ExerciseRead, TypesRead


router = APIRouter(
    prefix="/api/exercises",
    tags=["Exercises"]
)


@router.get("/", response_model=List[ExerciseRead])
async def get_exercises(session: AsyncSession = Depends(get_async_session)):
    return await service.get_exercises(session)


@router.get("/types_without_ids", response_model=List[str])
async def get_types_without_ids(session: AsyncSession = Depends(get_async_session)):
    return await service.get_types_without_ids(session)


@router.get("/types_with_ids", response_model=List[TypesRead])
async def get_types_with_ids(session: AsyncSession = Depends(get_async_session)):
    return await service.get_types_with_ids(session)


@router.get("/{tid}/", response_model=List[ExerciseRead])
async def get_exercises_filtered_by_tid(tid: int, session: AsyncSession = Depends(get_async_session)):
    return await service.get_exercises_filtered_by_tid(tid, session)
