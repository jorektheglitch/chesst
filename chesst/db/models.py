import functools
from datetime import datetime as dt, timezone as tz
from secrets import token_urlsafe

from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base


TOKEN_LENGTH = 32

metadata = MetaData()
Model = declarative_base()

SHA3_256_hexdigest = String(64)  # 256bit -> 32 bytes -> 64 hexdigits
access_token = String(TOKEN_LENGTH)
utcnow = functools.partial(dt.now, tz.utc)
create_token = functools.partial(token_urlsafe, TOKEN_LENGTH)


class User(Model):

    __tablename__ = "users"

    name = Column(Text, primary_key=True)
    joined_at = Column(DateTime, nullable=False, default=utcnow)
    admin_for = Column(DateTime, nullable=True)
    password_hash = Column(SHA3_256_hexdigest, nullable=False)

    @property
    def is_admin(self) -> bool:
        if self.admin_for is None:
            return False
        return dt.now() < self.admin_for


class AccessToken(Model):

    __tablename__ = "access_tokens"

    token = Column(access_token, primary_key=True, default=create_token)
    user = Column(Text, ForeignKey(User.name), nullable=False)
    created = Column(DateTime, nullable=False, default=utcnow)


class League(Model):

    __tablename__ = "leagues"

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(Text, nullable=False)


class Division(Model):

    __tablename__ = "divisions"

    id = Column(Integer, autoincrement=True, primary_key=True)
    league = Column(Integer, ForeignKey(League.id))


class Tournament(Model):

    __tablename__ = "tournaments"

    id = Column(Integer, autoincrement=True, primary_key=True)
    league = Column(Integer, ForeignKey(League.id), nullable=False)
    started_at = Column(DateTime, nullable=False)


class Game(Model):

    __tablename__ = "games"

    id = Column(Integer, autoincrement=True, primary_key=True)
    blacks = Column(Text, ForeignKey(User.name), nullable=False)
    whites = Column(Text, ForeignKey(User.name), nullable=False)
    winner = Column(Text, ForeignKey(User.name), nullable=True)
    complete = Column(Boolean, server_default=False)
