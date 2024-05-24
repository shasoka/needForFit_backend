from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_async_session
from src.database.models import User
from src.auth.service import current_user_getter_moderate, current_user_getter_strict
from src.users.phrases import service
from src.users.phrases.schemas import DayPhraseRead, DayPhraseCreate, DayPhraseUpdate


router = APIRouter(
    prefix="/api/phrases",
    tags=["Phrases"]
)


@router.get("/", response_model=DayPhraseRead)
async def get_day_phrase(
        uid: Optional[int],
        current_user: Optional[User] = Depends(current_user_getter_moderate),
        session: AsyncSession = Depends(get_async_session)
):
    if current_user:
        if current_user.id != uid:
            raise HTTPException(status_code=403, detail="Access forbidden")
        return await service.get_day_phrase(session, uid=uid)
    else:
        return await service.get_day_phrase(session)


@router.post("/", response_model=DayPhraseRead)
async def create_day_phrase(
        new_phrase: DayPhraseCreate,
        current_user: User = Depends(current_user_getter_strict),
        session: AsyncSession = Depends(get_async_session)
):
    if current_user.id != new_phrase.uid:
        raise HTTPException(status_code=403, detail="Access forbidden")

    return await service.create_phrase(session, new_phrase)


@router.put("/{uid}", response_model=DayPhraseRead)
async def update_day_phrase(
        uid: int,
        upd_phrase: DayPhraseUpdate,
        current_user: User = Depends(current_user_getter_strict),
        session: AsyncSession = Depends(get_async_session)
):
    if current_user.id != uid:
        raise HTTPException(status_code=403, detail="Access forbidden")

    return await service.update_phrase(session, uid, upd_phrase)


@router.delete("/{uid}", response_model=DayPhraseRead)
async def delete_day_phrase(
        uid: int,
        current_user: User = Depends(current_user_getter_strict),
        session: AsyncSession = Depends(get_async_session)
):
    if current_user.id != uid:
        raise HTTPException(status_code=403, detail="Access forbidden")

    return await service.delete_phrase(session, uid)
