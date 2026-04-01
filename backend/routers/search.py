from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import List

router = APIRouter(prefix="/search", tags=["search"])

_SEARCH_QUERY = text("""
    SELECT *
    FROM lists
    WHERE is_public = true
      AND to_tsvector('english', title || ' ' || coalesce(description, '') || ' ' || coalesce(category, ''))
          @@ plainto_tsquery('english', :q)
    ORDER BY like_count DESC
    LIMIT :limit
""")


@router.get("", response_model=list[dict])
async def search_lists(
    q: str = Query(min_length=1),
    limit: int = Query(default=20, le=100),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(_SEARCH_QUERY, {"q": q, "limit": limit})
    rows = result.mappings().all()
    return [dict(r) for r in rows]
