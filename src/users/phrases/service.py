import random

from fastapi import HTTPException
from sqlalchemy import select, exists, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import DayPhrase
from src.users.phrases.schemas import DayPhraseCreate, DayPhraseUpdate


async def get_day_phrase(session: AsyncSession, uid: int = 0):
    # Попытка найти фразу, которая соответствует переданному uid
    user_phrase_result = await session.execute(select(DayPhrase).where(DayPhrase.uid == uid))
    user_phrase = user_phrase_result.scalars().first()

    if user_phrase:
        # Если фраза пользователя найдена, возвращаем ее
        return user_phrase
    else:
        # Если фраза пользователя не найдена, выбираем случайную фразу, у которой uid равен None
        null_uid_phrases_result = await session.execute(select(DayPhrase).where(DayPhrase.uid == None))
        null_uid_phrases = null_uid_phrases_result.scalars().all()
        if null_uid_phrases:
            return random.choice(null_uid_phrases)
        else:
            raise HTTPException(status_code=404, detail="No phrases found")


async def create_phrase(session: AsyncSession, new_phrase: DayPhraseCreate):
    # Проверка, существует ли уже фраза с данным uid
    exists_query = await session.execute(select(exists().where(DayPhrase.uid == new_phrase.uid)))
    exists_result = exists_query.scalar()

    if exists_result:
        # Если такая фраза существует, поднимаем исключение
        raise HTTPException(status_code=400, detail="Phrase with this uid already exists")
    else:
        # Если такой фразы нет, создаем новую запись в базе данных
        new_phrase_obj = DayPhrase(**new_phrase.dict())
        session.add(new_phrase_obj)
        await session.commit()
        await session.refresh(new_phrase_obj)
        return new_phrase_obj


async def update_phrase(session: AsyncSession, uid: int, upd_phrase: DayPhraseUpdate):
    # Попытка найти фразу, которую нужно обновить
    phrase_result = await session.execute(select(DayPhrase).where(DayPhrase.uid == uid))
    phrase = phrase_result.scalars().first()

    if phrase:
        # Если фраза найдена, обновляем ее
        await session.execute(
            update(DayPhrase).
            where(DayPhrase.uid == uid).
            values(**upd_phrase.dict())
        )
        await session.commit()

        # Получаем обновленную запись
        updated_phrase_result = await session.execute(select(DayPhrase).where(DayPhrase.uid == uid))
        updated_phrase = updated_phrase_result.scalars().first()

        return updated_phrase
    else:
        # Если фраза не найдена, поднимаем исключение
        raise HTTPException(status_code=404, detail="Phrase not found")


async def delete_phrase(session: AsyncSession, uid: int):
    # Попытка найти фразу, которую нужно удалить
    phrase_result = await session.execute(select(DayPhrase).where(DayPhrase.uid == uid))
    phrase = phrase_result.scalars().first()

    if phrase:
        # Если фраза найдена, удаляем ее
        await session.execute(
            delete(DayPhrase).
            where(DayPhrase.uid == uid)
        )
        await session.commit()
        return phrase
    else:
        # Если фраза не найдена, поднимаем исключение
        raise HTTPException(status_code=404, detail="Phrase not found")
