from sqlalchemy import Column, Integer, String, UniqueConstraint, Index, func, Boolean, DateTime
from app.database import Base

class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    __table_args__ = (
        Index('ix_users_email_lower', func.lower(email), unique=True),
    )

class Book(Base, TimestampMixin):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    category = Column(String, index=True)  # fantasy, fic, non-fic
    description = Column(String, nullable=True)

    __table_args__ = (
        UniqueConstraint('title', 'category', 'author', name='_title_category_author_uc'),
        Index('unique_title_lower', func.lower(title), unique=True),
    )