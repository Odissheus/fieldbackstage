from alembic import op
import sqlalchemy as sa

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'tenant',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('company_code', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True)),
    )
    op.create_table(
        'user',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('external_id', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True)),
    )
    op.create_table(
        'login_account',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('tenant_id', sa.String(), nullable=True),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True)),
    )
    op.create_table(
        'user_tenant_role',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('product_line_ids', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True)),
    )
    op.create_table(
        'product_line',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('active', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True)),
    )
    op.create_table(
        'insight_raw',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('tenant_id', sa.String(), nullable=True),
        sa.Column('product_line_id', sa.String(), nullable=False),
        sa.Column('territory_id', sa.String(), nullable=True),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('text', sa.Text(), nullable=True),
        sa.Column('audio_url', sa.Text(), nullable=True),
        sa.Column('photo_url', sa.Text(), nullable=True),
        sa.Column('ocr_text', sa.Text(), nullable=True),
        sa.Column('extracted', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True)),
    )
    op.create_table(
        'weekly_report',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('tenant_id', sa.String(), nullable=True),
        sa.Column('product_line_id', sa.String(), nullable=False),
        sa.Column('week_id', sa.String(), nullable=False),
        sa.Column('executive_summary', sa.Text(), nullable=False),
        sa.Column('ci_summary', sa.Text(), nullable=True),
        sa.Column('heatmap', sa.JSON(), nullable=False),
        sa.Column('contributors', sa.JSON(), nullable=False),
        sa.Column('url_pdf', sa.Text(), nullable=True),
        sa.Column('url_html', sa.Text(), nullable=True),
        sa.Column('hash', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True)),
    )


def downgrade() -> None:
    for t in [
        'weekly_report',
        'insight_raw',
        'product_line',
        'user_tenant_role',
        'login_account',
        'user',
        'tenant',
    ]:
        op.drop_table(t)

