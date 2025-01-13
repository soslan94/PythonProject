"""Initial_2

Revision ID: 2d68d85b1a80
Revises: fb73446f6786
Create Date: 2025-01-11 11:47:30.995620

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d68d85b1a80'
down_revision: Union[str, None] = 'fb73446f6786'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('pages', sa.INTEGER(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books', 'pages')
    # ### end Alembic commands ###
