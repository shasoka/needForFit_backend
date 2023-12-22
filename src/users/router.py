from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_async_session
from src.users import service
from src.users.schemas import UserRead, UserWithWorkoutsAndStats

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)


@router.get("/{uid}", response_model=UserRead)
async def get_user(uid: int, session: AsyncSession = Depends(get_async_session)):
    return await service.get_user_by_uid(session, uid)


@router.get("/stats/{uid}", response_model=UserWithWorkoutsAndStats)
async def get_user_with_stats(uid: int, session: AsyncSession = Depends(get_async_session)):
    return await service.get_user_with_stats_and_workouts(session, uid)
