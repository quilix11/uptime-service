from datetime import datetime
from typing import List, Optional
from urllib.parse import urlparse

from sqlalchemy import UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, validates
from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import String


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255))

    websites: Mapped[List["Website"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Website(Base):
    __tablename__ = "website"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    url: Mapped[str]
    interval: Mapped[int]
    is_active: Mapped[bool] = mapped_column(default=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    user: Mapped["Users"] = relationship(back_populates="websites")

    logs: Mapped[List["Logs"]] = relationship(back_populates="website", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("url", "user_id", name="uq_url"),
    )

    @validates("url")
    def validate_url(self, key: str, url: str) -> str:
        if not url:
            raise ValueError("url cannot be empty")
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"incorrect url format: {url}")
        return url


class Logs(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    website_id: Mapped[int] = mapped_column(ForeignKey("website.id"))
    
    status_code: Mapped[Optional[int]] = mapped_column(nullable=True)
    response_time: Mapped[int]
    is_online: Mapped[bool]
    checked_at: Mapped[datetime] = mapped_column(server_default=func.now())

    website: Mapped["Website"] = relationship(back_populates="logs")
