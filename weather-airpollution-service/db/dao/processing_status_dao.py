from datetime import date

from db.db_connection import DatabaseConnectionManager
from domain.entities import ProcessingStatus
from config import config


class ProcessingStatusDAO:
    def __init__(self):
        self.db_manager = DatabaseConnectionManager()
        self.schema = config.db_config.schema

    def get_status_for_date(self, target_date: date) -> ProcessingStatus:
        """Get the processing status for a specific date.
        
        Returns:
            ProcessingStatus object if found, None otherwise.
        """
        with self.db_manager.get_cursor() as cursor:
            query = f'SELECT date, isprocessed FROM "{self.schema}"."processing_status" WHERE date = %s'
            cursor.execute(query, (target_date,))
            row = cursor.fetchone()
            
            if row:
                return ProcessingStatus(date=row[0], isprocessed=row[1])
            return None
    
    def create_or_update_status(self, status: ProcessingStatus) -> None:
        """Create or update the processing status for a date."""
        with self.db_manager.get_cursor() as cursor:
            query = f"""
                INSERT INTO "{self.schema}"."processing_status" (date, isprocessed)
                VALUES (%s, %s)
                ON CONFLICT (date) DO UPDATE SET isprocessed = %s
            """
            cursor.execute(query, (status.date, status.isprocessed, status.isprocessed))
