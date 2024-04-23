from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_async_session
from src.database.models import User
from src.workouts.workout_types import service
from src.workouts.workout_types.schemas import WorkoutTypesRead, WorkoutTypeCreate
from src.auth import service as auth_service


router = APIRouter(
    prefix="/api/workout_types",
    tags=["Workout Types"]
)


@router.get("/{uid}/", response_model=List[WorkoutTypesRead])
async def get_types_with_ids(
        uid: int,
        current_user: User = Depends(auth_service.get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    if current_user.id != uid:
        raise HTTPException(status_code=403, detail="Access forbidden")

    return await service.get_types_with_ids(session, uid)


@router.post("/", response_model=WorkoutTypesRead)
async def create_type(
        new_type: WorkoutTypeCreate,
        current_user: User = Depends(auth_service.get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    if current_user.id != new_type.uid:
        raise HTTPException(status_code=403, detail="Access forbidden")

    return await service.create_type(session, new_type)


@router.put("/{tid}/", response_model=WorkoutTypesRead)
async def update_type(
        tid: int,
        upd_type: WorkoutTypesRead,
        current_user: User = Depends(auth_service.get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    uid = await service.get_uid_by_tid(tid, session)
    if current_user.id != uid:
        raise HTTPException(status_code=403, detail="Access forbidden")

    return await service.update_type(tid, upd_type, session)


@router.delete("/{tid}/", response_model=WorkoutTypesRead)
async def delete_type(
        tid: int,
        current_user: User = Depends(auth_service.get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    uid = await service.get_uid_by_tid(tid, session)
    if current_user.id != uid:
        raise HTTPException(status_code=403, detail="Access forbidden")

    return await service.delete_type(tid, session)
