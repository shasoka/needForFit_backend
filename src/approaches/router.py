from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.approaches import service
from src.approaches.schemas import ApproachRead, ApproachCreate, ApproachGrouped
from src.database.database import get_async_session
from src.database.models import User
from src.auth import service as auth_service
from src.workouts import service as workout_service


router = APIRouter(prefix="/api/approaches", tags=["Approaches"])


@router.get("/{wid}", response_model=List[ApproachGrouped])
async def get_approaches_by_wid_grouped(
        wid: int,
        current_user: User = Depends(auth_service.get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    uid = await workout_service.get_uid_by_wid(wid, session)
    if current_user.id != uid:
        raise HTTPException(status_code=403, detail="Access forbidden")

    return await service.get_approaches_by_wid_grouped_by_eid(session, wid)


@router.post("/", response_model=ApproachRead)
async def create_approach(
        new_approach: ApproachCreate,
        current_user: User = Depends(auth_service.get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    uid = await workout_service.get_uid_by_wid(new_approach.wid, session)
    if current_user.id != uid:
        raise HTTPException(status_code=403, detail="Access forbidden")

    return await service.create_approach(session, new_approach)


@router.put("/{aid}", response_model=ApproachRead)
async def update_approach(
        aid: int,
        upd_approach: ApproachRead,
        current_user: User = Depends(auth_service.get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    uid_from_wid = await workout_service.get_uid_by_wid(upd_approach.wid, session)
    uid_from_aid = await service.get_uid_by_aid(aid, session)
    if uid_from_aid != uid_from_wid or uid_from_aid != current_user.id:
        # Если uid, полученный из aid в адресе запроса не равен uid, который лежит в теле запроса (через wid) или
        # если uid, полученный из aid в адресе запроса не равен uid текущего юзера
        raise HTTPException(status_code=403, detail="Access forbidden")
    if aid != upd_approach.id:
        raise HTTPException(status_code=404, detail=f"Aid from route doesn't match aid from payload")

    return await service.update_approach(aid, upd_approach, session)


@router.delete("/{aid}", response_model=ApproachRead)
async def delete_approach(
        aid: int,
        current_user: User = Depends(auth_service.get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    uid = await service.get_uid_by_aid(aid, session)
    if uid != current_user.id:
        raise HTTPException(status_code=403, detail="Access forbidden")

    return await service.delete_approach(session, aid)


@router.delete("/{wid}/{eid}", response_model=List[ApproachRead])
async def delete_exercise_from_workout(
        wid: int,
        eid: int,
        current_user: User = Depends(auth_service.get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    uid = await workout_service.get_uid_by_wid(wid, session)
    if current_user.id != uid:
        raise HTTPException(status_code=403, detail="Access forbidden")

    return await service.delete_exercise_from_workout(session, wid, eid)
