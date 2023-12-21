from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Exercise


async def get_exercises(session: AsyncSession):
    return await session.execute(select(Exercise))
