import datetime

from sqlalchemy import String, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from uuid import UUID


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    uuid: Mapped[UUID] = mapped_column(primary_key=True, server_default=text('gen_random_uuid()'))
    full_name: Mapped[str] = mapped_column(String(length=80))
    email: Mapped[str | None] = mapped_column(String(320), unique=True)  # 320 is standardised max length of email
    password_hash: Mapped[str]
    last_login: Mapped[datetime.datetime] = mapped_column(server_default=text("NOW()"))
