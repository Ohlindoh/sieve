from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Topic(Base):
    __tablename__ = "topics"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    keywords: Mapped[str] = mapped_column(String(500))  # Comma-separated keywords
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

class NewsItem(Base):
    __tablename__ = "news_items"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(500))
    url: Mapped[str] = mapped_column(String(1000))
    source: Mapped[str] = mapped_column(String(50))  # e.g., "hackernews"
    points: Mapped[Optional[int]] = mapped_column(default=0)
    num_comments: Mapped[Optional[int]] = mapped_column(default=0)
    external_id: Mapped[str] = mapped_column(String(100))  # ID from source
    collected_at: Mapped[datetime] = mapped_column(default=datetime.utcnow) 