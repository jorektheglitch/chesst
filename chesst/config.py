from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import json

from typing import Mapping


@dataclass
class Config:

    app: ApplicationConfig
    db: DatabaseConfig

    @classmethod
    def load(cls, fd, loader=json.load, *args, **kwargs):
        parsed = loader(fd, *args, **kwargs)
        config = cls._from_mapping(parsed)
        return config

    @classmethod
    def _from_mapping(cls, mapping: Mapping[str, dict]) -> Config:
        try:
            app = ApplicationConfig(**mapping["app"])
            db = DatabaseConfig(**mapping["database"])
        except KeyError:
            raise ValueError("Missing 'app' or 'database' block in config")
        return cls(app=app, db=db)


@dataclass
class ApplicationConfig:
    host: str = "localhost"
    port: int = 80
    app_directory: Path = Path.cwd()


@dataclass
class DatabaseConfig:
    dbms: str = "postgresql"
    driver: str = "asyncpg"
    user: str = "chesst"
    password: str = "chesst"
    host: str = "127.0.0.1"
    port: int = 5432
    db_name: str = "chesst"
    options: dict = field(default_factory=dict)
