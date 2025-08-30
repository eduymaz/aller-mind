import psycopg2
from psycopg2.extensions import connection
from contextlib import contextmanager
from typing import Optional

from config import config


class DatabaseConnectionManager:
    _instance: Optional['DatabaseConnectionManager'] = None
    _connection: Optional[connection] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnectionManager, cls).__new__(cls)
            cls._instance._connection = None
        return cls._instance

    def get_connection(self) -> connection:
        """Get a connection to the database, creating it if needed."""
        if self._connection is None or self._connection.closed:
            self._connection = psycopg2.connect(
                host=config.db_config.host,
                port=config.db_config.port,
                dbname=config.db_config.name,
                user=config.db_config.user,
                password=config.db_config.password
            )
            # Create schema if it doesn't exist
            with self._connection.cursor() as cursor:
                cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{config.db_config.schema}"')
                self._connection.commit()
        return self._connection

    def close_connection(self) -> None:
        """Close the database connection if it's open."""
        if self._connection and not self._connection.closed:
            self._connection.close()
            self._connection = None

    @contextmanager
    def get_cursor(self):
        """Context manager for database cursor."""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
