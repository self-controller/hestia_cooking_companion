# backend/alembic/versions/002_add_default_recipes.py
"""add default recipes support

Revision ID: 002_add_default_recipes
Revises: 001_add_recipe_models
Create Date: 2024-01-XX XX:XX:XX.XXXXXX
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '002_add_default_recipes'
down_revision = '001_add_recipe_models'
branch_labels = None
depends_on = None

def upgrade():
    # Make user_id nullable to allow default recipes
    op.alter_column('recipes', 'user_id',
                    existing_type=sa.Integer(),
                    nullable=True)

def downgrade():
    # Remove any recipes with NULL user_id before making it non-nullable
    op.execute("DELETE FROM recipes WHERE user_id IS NULL")
    op.alter_column('recipes', 'user_id',
                    existing_type=sa.Integer(),
                    nullable=False)