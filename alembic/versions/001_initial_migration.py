"""Initial migration - create libraries, books, and library_books tables

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create libraries table
    op.create_table('libraries',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('dept', sa.String(length=100), nullable=True),
        sa.Column('count', sa.Integer(), nullable=False, default=0),
        sa.Column('status', sa.Enum('Active', 'Inactive', name='library_status'), nullable=False, default='Active'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for libraries table
    op.create_index('ix_libraries_id', 'libraries', ['id'])
    op.create_index('ix_libraries_name', 'libraries', ['name'])
    op.create_index('ix_libraries_dept', 'libraries', ['dept'])
    op.create_index('ix_libraries_status', 'libraries', ['status'])

    # Create books table
    op.create_table('books',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('author', sa.String(length=255), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('isbn', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('isbn')
    )
    
    # Create indexes for books table
    op.create_index('ix_books_id', 'books', ['id'])
    op.create_index('ix_books_title', 'books', ['title'])
    op.create_index('ix_books_author', 'books', ['author'])
    op.create_index('ix_books_category', 'books', ['category'])
    op.create_index('ix_books_isbn', 'books', ['isbn'])

    # Create library_books table
    op.create_table('library_books',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('lib_id', sa.Integer(), nullable=False),
        sa.Column('book_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.Enum('Active', 'Inactive', name='mapping_status'), nullable=False, default='Active'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['book_id'], ['books.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['lib_id'], ['libraries.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('lib_id', 'book_id', name='unique_library_book')
    )
    
    # Create indexes for library_books table
    op.create_index('ix_library_books_id', 'library_books', ['id'])
    op.create_index('ix_library_books_lib_id', 'library_books', ['lib_id'])
    op.create_index('ix_library_books_book_id', 'library_books', ['book_id'])
    op.create_index('ix_library_books_status', 'library_books', ['status'])


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('library_books')
    op.drop_table('books')
    op.drop_table('libraries')
    
    # Drop custom ENUM types
    op.execute("DROP TYPE IF EXISTS library_status")
    op.execute("DROP TYPE IF EXISTS mapping_status")
