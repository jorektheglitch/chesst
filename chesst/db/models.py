"""
Models for application's database.
"""


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
    """
    User model. User identified by string primary key `name`.

    There is a fields for each user:
      `name` str - unique name of the user.
      `joined_at` datetime - date which user was registered.
      `admin_for` datetime - nullable date that user was admin for.
      `password_hash` str - hexdigest of hash of user's password.

    And there is some properties for user:
      `is_admin` bool - True if user is admin.
    """

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
    """
    AccesssToken is a model for user's access tokens.
    Each token identifies one user.
    """

    __tablename__ = "access_tokens"

    token = Column(access_token, primary_key=True, default=create_token)
    user = Column(Text, ForeignKey(User.name), nullable=False)
    created = Column(DateTime, nullable=False, default=utcnow)


class League(Model):
    """
    League is a bunch of users which play tournaments together.
    """

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
