from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_async_session
from src.database.models import User
from src.statistics.global_stats_service import GlobalStatsService
from src.statistics.local_stats_service import LocalStatsService
from src.workouts import service
from src.workouts import service as workout_service
from src.workouts.schemas import WorkoutRead, WorkoutCreate, WorkoutWithStatsRead
from src.auth import service as auth_service


router = APIRouter(
    prefix="/api/workouts",
    tags=["Workouts"]
)


@router.get("/{uid}", response_model=List[WorkoutRead])
async def get_workouts(
        uid: int,
        current_user: User = Depends(auth_service.get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    if current_user.id != uid:
        raise HTTPException(status_code=403, detail="Access forbidden")

    return await service.get_workouts(session, uid)


@router.get("/stats/{uid}", response_model=List[WorkoutWithStatsRead])
async def get_workouts_with_stats(
        uid: int,
        current_user: User = Depends(auth_service.get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    if current_user.id != uid:
        raise HTTPException(status_code=403, detail="Access forbidden")

    return await service.get_workouts_with_stats(session, uid)


@router.get("/global_stats/{wid}")
async def update_global_stats(
        wid: int,
        current_user: User = Depends(auth_service.get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    uid = await workout_service.get_uid_by_wid(wid, session)
    if current_user.id != uid:
        raise HTTPException(status_code=403, detail="Access forbidden")

    await GlobalStatsService.calculate_stats(session, uid)


@router.post("/{wid}")
async def save_workout(
        wid: int,
        current_user: User = Depends(auth_service.get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    uid = await workout_service.get_uid_by_wid(wid, session)
    if current_user.id != uid:
        raise HTTPException(status_code=403, detail="Access forbidden")

    await LocalStatsService.calculate_stats(session, wid)
    target_endpoint = f"global_stats/{wid}"
    response = RedirectResponse(url=target_endpoint, status_code=303)
    return response


@router.post("/", response_model=WorkoutRead)
async def create_workout(
        new_workout: WorkoutCreate,
        current_user: User = Depends(auth_service.get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    if current_user.id != new_workout.uid:
        raise HTTPException(status_code=403, detail="Access forbidden")

    return await service.create_workout(session, new_workout)


@router.put("/{wid}/", response_model=WorkoutRead)
async def update_workout(
        wid: int,
        upd_workout: WorkoutRead,
        current_user: User = Depends(auth_service.get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    uid = await workout_service.get_uid_by_wid(wid, session)
    if uid != upd_workout.uid or uid != current_user.id:
        # Если uid, полученный из wid в адресе запроса не равен uid, который лежит в теле запроса или
        # если uid, полученный из wid в адресе запроса не равен uid текущего юзера
        raise HTTPException(status_code=403, detail="Access forbidden")
    if wid != upd_workout.id:
        raise HTTPException(status_code=404, detail=f"Wid from route doesn't match wid from payload")

    return await service.update_workout(wid, upd_workout, session)


@router.delete("/{wid}/", response_model=WorkoutRead)
async def delete_workout(
        wid: int,
        current_user: User = Depends(auth_service.get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    uid = await workout_service.get_uid_by_wid(wid, session)
    if current_user.id != uid:
        raise HTTPException(status_code=403, detail="Access forbidden")

    return await service.delete_workout(session, wid)
