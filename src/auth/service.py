from datetime import timedelta, timezone, datetime

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import TokenData
from src.config import JWT_ALG, JWT_SECRET
from src.database.database import get_async_session
from src.database.models import User
from src.users import service as user_service
from src.users.schemas import UserLogin
from src.users.service import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login", auto_error=False)  # Не будет выбрасываться 401 автомаатически
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str, session: AsyncSession) -> bool | User:
    try:
        # Ищем юзера с таким никнеймом
        user = await get_user_by_username(username, session)
        if not verify_password(password, user.password):
            # Если такой юзер есть, но пароли не совпадают
            return False
        return user
    except HTTPException as _:
        # Если такого юзера не оказалось
        return False


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALG)
    return encoded_jwt


async def register_user(session: AsyncSession, new_user: UserLogin):
    try:
        # Пробуем получить юзера
        await user_service.get_user_by_username(new_user.username, session)
    except HTTPException as _:
        # Если юзера с таким никнеймом нет - значит он свободен, регистрируем
        to_add = User(username=new_user.username, password=hash_password(new_user.password))
        session.add(to_add)
        await session.commit()
        await session.refresh(to_add)
        return to_add

    # Если такой юзер уже есть, выкидываем 409
    raise HTTPException(status_code=409, detail="Such username already exists")


async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_async_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    try:
        user = await get_user_by_username(username=token_data.username, session=session)
    except HTTPException as _:
        raise credentials_exception
    return user


class CurrentUserManager:
    def __init__(self, strict: bool = True):
        self.strict = strict

    async def __call__(self, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_async_session)):
        if self.strict:
            if token is not None:
                return await get_current_user(token, session)
            raise HTTPException(status_code=401, detail="Not authorized")
        else:
            if token is not None:
                return await get_current_user(token, session)
            return None


current_user_getter_moderate = CurrentUserManager(strict=False)
current_user_getter_strict = CurrentUserManager(strict=True)
