"""added users table is superuser field

Revision ID: 2b110c57bb18
Revises: b30aba94299a
Create Date: 2025-03-29 07:27:41.220543

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2b110c57bb18"
down_revision: Union[str, None] = "b30aba94299a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("is_superuser", sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "is_superuser")
    # ### end Alembic commands ###
