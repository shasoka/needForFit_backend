import secrets

from PIL import Image
from fastapi import HTTPException, UploadFile
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.config import SERVER_HOST, SERVER_PORT
from src.database.models import User, Workout


async def get_user_by_uid(uid: int, session: AsyncSession):
    query = select(User).where(User.id == uid)
    result = await session.execute(query)
    user = result.scalar()
    if user is not None:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


async def upload_photo(uid: int, file: UploadFile, session: AsyncSession):
    extension = file.filename.split(".")[-1]
    if extension not in ["jpg", "jpeg", "png"]:
        raise HTTPException(status_code=415, detail="Unsupported media format")

    token_name = "_" + secrets.token_hex(16) + "." + extension
    file_path = "./static/images/users/" + token_name

    # Запись полученных байтов в файл
    file_content = await file.read()
    with open(file_path, "wb") as f:
        f.write(file_content)
    # Ресайз изображения
    image = Image.open(file_path)
    image = image.resize((235, 235))
    image.save(file_path)

    # Обновление записи пользователя в базе данных
    await session.execute(
        update(User)
        .where(User.id == uid)
        .values(profile_picture=SERVER_HOST+":"+SERVER_PORT+file_path[1:])
    )
    await session.commit()

    # Получение и возврат обновленного пользователя
    updated_user = await get_user_by_uid(uid, session)
    return updated_user


async def get_user_by_username(username: str, session: AsyncSession) -> User:
    query = select(User).where(User.username == username)
    result = await session.execute(query)
    user = result.scalar()
    if user is not None:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


async def get_user_with_stats_and_workouts(session: AsyncSession, uid: int):
    user = await session.execute(select(User).where(User.id == uid).options(selectinload(User.stat)))
    workouts = await session.execute(select(Workout).where(Workout.uid == uid).options(selectinload(Workout.stat), selectinload(Workout.workout_type)))
    return {"user": user.scalar(), "workouts": workouts.scalars().all()}
