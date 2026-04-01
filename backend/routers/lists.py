import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from auth import get_current_user
from database import get_session
from models import Activity, List, ListCreate, ListLike, ListUpdate

router = APIRouter(prefix="/api/lists", tags=["lists"])


@router.post("", response_model=List, status_code=status.HTTP_201_CREATED)
async def create_list(
    body: ListCreate,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    lst = List(**body.model_dump(), user_id=current_user["sub"])
    session.add(lst)

    activity = Activity(
        user_id=current_user["sub"],
        type="LIST_CREATED",
        target_id=str(lst.id),
        target_type="LIST",
    )
    session.add(activity)
    await session.commit()
    await session.refresh(lst)
    return lst


@router.get("", response_model=list[List])
async def get_lists(
    user_id: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
):
    stmt = select(List).where(List.is_public == True)
    if user_id:
        stmt = stmt.where(List.user_id == user_id)
    stmt = stmt.order_by(List.created_at.desc())
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{list_id}", response_model=List)
async def get_list(list_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    lst = await session.get(List, list_id)
    if not lst:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List not found")
    return lst


@router.patch("/{list_id}", response_model=List)
async def update_list(
    list_id: uuid.UUID,
    body: ListUpdate,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    lst = await session.get(List, list_id)
    if not lst:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List not found")
    if lst.user_id != current_user["sub"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(lst, field, value)
    lst.updated_at = datetime.now(timezone.utc)
    session.add(lst)
    await session.commit()
    await session.refresh(lst)
    return lst


@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_list(
    list_id: uuid.UUID,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    lst = await session.get(List, list_id)
    if not lst:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List not found")
    if lst.user_id != current_user["sub"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await session.delete(lst)
    await session.commit()


@router.post("/{list_id}/like", status_code=status.HTTP_204_NO_CONTENT)
async def like_list(
    list_id: uuid.UUID,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    lst = await session.get(List, list_id)
    if not lst:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List not found")

    existing = await session.get(ListLike, (current_user["sub"], list_id))
    if existing:
        return  # already liked

    like = ListLike(user_id=current_user["sub"], list_id=list_id)
    session.add(like)
    lst.like_count += 1
    session.add(lst)

    activity = Activity(
        user_id=current_user["sub"],
        type="LIST_LIKED",
        target_id=str(list_id),
        target_type="LIST",
    )
    session.add(activity)
    await session.commit()


@router.delete("/{list_id}/like", status_code=status.HTTP_204_NO_CONTENT)
async def unlike_list(
    list_id: uuid.UUID,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    like = await session.get(ListLike, (current_user["sub"], list_id))
    if not like:
        return

    lst = await session.get(List, list_id)
    if lst and lst.like_count > 0:
        lst.like_count -= 1
        session.add(lst)

    await session.delete(like)
    await session.commit()
