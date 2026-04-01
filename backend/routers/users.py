from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert

from auth import get_current_user
from database import get_session
from models import User

router = APIRouter(prefix="/users", tags=["users"])


async def upsert_user(claims: dict, session: AsyncSession) -> User:
    """Create or update a user row from Cognito JWT claims."""
    user_id = claims["sub"]
    email = claims.get("email", "")
    username = claims.get("cognito:username", email.split("@")[0])
    name = claims.get("name", username)

    stmt = (
        pg_insert(User)
        .values(id=user_id, username=username, email=email, name=name)
        .on_conflict_do_update(
            index_elements=["id"],
            set_={"email": email, "name": name},
        )
        .returning(User)
    )
    result = await session.execute(stmt)
    await session.commit()
    row = result.fetchone()
    return row[0]


@router.get("/me", response_model=User)
async def get_me(
    claims: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await upsert_user(claims, session)


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
