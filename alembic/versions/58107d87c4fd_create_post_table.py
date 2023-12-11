"""Create post table

Revision ID: 58107d87c4fd
Revises: 
Create Date: 2023-12-11 11:49:08.421629

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58107d87c4fd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer, nullable= True, primary_key= True),
                    sa.Column('title', sa.String, nullable= False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
