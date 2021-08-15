"""remove user type field

Revision ID: f3c3e7ba9ea9
Revises: 5200c42123c4
Create Date: 2021-08-15 18:28:24.379596

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f3c3e7ba9ea9"
down_revision = "5200c42123c4"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint("admins_email_unique", "admins", ["email"])
    op.drop_column("admins", "user_type")
    op.create_unique_constraint("agents_email_unique", "agents", ["email"])
    op.drop_column("agents", "user_type")
    op.create_unique_constraint("user_email_unique", "users", ["email"])
    op.drop_column("users", "user_type")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column("user_type", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.drop_constraint("user_email_unique", "users", type_="unique")
    op.add_column(
        "agents",
        sa.Column("user_type", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.drop_constraint("agents_email_unique", "agents", type_="unique")
    op.add_column(
        "admins",
        sa.Column("user_type", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.drop_constraint("admins_email_unique", "admins", type_="unique")
    # ### end Alembic commands ###
