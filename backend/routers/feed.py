from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from auth import get_current_user
from database import get_session
from models import List

router = APIRouter(prefix="/feed", tags=["feed"])

_FEED_QUERY = text("""
    SELECT a.*
    FROM activities a
    JOIN follows f ON f.following_id = a.user_id
    WHERE f.follower_id = :current_user_id
    ORDER BY a.created_at DESC
    LIMIT :limit OFFSET :offset
""")


@router.get("", response_model=list[dict])
async def get_feed(
    current_user: dict = Depends(get_current_user),
    limit: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        _FEED_QUERY,
        {"current_user_id": current_user["sub"], "limit": limit, "offset": offset},
    )
    rows = result.mappings().all()
    return [dict(r) for r in rows]


@router.get("/trending", response_model=list[List])
async def get_trending(
    limit: int = Query(default=20, le=100),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(List)
        .where(List.is_public == True)
        .order_by(List.like_count.desc())
        .limit(limit)
    )
    return result.scalars().all()
