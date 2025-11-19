"""init

Revision ID: e1ad25e6055a
Revises: 
Create Date: 2025-09-05 17:59:24.838401

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1ad25e6055a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    auction_enum = sa.Enum('COPART', 'IAAI', name='auctionenum')
    destination_enum = sa.Enum('Klaipeda', 'Rotterdam', 'Poti', 'Jebel Ali', name='destinationenum')
    terminal_enum = sa.Enum('new york', 'savannah', 'miami', 'chicago', name='terminalenum')
    invoice_type_enum = sa.Enum('navi_grupe_invoice', 't_autologistics_invoice', name='invoicetypeenum')
    fee_type_enum = sa.Enum('clean_title_fee', 'non_clean_title_fee', 'crashed_toys_fee', 'less_fee', name='feetypeenum')
    order_status_enum = sa.Enum(
        'pending_payment',
        'paid',
        'unpaid',
        'picked_up',
        'delivered_terminal',
        'no_title',
        'loaded_into_container',
        name='orderstatusenum'
    )
    appeal_message_role_enum = sa.Enum('user', 'admin', name='appealmessageroleenum')

    auction_enum.create(op.get_bind(), checkfirst=True)
    destination_enum.create(op.get_bind(), checkfirst=True)
    terminal_enum.create(op.get_bind(), checkfirst=True)
    invoice_type_enum.create(op.get_bind(), checkfirst=True)
    fee_type_enum.create(op.get_bind(), checkfirst=True)
    order_status_enum.create(op.get_bind(), checkfirst=True)
    appeal_message_role_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        'containers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('destination', destination_enum, nullable=False),
        sa.Column('ship_line', sa.String(), nullable=False, server_default='Unknown'),
        sa.Column('vessel', sa.String(), nullable=False, server_default='Unknown'),
        sa.Column('container_key', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('container_key')
    )
    op.create_index(op.f('ix_containers_id'), 'containers', ['id'], unique=False)

    op.create_table(
        'orders',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.Column('auction_name', sa.String(), nullable=False, server_default='Dealer'),
        sa.Column('lot_id', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('from_dealer', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('terminal', terminal_enum, nullable=False),
        sa.Column('car_value', sa.Integer(), nullable=False),
        sa.Column('extra_fee', sa.JSON(), nullable=True),
        sa.Column('invoice_items', sa.JSON(), nullable=True),
        sa.Column('invoice_type', invoice_type_enum, nullable=False, server_default='navi_grupe_invoice'),
        sa.Column('vehicle_type', sa.String(), nullable=False, server_default='CAR'),
        sa.Column('vin', sa.String(), nullable=False),
        sa.Column('vehicle_name', sa.String(), nullable=False),
        sa.Column('keys', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('damage', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('color', sa.String(), nullable=False, server_default='Unknown'),
        sa.Column('auto_generated', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('fee_type', fee_type_enum, nullable=False, server_default='non_clean_title_fee'),
        sa.Column('delivery_status', order_status_enum, nullable=False, server_default='pending_payment'),
        sa.Column('container_id', sa.Integer(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('location_id', sa.Integer(), nullable=True),
        sa.Column('auction', auction_enum, nullable=False, server_default='COPART'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('vin'),
        sa.ForeignKeyConstraint(['container_id'], ['containers.id'], ondelete='SET NULL')
    )
    op.create_index(op.f('ix_orders_id'), 'orders', ['id'], unique=False)

    op.create_table(
        'order_status_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('status', order_status_enum, nullable=False),
        sa.Column('changed_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_status_history_id'), 'order_status_history', ['id'], unique=False)

    op.create_table(
        'order_depth_video',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('video_url', sa.String(), nullable=True),
        sa.Column('requested', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('order_id')
    )
    op.create_index(op.f('ix_order_depth_video_id'), 'order_depth_video', ['id'], unique=False)

    op.create_table(
        'ship_lines',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ship_line', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ship_lines_id'), 'ship_lines', ['id'], unique=False)

    op.create_table(
        'appeals',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('reason', sa.String(), nullable=False),
        sa.Column('solved', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('order_id')
    )
    op.create_index(op.f('ix_appeals_id'), 'appeals', ['id'], unique=False)

    op.create_table(
        'appeal_messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('appeal_id', sa.Integer(), nullable=False),
        sa.Column('message', sa.String(), nullable=True),
        sa.Column('role', appeal_message_role_enum, nullable=False),
        sa.Column('seen', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['appeal_id'], ['appeals.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_appeal_messages_id'), 'appeal_messages', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_appeal_messages_id'), table_name='appeal_messages')
    op.drop_table('appeal_messages')

    op.drop_index(op.f('ix_appeals_id'), table_name='appeals')
    op.drop_table('appeals')

    op.drop_index(op.f('ix_ship_lines_id'), table_name='ship_lines')
    op.drop_table('ship_lines')

    op.drop_index(op.f('ix_order_depth_video_id'), table_name='order_depth_video')
    op.drop_table('order_depth_video')

    op.drop_index(op.f('ix_order_status_history_id'), table_name='order_status_history')
    op.drop_table('order_status_history')

    op.drop_index(op.f('ix_orders_id'), table_name='orders')
    op.drop_table('orders')

    op.drop_index(op.f('ix_containers_id'), table_name='containers')
    op.drop_table('containers')

    op.execute("DROP TYPE IF EXISTS appealmessageroleenum")
    op.execute("DROP TYPE IF EXISTS orderstatusenum")
    op.execute("DROP TYPE IF EXISTS invoicetypeenum")
    op.execute("DROP TYPE IF EXISTS terminalenum")
    op.execute("DROP TYPE IF EXISTS destinationenum")
    op.execute("DROP TYPE IF EXISTS auctionenum")
    op.execute("DROP TYPE IF EXISTS feetypeenum")
