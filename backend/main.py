from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from auth import get_current_user
from database import get_session, init_db
from routers import feed, lists, search, spots, users
from routers.users import upsert_user


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(lists.router)
app.include_router(spots.router)
app.include_router(feed.router)
app.include_router(search.router)


# ---------------------------------------------------------------------------
# Core endpoints
# ---------------------------------------------------------------------------

@app.get("/")
async def health_check():
    return {"status": "ok"}


@app.get("/auth/me")
async def get_me(
    claims: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Verify Cognito JWT and upsert user row on every login."""
    user = await upsert_user(claims, session)
    return {"user": user}
