from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload, subqueryload

from src.database.models import User, Workout
from src.users import service

from src.database.database import get_async_session
from src.users.schemas import UserRead


router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)


@router.get("/{uid}", response_model=UserRead)
async def get_user(uid: int, session: AsyncSession = Depends(get_async_session)):
    return await service.get_user_by_uid(session, uid)


@router.get("/stats/{uid}")
async def get_user_with_stats(uid: int, session: AsyncSession = Depends(get_async_session)):
    user = await session.execute(select(User).where(User.id == uid).options(subqueryload(User.stat)))
    workouts = await session.execute(select(Workout).where(Workout.uid == uid).options(subqueryload(Workout.stat)))
    return {"user": user.scalars().all(), "workouts": workouts.scalars().all()}
    # TODO написать схему респонса
    # TODO перенести этот метод в сервис
