"""Add recipe models

Revision ID: 001_add_recipe_models
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_add_recipe_models'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create recipes table
    op.create_table(
        'recipes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('ingredients', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('instructions', sa.Text(), nullable=False),
        sa.Column('prep_time', sa.Integer(), nullable=True),
        sa.Column('cook_time', sa.Integer(), nullable=True),
        sa.Column('servings', sa.Integer(), nullable=True),
        sa.Column('source_url', sa.String(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_recipes_id'), 'recipes', ['id'], unique=False)
    op.create_index(op.f('ix_recipes_title'), 'recipes', ['title'], unique=False)
    op.create_index(op.f('ix_recipes_user_id'), 'recipes', ['user_id'], unique=False)
    
    # Create recipe_ingredients table
    op.create_table(
        'recipe_ingredients',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('recipe_id', sa.Integer(), nullable=False),
        sa.Column('ingredient_name', sa.String(), nullable=False),
        sa.Column('quantity', sa.String(), nullable=True),
        sa.Column('unit', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_recipe_ingredients_id'), 'recipe_ingredients', ['id'], unique=False)
    op.create_index(op.f('ix_recipe_ingredients_recipe_id'), 'recipe_ingredients', ['recipe_id'], unique=False)
    op.create_index(op.f('ix_recipe_ingredients_ingredient_name'), 'recipe_ingredients', ['ingredient_name'], unique=False)


def downgrade() -> None:
    # Drop indexes
    op.drop_index(op.f('ix_recipe_ingredients_ingredient_name'), table_name='recipe_ingredients')
    op.drop_index(op.f('ix_recipe_ingredients_recipe_id'), table_name='recipe_ingredients')
    op.drop_index(op.f('ix_recipe_ingredients_id'), table_name='recipe_ingredients')
    op.drop_index(op.f('ix_recipes_user_id'), table_name='recipes')
    op.drop_index(op.f('ix_recipes_title'), table_name='recipes')
    op.drop_index(op.f('ix_recipes_id'), table_name='recipes')
    
    # Drop tables
    op.drop_table('recipe_ingredients')
    op.drop_table('recipes')

