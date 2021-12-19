from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d5de2b8cabf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('question_details',
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('user_id', sa.String(length=255), unique=False, nullable=False),
    sa.Column('user_name', sa.String(length=255), unique=False, nullable=False),
    sa.Column('question_title', sa.String(length=1000), unique=False, nullable=False),
    sa.Column('question_body', sa.String(length=1000), nullable=False),
    sa.Column('tags', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('question_answers',
    sa.Column('answer_id', sa.String(length=60), nullable=False),
    sa.Column('question_id', sa.String(length=255), unique=False, nullable=False),  
    sa.Column('user_id', sa.String(length=255), unique=False, nullable=False),
    sa.Column('user_name', sa.String(length=255), unique=False, nullable=False),
    sa.Column('question_body', sa.String(length=1000), nullable=False),
    sa.Column('answer', sa.String(length=1000), nullable=False),
    sa.Column('upvote', sa.Integer, nullable=True),
    sa.Column('downvote', sa.Integer, nullable=True),
    sa.PrimaryKeyConstraint('answer_id')
    )

    op.create_table('users',
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('public_id', sa.String(length=60)),  
    sa.Column('user_name', sa.String(length=255), unique=False, nullable=False),
    sa.Column('password', sa.String(length=255), unique=False, nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('question_details')
    op.drop_table('question_answers')
    op.drop_table('users')

