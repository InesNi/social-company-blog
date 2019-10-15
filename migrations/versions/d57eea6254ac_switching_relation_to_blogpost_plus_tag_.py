"""switching relation to blogpost plus tag,untag and tagged methods

Revision ID: d57eea6254ac
Revises: 57d2b2d7c88f
Create Date: 2019-10-15 12:54:49.464184

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd57eea6254ac'
down_revision = '57d2b2d7c88f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_tag',
    sa.Column('blogpost_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['blogpost_id'], ['blogpost.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], )
    )
    op.drop_table('tag_post')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag_post',
    sa.Column('tag_id', sa.INTEGER(), nullable=True),
    sa.Column('blogpost_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['blogpost_id'], ['blogpost.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], )
    )
    op.drop_table('post_tag')
    # ### end Alembic commands ###
