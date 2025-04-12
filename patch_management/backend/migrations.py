from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic
revision = 'initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create enum types
    op.execute("CREATE TYPE user_role AS ENUM ('admin', 'user')")
    op.execute("CREATE TYPE server_status AS ENUM ('online', 'offline', 'maintenance')")
    op.execute("CREATE TYPE patch_status AS ENUM ('pending', 'applied', 'failed')")
    op.execute("CREATE TYPE patch_severity AS ENUM ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW')")

    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('role', postgresql.ENUM('admin', 'user', name='user_role'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )

    # Create servers table
    op.create_table(
        'servers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('hostname', sa.String(), nullable=False),
        sa.Column('ip_address', sa.String(), nullable=False),
        sa.Column('os_version', sa.String(), nullable=False),
        sa.Column('status', postgresql.ENUM('online', 'offline', 'maintenance', name='server_status'), nullable=False),
        sa.Column('last_scan', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('hostname'),
        sa.UniqueConstraint('ip_address')
    )

    # Create patches table
    op.create_table(
        'patches',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('package_name', sa.String(), nullable=False),
        sa.Column('current_version', sa.String(), nullable=False),
        sa.Column('available_version', sa.String(), nullable=False),
        sa.Column('severity', postgresql.ENUM('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', name='patch_severity'), nullable=False),
        sa.Column('status', postgresql.ENUM('pending', 'applied', 'failed', name='patch_status'), nullable=False),
        sa.Column('server_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('applied_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['server_id'], ['servers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create audit_logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('details', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('audit_logs')
    op.drop_table('patches')
    op.drop_table('servers')
    op.drop_table('users')
    op.execute('DROP TYPE user_role')
    op.execute('DROP TYPE server_status')
    op.execute('DROP TYPE patch_status')
    op.execute('DROP TYPE patch_severity') 