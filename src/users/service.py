import os
import secrets

from PIL import Image
from fastapi import HTTPException, UploadFile
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.config import SERVER_HOST, SERVER_PORT
from src.database.models import User, Workout
from src.auth import service as auth_service


async def get_user_by_uid(uid: int, session: AsyncSession):
    query = select(User).where(User.id == uid)
    result = await session.execute(query)
    user = result.scalar()
    if user is not None:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


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


async def upload_photo(uid: int, file: UploadFile, session: AsyncSession):
    extension = file.filename.split(".")[-1]
    if extension not in ["jpg", "jpeg", "png"]:
        raise HTTPException(status_code=415, detail="Unsupported media format")

    token_name = secrets.token_hex(16) + "." + extension
    file_path = "./static/images/users/" + token_name

    # Запись полученных байтов в файл
    file_content = await file.read()
    if len(file_content) > 1 * 1024 * 1024:  # 1,00 MB
        raise HTTPException(status_code=413, detail="File size exceeds 1 MB")

    # Получение текущего пользователя
    user = await get_user_by_uid(uid, session)

    # Проверка на наличие "profile_picture_placeholder" в имени файла
    if "profile_picture_placeholder" not in user.profile_picture:
        old_file_path = "." + user.profile_picture.split(SERVER_HOST+":"+SERVER_PORT)[1]
        os.remove(old_file_path)

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
    return await get_user_by_uid(uid, session)


async def delete_photo(uid: int, session: AsyncSession):
    user = await get_user_by_uid(uid, session)
    if "profile_picture_placeholder" not in user.profile_picture:
        path = "." + user.profile_picture.split(SERVER_HOST+":"+SERVER_PORT)[1]
        # Удаление файла
        os.remove(path)
        # Обновление записи пользователя в базе данных
        await session.execute(
            update(User).
            where(User.id == uid).
            values(profile_picture=SERVER_HOST+":"+SERVER_PORT+"/static/images/users/profile_picture_placeholder.png")
        )
        await session.commit()

        # Получение и возврат обновленного пользователя
        return await get_user_by_uid(uid, session)
    else:
        raise HTTPException(status_code=403, detail="Access denied for deleting default profile picture")


async def change_login(uid: int, new_login: str, session: AsyncSession):
    try:
        await session.execute(
            update(User).
            where(User.id == uid).
            values(username=new_login)
        )
        await session.commit()

        # Получение и возврат обновленного пользователя
        return await get_user_by_uid(uid, session)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Username already in use")


async def change_password(uid: int, old_password: str, new_password: str, session: AsyncSession):
    if auth_service.verify_password(old_password, (await get_user_by_uid(uid, session)).password):
        await session.execute(
            update(User).
            where(User.id == uid).
            values(password=auth_service.hash_password(new_password))
        )
        await session.commit()

        # Получение и возврат обновленного пользователя
        return await get_user_by_uid(uid, session)

    raise HTTPException(status_code=403, detail="Incorrect old password")
