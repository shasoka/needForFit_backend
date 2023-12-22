from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User


async def get_user_by_uid(session: AsyncSession, uid: int):
    query = select(User).where(User.id == uid)
    result = await session.execute(query)
    user = result.scalars().first()
    return user.exclude("password")
