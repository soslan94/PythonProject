"""initial schema

Revision ID: fc8b4f564369
Revises: a5799e23b8d8
Create Date: 2025-07-08 11:49:23.290596

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'fc8b4f564369'
down_revision: Union[str, Sequence[str], None] = 'a5799e23b8d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()

    # 1) Дроп старых определений, чтобы не ломаться
    op.execute("DROP TYPE IF EXISTS colorenum CASCADE;")
    op.execute("DROP TYPE IF EXISTS sizeenum CASCADE;")
    op.execute("DROP TYPE IF EXISTS userrole CASCADE;")

    # 2) Создаём ENUM‑типы (checkfirst защитит от повторного создания)
    color_enum = postgresql.ENUM('pink','black','white','yellow', name='colorenum')
    color_enum.create(bind, checkfirst=True)
    size_enum  = postgresql.ENUM('xs','s','m','l','xl','xxl',    name='sizeenum')
    size_enum.create(bind,  checkfirst=True)
    userrole_enum = postgresql.ENUM('super_admin','admin','user', name='userrole')
    userrole_enum.create(bind, checkfirst=True)

    # 3) Таблицы – перечисления вставляем с create_type=False, чтобы
    #    SQLAlchemy не пытался создавать их снова
    op.create_table(
        'clothes',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(120), nullable=False),
        sa.Column(
            'color',
            postgresql.ENUM('pink','black','white','yellow', name='colorenum', create_type=False),
            nullable=False
        ),
        sa.Column(
            'size',
            postgresql.ENUM('xs','s','m','l','xl','xxl', name='sizeenum', create_type=False),
            nullable=False
        ),
        sa.Column('photo_url', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('last_modified_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    )

    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(120), nullable=False),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(200), nullable=False),
        sa.Column('phone', sa.String(13), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('last_modified_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column(
            'role',
            postgresql.ENUM('super_admin','admin','user', name='userrole', create_type=False),
            nullable=False
        ),
        sa.UniqueConstraint('email'),
    )

def downgrade() -> None:
    bind = op.get_bind()
    # Удаляем таблицы
    op.drop_table('users')
    op.drop_table('clothes')
    # Дропаем типы
    postgresql.ENUM(name='userrole').drop(bind, checkfirst=True)
    postgresql.ENUM(name='sizeenum').drop(bind, checkfirst=True)
    postgresql.ENUM(name='colorenum').drop(bind, checkfirst=True)