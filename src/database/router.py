from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from database.database import SessionLocal

router = APIRouter(
    prefix="/api/ping",
    tags=["Database"]
)


@router.get("/")
async def check_db_connection():
    async with SessionLocal() as session:
        async with session.begin():
            try:
                await session.execute(text("SELECT 1"))
                return {"status": "Database is working"}
            except Exception:
                raise HTTPException(status_code=500, detail="Database is not responding")
