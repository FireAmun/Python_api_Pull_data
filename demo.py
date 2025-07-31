# Example usage script for MealDB ETL
from etl_pipeline import MealETL
import time

def demo_etl_pipeline():
    """Demonstrate the ETL pipeline functionality"""
    
    print("🍽️ MealDB ETL Pipeline Demo")
    print("=" * 50)
    
    # Initialize ETL
    etl = MealETL()
    
    try:
        # 1. Set up database schema
        print("\n1. Setting up database schema...")
        etl.db_manager.execute_schema()
        print("   ✓ Database schema created")
        
        # 2. Run initial ETL with categories and areas
        print("\n2. Loading reference data (categories and areas)...")
        categories = etl.extract_categories()
        areas = etl.extract_areas()
        
        categories_df = etl.transformer.transform_categories_to_dataframe(categories)
        areas_df = etl.transformer.transform_areas_to_dataframe(areas)
        
        etl.db_manager.insert_dataframe(categories_df, 'categories', 'replace')
        etl.db_manager.insert_dataframe(areas_df, 'areas', 'replace')
        print(f"   ✓ Loaded {len(categories_df)} categories and {len(areas_df)} areas")
        
        # 3. Load some random meals
        print("\n3. Loading random meals...")
        etl.run_incremental_etl(meal_count=10)
        print("   ✓ Loaded 10 random meals")
        
        # 4. Search for specific cuisine
        print("\n4. Loading Italian cuisine meals...")
        etl.search_and_load_meals('Italian', 'area')
        print("   ✓ Loaded Italian meals")
        
        # 5. Search for chicken recipes
        print("\n5. Loading chicken recipes...")
        etl.search_and_load_meals('chicken', 'ingredient')
        print("   ✓ Loaded chicken recipes")
        
        # 6. Show final statistics
        print("\n6. Final Database Statistics:")
        print("-" * 30)
        meals_count = etl.db_manager.get_table_count('meals')
        ingredients_count = etl.db_manager.get_table_count('ingredients')
        categories_count = etl.db_manager.get_table_count('categories')
        areas_count = etl.db_manager.get_table_count('areas')
        
        print(f"   Meals: {meals_count}")
        print(f"   Ingredients: {ingredients_count}")
        print(f"   Categories: {categories_count}")
        print(f"   Areas: {areas_count}")
        
        print("\n🎉 Demo completed successfully!")
        print("\nNext steps:")
        print("- Run 'python cli.py dashboard' to launch the web dashboard")
        print("- Use 'python cli.py etl full --count 50' to load more meals")
        print("- Explore the database with your favorite MySQL client")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        
    finally:
        etl.cleanup()

if __name__ == "__main__":
    demo_etl_pipeline()
