"""Create stations and bikes tables

Revision ID: 002_stations_bikes
Revises: 001_initial_users
Create Date: 2024-05-20 22:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "002_stations_bikes"
down_revision: Union[str, None] = "001_initial_users"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum type for bike status
    bikestatus_enum = sa.Enum('AVAILABLE', 'RESERVED', 'IN_USE', 'MAINTENANCE', 'RETIRED', 
                               name='bikestatus', create_type=True)
    bikestatus_enum.create(op.get_bind(), checkfirst=True)
    
    # Create stations table
    op.create_table(
        'stations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('capacity', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create bikes table
    op.create_table(
        'bikes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('station_id', sa.Integer(), nullable=False),
        sa.Column('qr_code_hash', sa.String(), nullable=False),
        sa.Column('model', sa.String(), nullable=True),
        sa.Column('status', bikestatus_enum, nullable=False, server_default='AVAILABLE'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('last_maintenance', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['station_id'], ['stations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bikes_qr_code_hash'), 'bikes', ['qr_code_hash'], unique=True)
    op.create_index(op.f('ix_bikes_station_id'), 'bikes', ['station_id'])
    op.create_index(op.f('ix_bikes_status'), 'bikes', ['status'])


def downgrade() -> None:
    op.drop_index(op.f('ix_bikes_status'), table_name='bikes')
    op.drop_index(op.f('ix_bikes_station_id'), table_name='bikes')
    op.drop_index(op.f('ix_bikes_qr_code_hash'), table_name='bikes')
    op.drop_table('bikes')
    op.drop_table('stations')
    op.execute('DROP TYPE bikestatus')
