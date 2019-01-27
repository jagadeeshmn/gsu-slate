"""Department & Program table

Revision ID: 2e68e79b2fba
Revises: 
Create Date: 2019-01-26 15:58:33.912996

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e68e79b2fba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('department',
    sa.Column('university', sa.String(length=40), nullable=False),
    sa.Column('dname', sa.String(length=40), nullable=True),
    sa.PrimaryKeyConstraint('university'),
    sa.UniqueConstraint('dname')
    )
    op.create_table('program',
    sa.Column('university', sa.String(length=40), nullable=True),
    sa.Column('dname', sa.String(length=40), nullable=True),
    sa.Column('program', sa.String(length=10), nullable=False),
    sa.Column('department_university', sa.String(length=40), nullable=True),
    sa.ForeignKeyConstraint(['department_university'], ['department.university'], ),
    sa.PrimaryKeyConstraint('program'),
    sa.UniqueConstraint('dname'),
    sa.UniqueConstraint('university')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('program')
    op.drop_table('department')
    # ### end Alembic commands ###
