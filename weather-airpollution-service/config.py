from dataclasses import dataclass, field
from typing import Callable


@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: str = "5432"
    name: str = "ALLERMIND"
    user: str = "postgres"
    password: str = "123456"
    schema: str = "WEATHER"


@dataclass
class ApplicationConfig:
    # Using default_factory to create a new instance of DatabaseConfig each time
    db_config: DatabaseConfig = field(default_factory=DatabaseConfig)
    create_tables_if_not_exists: bool = True


config = ApplicationConfig()
