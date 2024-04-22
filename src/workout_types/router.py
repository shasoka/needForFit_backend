from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_async_session
from src.workout_types import service
from src.workout_types.schemas import WorkoutTypesRead, WorkoutTypeCreate

router = APIRouter(
    prefix="/api/workout_types",
    tags=["Workout Types"]
)


@router.get("/{uid}/", response_model=List[WorkoutTypesRead])
async def get_types_with_ids(uid: int, session: AsyncSession = Depends(get_async_session)):
    return await service.get_types_with_ids(session, uid)


@router.post("/", response_model=WorkoutTypesRead)
async def create_type(new_type: WorkoutTypeCreate, session: AsyncSession = Depends(get_async_session)):
    return await service.create_type(session, new_type)


@router.put("/{tid}/", response_model=WorkoutTypesRead)
async def update_type(tid: int, upd_type: WorkoutTypesRead, session: AsyncSession = Depends(get_async_session)):
    return await service.update_type(tid, upd_type, session)


@router.delete("/{tid}/", response_model=WorkoutTypesRead)
async def delete_type(tid: int, session: AsyncSession = Depends(get_async_session)):
    return await service.delete_type(tid, session)
