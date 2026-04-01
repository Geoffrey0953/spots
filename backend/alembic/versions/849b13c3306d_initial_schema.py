"""initial schema

Revision ID: 849b13c3306d
Revises:
Create Date: 2026-02-19 17:02:40.793361

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '849b13c3306d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # users
    op.create_table(
        'users',
        sa.Column('id', sa.Text(), primary_key=True),
        sa.Column('username', sa.Text(), nullable=False),
        sa.Column('email', sa.Text(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('avatar_url', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email'),
    )

    # lists
    op.create_table(
        'lists',
        sa.Column('id', sa.Uuid(), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', sa.Text(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.Text(), nullable=True),
        sa.Column('is_public', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('like_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # spots
    op.create_table(
        'spots',
        sa.Column('id', sa.Uuid(), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('list_id', sa.Uuid(), sa.ForeignKey('lists.id', ondelete='CASCADE'), nullable=False),
        sa.Column('rank', sa.Integer(), nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('lat', sa.Numeric(), nullable=True),
        sa.Column('lng', sa.Numeric(), nullable=True),
        sa.Column('image_url', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.UniqueConstraint('list_id', 'rank', name='uq_spots_list_rank'),
    )

    # follows
    op.create_table(
        'follows',
        sa.Column('follower_id', sa.Text(), sa.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('following_id', sa.Text(), sa.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # list_likes
    op.create_table(
        'list_likes',
        sa.Column('user_id', sa.Text(), sa.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('list_id', sa.Uuid(), sa.ForeignKey('lists.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # activities
    op.create_table(
        'activities',
        sa.Column('id', sa.Uuid(), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', sa.Text(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('type', sa.Text(), nullable=False),
        sa.Column('target_id', sa.Text(), nullable=False),
        sa.Column('target_type', sa.Text(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # Full-text search index on lists
    op.execute(
        "CREATE INDEX lists_fts ON lists USING GIN ("
        "  to_tsvector('english', title || ' ' || coalesce(description, '') || ' ' || coalesce(category, ''))"
        ")"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS lists_fts")
    op.drop_table('activities')
    op.drop_table('list_likes')
    op.drop_table('follows')
    op.drop_table('spots')
    op.drop_table('lists')
    op.drop_table('users')
