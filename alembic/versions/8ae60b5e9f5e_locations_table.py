"""locations table

Revision ID: 8ae60b5e9f5e
Revises: 9814a6695f71
Create Date: 2021-08-14 15:37:43.889360

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ae60b5e9f5e'
down_revision = '9814a6695f71'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('locations',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('run_id', sa.String(), nullable=False),
    sa.Column('lat', sa.Float(), nullable=False),
    sa.Column('lon', sa.Float (), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['run_id'], ['runs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('locations')
    # ### end Alembic commands ###