import secrets

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from PIL import Image

from src.database.database import get_async_session
from src.database.models import User
from src.users import service
from src.auth import service as auth_service
from src.auth.schemas import Token
from src.config import TOKEN_EXPIRATION
from src.users.schemas import UserRead, UserWithWorkoutsAndStats, UserLogin

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)


@router.post("/register", response_model=UserRead)
async def register_user(new_user: UserLogin, session: AsyncSession = Depends(get_async_session)):
    return await auth_service.register_user(session, new_user)


@router.post("/login")
async def login_user(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_async_session)
):
    if not (user := await auth_service.authenticate_user(form_data.username, form_data.password, session)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=TOKEN_EXPIRATION)
    access_token = auth_service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer", uid=user.id)


@router.get("/{uid}", response_model=UserRead)
async def get_user(
        uid: int,
        current_user: User = Depends(auth_service.current_user_getter_strict),
        session: AsyncSession = Depends(get_async_session)
):
    if current_user.id != uid:
        raise HTTPException(status_code=403, detail="Access forbidden")
    return await service.get_user_by_uid(uid, session)


@router.get("/stats/{uid}", response_model=UserWithWorkoutsAndStats)
async def get_user_with_stats(
        uid: int,
        current_user: User = Depends(auth_service.current_user_getter_strict),
        session: AsyncSession = Depends(get_async_session)
):
    if current_user.id != uid:
        raise HTTPException(status_code=403, detail="Access forbidden")
    return await service.get_user_with_stats_and_workouts(session, uid)


@router.post("/{uid}/picture/upload", response_model=UserRead)
async def upload_photo(
        uid: int,
        file: UploadFile = File(...),
        current_user: User = Depends(auth_service.current_user_getter_strict),
        session: AsyncSession = Depends(get_async_session)
):
    if current_user.id != uid:
        raise HTTPException(status_code=403, detail="Access forbidden")
    return await service.upload_photo(uid, file, session)


@router.delete("/{uid}/picture/delete", response_model=UserRead)
async def delete_photo(
        uid: int,
        current_user: User = Depends(auth_service.current_user_getter_strict),
        session: AsyncSession = Depends(get_async_session)
):
    if current_user.id != uid:
        raise HTTPException(status_code=403, detail="Access forbidden")
    return await service.delete_photo(uid, session)


@router.post("/{uid}/login/change", response_model=UserRead)
async def change_login(
        uid: int,
        new_login: str,
        current_user: User = Depends(auth_service.current_user_getter_strict),
        session: AsyncSession = Depends(get_async_session)
):
    if current_user.id != uid:
        raise HTTPException(status_code=403, detail="Access forbidden")
    return await service.change_login(uid, new_login, session)


@router.post("/{uid}/password/change", response_model=UserRead)
async def change_password(
        uid: int,
        old_password: str,
        new_password: str,
        current_user: User = Depends(auth_service.current_user_getter_strict),
        session: AsyncSession = Depends(get_async_session)
):
    if current_user.id != uid:
        raise HTTPException(status_code=403, detail="Access forbidden")
    return await service.change_password(uid, old_password, new_password, session)
