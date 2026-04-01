import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from auth import get_current_user
from database import get_session
from models import Activity, List, Spot, SpotCreate, SpotUpdate

router = APIRouter(prefix="/api/lists/{list_id}/spots", tags=["spots"])


async def _get_list_or_404(list_id: uuid.UUID, session: AsyncSession) -> List:
    lst = await session.get(List, list_id)
    if not lst:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List not found")
    return lst


@router.get("", response_model=list[Spot])
async def get_spots(list_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    await _get_list_or_404(list_id, session)
    result = await session.execute(
        select(Spot).where(Spot.list_id == list_id).order_by(Spot.rank)
    )
    return result.scalars().all()


@router.post("", response_model=Spot, status_code=status.HTTP_201_CREATED)
async def create_spot(
    list_id: uuid.UUID,
    body: SpotCreate,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    lst = await _get_list_or_404(list_id, session)
    if lst.user_id != current_user["sub"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    spot = Spot(**body.model_dump(), list_id=list_id)
    session.add(spot)

    activity = Activity(
        user_id=current_user["sub"],
        type="SPOT_ADDED",
        target_id=str(spot.id),
        target_type="SPOT",
    )
    session.add(activity)
    await session.commit()
    await session.refresh(spot)
    return spot


@router.patch("/{spot_id}", response_model=Spot)
async def update_spot(
    list_id: uuid.UUID,
    spot_id: uuid.UUID,
    body: SpotUpdate,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    lst = await _get_list_or_404(list_id, session)
    if lst.user_id != current_user["sub"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    spot = await session.get(Spot, spot_id)
    if not spot or spot.list_id != list_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Spot not found")

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(spot, field, value)
    session.add(spot)
    await session.commit()
    await session.refresh(spot)
    return spot


@router.delete("/{spot_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_spot(
    list_id: uuid.UUID,
    spot_id: uuid.UUID,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    lst = await _get_list_or_404(list_id, session)
    if lst.user_id != current_user["sub"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    spot = await session.get(Spot, spot_id)
    if not spot or spot.list_id != list_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Spot not found")

    await session.delete(spot)
    await session.commit()
