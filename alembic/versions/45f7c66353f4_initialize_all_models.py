"""initialize all models

Revision ID: 45f7c66353f4
Revises:
Create Date: 2023-10-16 11:46:50.753722

"""

from typing import Sequence, Union

from app import models  # noqa
from app.models import users  # noqa

# revision identifiers, used by Alembic.
revision: str = "45f7c66353f4"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
