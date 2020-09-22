"""empty message

Revision ID: 627a93f294dc
Revises: fe6a3d4f5353
Create Date: 2020-09-22 04:35:25.693402

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '627a93f294dc'
down_revision = 'fe6a3d4f5353'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('doctor', sa.Column('doctorNumber', sa.String(length=300), nullable=False))
    op.create_unique_constraint(None, 'doctor', ['doctorNumber'])
    op.add_column('patient', sa.Column('patientHash', sa.String(length=300), nullable=False))
    op.create_unique_constraint(None, 'patient', ['patientHash'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'patient', type_='unique')
    op.drop_column('patient', 'patientHash')
    op.drop_constraint(None, 'doctor', type_='unique')
    op.drop_column('doctor', 'doctorNumber')
    # ### end Alembic commands ###
