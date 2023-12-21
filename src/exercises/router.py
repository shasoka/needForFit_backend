from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_async_session
from src.exercises import service
from src.exercises.schemas import ExerciseRead


router = APIRouter(
    prefix="/api/exercises",
    tags=["Exercises"]
)


@router.get("/", response_model=List[ExerciseRead])
async def get_exercises(session: AsyncSession = Depends(get_async_session)):
    exercises = await service.get_exercises(session)
    return exercises.scalars().all()
