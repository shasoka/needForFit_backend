from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, aliased

from src.database.models import Exercise, Approach


async def get_exercises(session: AsyncSession):
    return await session.execute(select(Exercise))
