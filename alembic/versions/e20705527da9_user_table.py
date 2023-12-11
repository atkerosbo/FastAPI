"""User table

Revision ID: e20705527da9
Revises: 8881983da45b
Create Date: 2023-12-11 12:20:25.930935

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e20705527da9'
down_revision: Union[str, None] = '8881983da45b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer, nullable= False,),
                    sa.Column('email', sa.String, nullable= False, unique= True),
                    sa.Column('password', sa.String, nullable= False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )

    pass


def downgrade() -> None:
    op.drop_table('users')
    

    pass
