import logging
import time
from typing import List, Dict
from api_client import MealDBAPI
from data_transformer import DataTransformer
from database_manager import DatabaseManager
from config import Config

class MealETL:
    """Main ETL pipeline for MealDB data"""
    
    def __init__(self):
        self.config = Config()
        self.api_client = MealDBAPI()
        self.transformer = DataTransformer()
        self.db_manager = DatabaseManager()
        self.logger = self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=getattr(logging, self.config.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('etl.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def extract_random_meals(self, count: int = None) -> List[Dict]:
        """Extract random meals from API"""
        count = count or self.config.BATCH_SIZE
        self.logger.info(f"Extracting {count} random meals")
        
        meals = self.api_client.get_multiple_random_meals(count)
        self.logger.info(f"Extracted {len(meals)} meals")
        
        return meals
    
    def extract_categories(self) -> List[Dict]:
        """Extract categories from API"""
        self.logger.info("Extracting categories")
        
        categories = self.api_client.get_categories()
        self.logger.info(f"Extracted {len(categories)} categories")
        
        return categories
    
    def extract_areas(self) -> List[Dict]:
        """Extract areas from API"""
        self.logger.info("Extracting areas")
        
        areas = self.api_client.get_areas()
        self.logger.info(f"Extracted {len(areas)} areas")
        
        return areas
    
    def run_full_etl(self, meal_count: int = None):
        """Run complete ETL pipeline"""
        start_time = time.time()
        meal_count = meal_count or self.config.BATCH_SIZE
        
        self.logger.info("Starting full ETL pipeline")
        
        try:
            # Extract data
            self.logger.info("=== EXTRACTION PHASE ===")
            meals = self.extract_random_meals(meal_count)
            categories = self.extract_categories()
            areas = self.extract_areas()
            
            # Transform data
            self.logger.info("=== TRANSFORMATION PHASE ===")
            meals_df = self.transformer.transform_meals_to_dataframe(meals)
            ingredients_df = self.transformer.transform_ingredients_to_dataframe(meals)
            categories_df = self.transformer.transform_categories_to_dataframe(categories)
            areas_df = self.transformer.transform_areas_to_dataframe(areas)
            
            self.logger.info(f"Transformed {len(meals_df)} meals, {len(ingredients_df)} ingredients, "
                           f"{len(categories_df)} categories, {len(areas_df)} areas")
            
            # Load data
            self.logger.info("=== LOADING PHASE ===")
            
            # Load reference data first
            if not categories_df.empty:
                self.db_manager.insert_dataframe(categories_df, 'categories', 'replace')
            
            if not areas_df.empty:
                self.db_manager.insert_dataframe(areas_df, 'areas', 'replace')
            
            # Load meals and ingredients
            if not meals_df.empty:
                self.db_manager.upsert_meals(meals_df)
                
                # Delete existing ingredients for these meals and insert new ones
                meal_ids = meals_df['id'].tolist()
                self.db_manager.delete_meal_ingredients(meal_ids)
                
                if not ingredients_df.empty:
                    self.db_manager.insert_dataframe(ingredients_df, 'ingredients', 'append')
            
            execution_time = time.time() - start_time
            self.logger.info(f"ETL pipeline completed successfully in {execution_time:.2f} seconds")
            
            # Print summary
            self._print_summary()
            
        except Exception as e:
            self.logger.error(f"ETL pipeline failed: {e}")
            raise
    
    def run_incremental_etl(self, meal_count: int = 5):
        """Run incremental ETL for new meals only"""
        self.logger.info(f"Starting incremental ETL for {meal_count} meals")
        
        try:
            # Extract only new meals
            meals = self.extract_random_meals(meal_count)
            
            if meals:
                # Transform and load
                meals_df = self.transformer.transform_meals_to_dataframe(meals)
                ingredients_df = self.transformer.transform_ingredients_to_dataframe(meals)
                
                if not meals_df.empty:
                    self.db_manager.upsert_meals(meals_df)
                    
                    meal_ids = meals_df['id'].tolist()
                    self.db_manager.delete_meal_ingredients(meal_ids)
                    
                    if not ingredients_df.empty:
                        self.db_manager.insert_dataframe(ingredients_df, 'ingredients', 'append')
                
                self.logger.info(f"Incremental ETL completed: {len(meals_df)} meals processed")
            else:
                self.logger.info("No new meals to process")
                
        except Exception as e:
            self.logger.error(f"Incremental ETL failed: {e}")
            raise
    
    def search_and_load_meals(self, search_term: str, search_type: str = 'name'):
        """Search for specific meals and load them"""
        self.logger.info(f"Searching meals by {search_type}: {search_term}")
        
        try:
            # Extract based on search type
            if search_type == 'name':
                meals = self.api_client.search_meal_by_name(search_term)
            elif search_type == 'letter':
                meals = self.api_client.search_meal_by_letter(search_term)
            elif search_type == 'category':
                meals = self.api_client.filter_by_category(search_term)
            elif search_type == 'area':
                meals = self.api_client.filter_by_area(search_term)
            elif search_type == 'ingredient':
                meals = self.api_client.filter_by_ingredient(search_term)
            else:
                raise ValueError(f"Invalid search type: {search_type}")
            
            if meals:
                # Get full details for each meal
                detailed_meals = []
                for meal in meals:
                    meal_id = meal.get('idMeal')
                    if meal_id:
                        detailed_meal = self.api_client.lookup_meal_by_id(meal_id)
                        if detailed_meal:
                            detailed_meals.append(detailed_meal)
                
                # Transform and load
                if detailed_meals:
                    meals_df = self.transformer.transform_meals_to_dataframe(detailed_meals)
                    ingredients_df = self.transformer.transform_ingredients_to_dataframe(detailed_meals)
                    
                    if not meals_df.empty:
                        self.db_manager.upsert_meals(meals_df)
                        
                        meal_ids = meals_df['id'].tolist()
                        self.db_manager.delete_meal_ingredients(meal_ids)
                        
                        if not ingredients_df.empty:
                            self.db_manager.insert_dataframe(ingredients_df, 'ingredients', 'append')
                    
                    self.logger.info(f"Loaded {len(detailed_meals)} meals from search")
                else:
                    self.logger.info("No detailed meals found")
            else:
                self.logger.info(f"No meals found for {search_type}: {search_term}")
                
        except Exception as e:
            self.logger.error(f"Search and load failed: {e}")
            raise
    
    def _print_summary(self):
        """Print ETL summary"""
        try:
            meals_count = self.db_manager.get_table_count('meals')
            ingredients_count = self.db_manager.get_table_count('ingredients')
            categories_count = self.db_manager.get_table_count('categories')
            areas_count = self.db_manager.get_table_count('areas')
            
            print("\n" + "="*50)
            print("ETL PIPELINE SUMMARY")
            print("="*50)
            print(f"Total Meals: {meals_count}")
            print(f"Total Ingredients: {ingredients_count}")
            print(f"Total Categories: {categories_count}")
            print(f"Total Areas: {areas_count}")
            print("="*50)
            
        except Exception as e:
            self.logger.error(f"Failed to print summary: {e}")
    
    def cleanup(self):
        """Cleanup resources"""
        self.db_manager.close()


def main():
    """Main execution function"""
    etl = MealETL()
    
    try:
        # Initialize database schema
        print("Setting up database schema...")
        etl.db_manager.execute_schema()
        
        # Run full ETL
        print("Running ETL pipeline...")
        etl.run_full_etl(meal_count=20)
        
        # Example of incremental ETL
        print("\nRunning incremental ETL...")
        etl.run_incremental_etl(meal_count=5)
        
        # Example of search-based ETL
        print("\nSearching for Italian meals...")
        etl.search_and_load_meals('Italian', 'area')
        
    except Exception as e:
        print(f"ETL process failed: {e}")
        
    finally:
        etl.cleanup()


if __name__ == "__main__":
    main()
