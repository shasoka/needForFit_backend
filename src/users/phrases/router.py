from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_async_session
from src.database.models import User
from src.auth import service as auth_service
from src.users.phrases import service
from src.users.phrases.schemas import DayPhraseRead, DayPhraseCreate, DayPhraseUpdate


router = APIRouter(
    prefix="/api/phrases",
    tags=["Phrases"]
)


@router.get("/{uid}", response_model=DayPhraseRead)
async def get_day_phrase(
        uid: int,
        current_user: User = Depends(auth_service.get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    if current_user.id != uid:
        raise HTTPException(status_code=403, detail="Access forbidden")
    return await service.get_day_phrase(uid, session)


@router.post("/", response_model=DayPhraseRead)
async def create_day_phrase(
        new_phrase: DayPhraseCreate,
        current_user: User = Depends(auth_service.get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    if current_user.id != new_phrase.uid:
        raise HTTPException(status_code=403, detail="Access forbidden")

    return await service.create_phrase(session, new_phrase)


@router.put("/{uid}", response_model=DayPhraseRead)
async def update_day_phrase(
        uid: int,
        upd_phrase: DayPhraseUpdate,
        current_user: User = Depends(auth_service.get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    if current_user.id != uid:
        raise HTTPException(status_code=403, detail="Access forbidden")

    return await service.update_phrase(session, uid, upd_phrase)


@router.delete("/{uid}", response_model=DayPhraseRead)
async def delete_day_phrase(
        uid: int,
        current_user: User = Depends(auth_service.get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    if current_user.id != uid:
        raise HTTPException(status_code=403, detail="Access forbidden")

    return await service.delete_phrase(session, uid)
