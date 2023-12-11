"""Add content to post table

Revision ID: 8881983da45b
Revises: 58107d87c4fd
Create Date: 2023-12-11 12:13:28.500711

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8881983da45b'
down_revision: Union[str, None] = '58107d87c4fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    
    pass
