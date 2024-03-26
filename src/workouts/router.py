from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_async_session
from src.schemas import TypesRead, TypeCreate
from src.statistics.global_stats_service import GlobalStatsService
from src.statistics.local_stats_service import LocalStatsService
from src.workouts import service
from src.workouts.schemas import WorkoutRead, WorkoutCreate, WorkoutWithStatsRead

from src.workouts import service as workout_service

router = APIRouter(
    prefix="/api/workouts",
    tags=["Workouts"]
)


@router.get("/{uid}", response_model=List[WorkoutRead])
async def get_workouts(uid: int, session: AsyncSession = Depends(get_async_session)):
    return await service.get_workouts(session, uid)


@router.get("/stats/{uid}", response_model=List[WorkoutWithStatsRead])
async def get_workouts_with_stats(uid: int, session: AsyncSession = Depends(get_async_session)):
    return await service.get_workouts_with_stats(session, uid)


@router.get("/global_stats/{wid}")
async def update_global_stats(wid: int, session: AsyncSession = Depends(get_async_session)):
    await GlobalStatsService.calculate_stats(session, await workout_service.get_uid_by_wid(wid, session))


@router.post("/{wid}")
async def save_workout(wid: int, session: AsyncSession = Depends(get_async_session)):
    await LocalStatsService.calculate_stats(session, wid)
    target_endpoint = f"global_stats/{wid}"
    response = RedirectResponse(url=target_endpoint, status_code=303)
    return response


@router.post("/", response_model=WorkoutRead)
async def create_workout(new_workout: WorkoutCreate, session: AsyncSession = Depends(get_async_session)):
    return await service.create_workout(session, new_workout)


@router.put("/{wid}/", response_model=WorkoutRead)
async def update_workout(wid: int, upd_workout: WorkoutRead, session: AsyncSession = Depends(get_async_session)):
    return await service.update_workout(wid, upd_workout, session)


@router.delete("/{wid}/")
async def delete_workout(wid: int, session: AsyncSession = Depends(get_async_session)):
    return await service.delete_workout(session, wid)


# ---------------- # ---------------- # ---------------- # ---------------- # ---------------- #


@router.get("/types/", response_model=List[TypesRead])
async def get_types_with_ids(session: AsyncSession = Depends(get_async_session)):
    return await service.get_workouts_types_with_ids(session)


@router.post("/types/", response_model=TypesRead)
async def create_type(new_type: TypeCreate, session: AsyncSession = Depends(get_async_session)):
    return await service.create_type(session, new_type)


@router.put("/types/{tid}/", response_model=TypesRead)
async def update_type(tid: int, upd_type: TypesRead, session: AsyncSession = Depends(get_async_session)):
    return await service.update_type(tid, upd_type, session)


@router.delete("/types/{tid}/")
async def delete_type(tid: int, session: AsyncSession = Depends(get_async_session)):
    return await service.delete_type(tid, session)
