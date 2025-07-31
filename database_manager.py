import pandas as pd
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, List, Optional
import time
from config import Config

class DatabaseManager:
    """Manage database connections and operations"""
    
    def __init__(self):
        self.config = Config()
        self.engine = None
        self.logger = logging.getLogger(__name__)
        self._connect()
    
    def _connect(self):
        """Create database connection"""
        try:
            self.engine = create_engine(
                self.config.database_url,
                echo=False,
                pool_pre_ping=True,
                pool_recycle=3600
            )
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            self.logger.info("Database connection established")
            
        except Exception as e:
            self.logger.error(f"Failed to connect to database: {e}")
            raise
    
    def execute_schema(self, schema_file: str = "database_schema.sql"):
        """Execute database schema from SQL file"""
        try:
            with open(schema_file, 'r') as file:
                schema_sql = file.read()
            
            # Split by semicolon and execute each statement
            statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
            
            with self.engine.connect() as conn:
                for statement in statements:
                    if statement:
                        conn.execute(text(statement))
                        conn.commit()
            
            self.logger.info("Database schema executed successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to execute schema: {e}")
            raise
    
    def insert_dataframe(self, df: pd.DataFrame, table_name: str, 
                        if_exists: str = 'append') -> bool:
        """Insert pandas DataFrame to database table"""
        try:
            if df.empty:
                self.logger.warning(f"Empty DataFrame for table {table_name}")
                return False
            
            start_time = time.time()
            
            # Insert data
            rows_affected = df.to_sql(
                name=table_name,
                con=self.engine,
                if_exists=if_exists,
                index=False,
                method='multi',
                chunksize=1000
            )
            
            execution_time = time.time() - start_time
            
            self.logger.info(f"Inserted {len(df)} rows into {table_name} in {execution_time:.2f}s")
            
            # Log ETL operation
            self._log_etl_operation(
                operation_type=f"INSERT_{table_name.upper()}",
                status="SUCCESS",
                records_processed=len(df),
                execution_time=execution_time
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to insert data into {table_name}: {e}")
            self._log_etl_operation(
                operation_type=f"INSERT_{table_name.upper()}",
                status="ERROR",
                records_processed=0,
                execution_time=0,
                error_message=str(e)
            )
            return False
    
    def upsert_meals(self, df: pd.DataFrame) -> bool:
        """Upsert meals data (update if exists, insert if new)"""
        try:
            if df.empty:
                return False
            
            # First, try to insert new records
            existing_ids = self.get_existing_meal_ids()
            new_meals = df[~df['id'].isin(existing_ids)]
            
            if not new_meals.empty:
                self.insert_dataframe(new_meals, 'meals', 'append')
            
            # Update existing records
            existing_meals = df[df['id'].isin(existing_ids)]
            if not existing_meals.empty:
                self._update_existing_meals(existing_meals)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to upsert meals: {e}")
            return False
    
    def get_existing_meal_ids(self) -> List[str]:
        """Get list of existing meal IDs"""
        try:
            query = "SELECT id FROM meals"
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                return [row[0] for row in result.fetchall()]
        except Exception as e:
            self.logger.error(f"Failed to get existing meal IDs: {e}")
            return []
    
    def _update_existing_meals(self, df: pd.DataFrame):
        """Update existing meal records"""
        try:
            with self.engine.connect() as conn:
                for _, row in df.iterrows():
                    update_query = text("""
                        UPDATE meals SET 
                            meal_name = :meal_name,
                            category = :category,
                            area = :area,
                            instructions = :instructions,
                            meal_thumb = :meal_thumb,
                            tags = :tags,
                            youtube = :youtube,
                            source = :source,
                            image_source = :image_source,
                            creative_commons_confirmed = :creative_commons_confirmed,
                            date_modified = :date_modified,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = :id
                    """)
                    
                    conn.execute(update_query, row.to_dict())
                    conn.commit()
            
            self.logger.info(f"Updated {len(df)} existing meal records")
            
        except Exception as e:
            self.logger.error(f"Failed to update existing meals: {e}")
            raise
    
    def delete_meal_ingredients(self, meal_ids: List[str]):
        """Delete existing ingredients for meals"""
        try:
            if not meal_ids:
                return
            
            placeholders = ','.join([':id' + str(i) for i in range(len(meal_ids))])
            query = f"DELETE FROM ingredients WHERE meal_id IN ({placeholders})"
            
            params = {f'id{i}': meal_id for i, meal_id in enumerate(meal_ids)}
            
            with self.engine.connect() as conn:
                result = conn.execute(text(query), params)
                conn.commit()
                
            self.logger.info(f"Deleted ingredients for {len(meal_ids)} meals")
            
        except Exception as e:
            self.logger.error(f"Failed to delete meal ingredients: {e}")
    
    def get_table_count(self, table_name: str) -> int:
        """Get count of records in table"""
        try:
            query = f"SELECT COUNT(*) FROM {table_name}"
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                return result.scalar()
        except Exception as e:
            self.logger.error(f"Failed to get count for {table_name}: {e}")
            return 0
    
    def _log_etl_operation(self, operation_type: str, status: str, 
                          records_processed: int, execution_time: float = 0,
                          error_message: str = None):
        """Log ETL operation to database"""
        try:
            log_data = pd.DataFrame([{
                'operation_type': operation_type,
                'status': status,
                'records_processed': records_processed,
                'execution_time': execution_time,
                'error_message': error_message
            }])
            
            log_data.to_sql('etl_logs', self.engine, if_exists='append', index=False)
            
        except Exception as e:
            self.logger.error(f"Failed to log ETL operation: {e}")
    
    def get_recent_etl_logs(self, limit: int = 10) -> pd.DataFrame:
        """Get recent ETL logs"""
        try:
            query = f"""
                SELECT * FROM etl_logs 
                ORDER BY created_at DESC 
                LIMIT {limit}
            """
            return pd.read_sql(query, self.engine)
        except Exception as e:
            self.logger.error(f"Failed to get ETL logs: {e}")
            return pd.DataFrame()
    
    def close(self):
        """Close database connection"""
        if self.engine:
            self.engine.dispose()
            self.logger.info("Database connection closed")
