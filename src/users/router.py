from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_async_session
from src.users.models import GlobalStats
from src.users.service import StatsService

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)


@router.get("/{uid}")
async def get_user_and_stats(uid: int, session: AsyncSession = Depends(get_async_session)):
    await StatsService.update_global_stats(session, uid)
    stats = await StatsService.get_stats_by_uid(uid, session)
    user = await StatsService.get_user_by_uid(uid, session)

    return {"user": user, "stats": stats}
