import datetime

from sqlalchemy import text, String, ForeignKey, JSON, Integer
from sqlalchemy.dialects.postgresql import ARRAY, JSONB

from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import Annotated
from sqlalchemy.ext.mutable import MutableList

intpk = Annotated[int, mapped_column(primary_key=True, unique=True)]
username = Annotated[str, mapped_column(String(20), nullable=False, unique=True)]
article_theme = Annotated[str, mapped_column(String(20), nullable=False)]
article_text = Annotated[str, mapped_column(String(4096), nullable=False)]
created_at = Annotated[
    datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
]
updated_at = Annotated[
    datetime.datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.utcnow
    ),
]


class User(Base):
    __tablename__ = "users"
    id: Mapped[intpk]
    username: Mapped[username]
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hash_password: Mapped[str] = mapped_column(nullable=False)


class Article(Base):
    __tablename__ = "articles"
    id: Mapped[intpk]
    article_theme: Mapped[article_theme]
    article_text: Mapped[article_text]
    likes_count: Mapped[int] = mapped_column(nullable=True)
    likes_id_users: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    article_author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    article_author: Mapped[str] = mapped_column(ForeignKey("users.username"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
