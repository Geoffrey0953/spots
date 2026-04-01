from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional


def _now() -> datetime:
    return datetime.now(timezone.utc)

from sqlmodel import Field, SQLModel


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(primary_key=True)          # Cognito "sub" claim
    username: str = Field(unique=True)
    email: str = Field(unique=True)
    name: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime = Field(default_factory=_now)


# ---------------------------------------------------------------------------
# Lists
# ---------------------------------------------------------------------------

class List(SQLModel, table=True):
    __tablename__ = "lists"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    is_public: bool = Field(default=True)
    like_count: int = Field(default=0)
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)


class ListCreate(SQLModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    is_public: bool = True


class ListUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    is_public: Optional[bool] = None


# ---------------------------------------------------------------------------
# Spots
# ---------------------------------------------------------------------------

class Spot(SQLModel, table=True):
    __tablename__ = "spots"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    list_id: uuid.UUID = Field(foreign_key="lists.id")
    rank: int
    title: str
    notes: Optional[str] = None
    address: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    image_url: Optional[str] = None
    created_at: datetime = Field(default_factory=_now)


class SpotCreate(SQLModel):
    rank: int
    title: str
    notes: Optional[str] = None
    address: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    image_url: Optional[str] = None


class SpotUpdate(SQLModel):
    rank: Optional[int] = None
    title: Optional[str] = None
    notes: Optional[str] = None
    address: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    image_url: Optional[str] = None


# ---------------------------------------------------------------------------
# Follows
# ---------------------------------------------------------------------------

class Follow(SQLModel, table=True):
    __tablename__ = "follows"

    follower_id: str = Field(foreign_key="users.id", primary_key=True)
    following_id: str = Field(foreign_key="users.id", primary_key=True)
    created_at: datetime = Field(default_factory=_now)


# ---------------------------------------------------------------------------
# List Likes
# ---------------------------------------------------------------------------

class ListLike(SQLModel, table=True):
    __tablename__ = "list_likes"

    user_id: str = Field(foreign_key="users.id", primary_key=True)
    list_id: uuid.UUID = Field(foreign_key="lists.id", primary_key=True)
    created_at: datetime = Field(default_factory=_now)


# ---------------------------------------------------------------------------
# Activities
# ---------------------------------------------------------------------------

class Activity(SQLModel, table=True):
    __tablename__ = "activities"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    type: str                    # LIST_CREATED, SPOT_ADDED, LIST_LIKED, USER_FOLLOWED
    target_id: str               # UUID or user id of the target
    target_type: str             # LIST, SPOT, USER
    created_at: datetime = Field(default_factory=_now)
