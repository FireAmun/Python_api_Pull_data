#!/usr/bin/env python3
"""
Enhanced ETL Demo - Shows what's new each run
Tracks and displays new additions to your database
"""

import sqlite3
import requests
import json
from datetime import datetime
import os

class EnhancedETL:
    def __init__(self, db_path="mealdb_enhanced.db"):
        self.db_path = db_path
        self.setup_database()
        
    def setup_database(self):
        """Create SQLite database and tables"""
        print("Setting up SQLite database...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create meals table with run tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS meals (
                id TEXT PRIMARY KEY,
                meal_name TEXT NOT NULL,
                category TEXT,
                area TEXT,
                instructions TEXT,
                meal_thumb TEXT,
                tags TEXT,
                youtube TEXT,
                run_number INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create ingredients table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                meal_id TEXT,
                ingredient_name TEXT,
                measurement TEXT,
                ingredient_order INTEGER,
                FOREIGN KEY (meal_id) REFERENCES meals(id)
            )
        ''')
        
        # Create run log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS run_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_number INTEGER,
                meals_added INTEGER,
                ingredients_added INTEGER,
                run_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✓ Database setup complete")
        
    def get_next_run_number(self):
        """Get the next run number"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT MAX(run_number) FROM run_log')
        result = cursor.fetchone()[0]
        
        conn.close()
        return (result or 0) + 1
        
    def get_existing_meal_ids(self):
        """Get list of existing meal IDs"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM meals')
        existing_ids = {row[0] for row in cursor.fetchall()}
        
        conn.close()
        return existing_ids
        
    def get_random_meals(self, count=15):
        """Get random meals from API"""
        print(f"Fetching {count} random meals from TheMealDB API...")
        meals = []
        existing_ids = self.get_existing_meal_ids()
        
        attempts = 0
        max_attempts = count * 3  # Try 3x more to find unique meals
        
        while len(meals) < count and attempts < max_attempts:
            attempts += 1
            try:
                response = requests.get("https://www.themealdb.com/api/json/v1/1/random.php", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    
                    if data and 'meals' in data and data['meals']:
                        meal = data['meals'][0]
                        meal_id = meal.get('idMeal')
                        
                        # Only add if we don't already have this meal
                        if meal_id not in existing_ids:
                            meals.append(meal)
                            existing_ids.add(meal_id)  # Prevent duplicates in this run
                            status = "NEW" 
                        else:
                            status = "DUPLICATE (skipped)"
                            
                        print(f"  {len(meals):2d}. {meal.get('strMeal', 'Unknown')[:45]:45} | {status}")
                        
            except Exception as e:
                print(f"  Error fetching meal: {e}")
                
        if len(meals) < count:
            print(f"⚠️  Only found {len(meals)} new meals (tried {attempts} attempts)")
        else:
            print(f"✓ Successfully fetched {len(meals)} NEW meals")
            
        return meals
    
    def extract_ingredients(self, meal):
        """Extract ingredients from meal data"""
        ingredients = []
        
        for i in range(1, 21):
            ingredient = meal.get(f'strIngredient{i}', '').strip()
            measure = meal.get(f'strMeasure{i}', '').strip()
            
            if ingredient and ingredient.lower() not in ['', 'null', 'none']:
                ingredients.append({
                    'ingredient_name': ingredient,
                    'measurement': measure if measure else None,
                    'ingredient_order': i
                })
        
        return ingredients
    
    def save_meals(self, meals, run_number):
        """Save meals to SQLite database"""
        if not meals:
            print("No new meals to save.")
            return 0, 0
            
        print(f"Saving {len(meals)} NEW meals to database...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        meals_saved = 0
        ingredients_saved = 0
        
        for meal in meals:
            try:
                # Insert meal
                cursor.execute('''
                    INSERT INTO meals 
                    (id, meal_name, category, area, instructions, meal_thumb, tags, youtube, run_number)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    meal.get('idMeal'),
                    meal.get('strMeal'),
                    meal.get('strCategory'),
                    meal.get('strArea'),
                    meal.get('strInstructions'),
                    meal.get('strMealThumb'),
                    meal.get('strTags'),
                    meal.get('strYoutube'),
                    run_number
                ))
                
                # Insert ingredients
                ingredients = self.extract_ingredients(meal)
                
                for ingredient in ingredients:
                    cursor.execute('''
                        INSERT INTO ingredients (meal_id, ingredient_name, measurement, ingredient_order)
                        VALUES (?, ?, ?, ?)
                    ''', (
                        meal.get('idMeal'),
                        ingredient['ingredient_name'],
                        ingredient['measurement'],
                        ingredient['ingredient_order']
                    ))
                    ingredients_saved += 1
                
                meals_saved += 1
                
            except Exception as e:
                print(f"  Error saving meal {meal.get('strMeal', 'Unknown')}: {e}")
        
        # Log this run
        cursor.execute('''
            INSERT INTO run_log (run_number, meals_added, ingredients_added)
            VALUES (?, ?, ?)
        ''', (run_number, meals_saved, ingredients_saved))
        
        conn.commit()
        conn.close()
        
        print(f"✓ Saved {meals_saved} NEW meals and {ingredients_saved} NEW ingredients")
        return meals_saved, ingredients_saved
    
    def get_stats(self):
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM meals')
        meals_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM ingredients')
        ingredients_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT category) FROM meals WHERE category IS NOT NULL')
        categories_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT area) FROM meals WHERE area IS NOT NULL')
        areas_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'meals': meals_count,
            'ingredients': ingredients_count,
            'categories': categories_count,
            'areas': areas_count
        }
    
    def show_run_history(self):
        """Show history of all runs"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT run_number, meals_added, ingredients_added, run_date
            FROM run_log
            ORDER BY run_number
        ''')
        
        runs = cursor.fetchall()
        
        if runs:
            print(f"\n📈 RUN HISTORY")
            print("-" * 60)
            print("Run | Meals Added | Ingredients | Date")
            print("-" * 60)
            
            total_meals = 0
            total_ingredients = 0
            
            for run_num, meals, ingredients, date in runs:
                total_meals += meals
                total_ingredients += ingredients
                date_str = date[:16] if date else "Unknown"  # Just date and time
                print(f" {run_num:2d} |    {meals:3d}      |    {ingredients:4d}     | {date_str}")
            
            print("-" * 60)
            print(f"TOTAL: {total_meals} meals, {total_ingredients} ingredients")
        
        conn.close()
    
    def show_latest_additions(self, run_number):
        """Show what was added in the latest run"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT meal_name, category, area 
            FROM meals 
            WHERE run_number = ?
            ORDER BY meal_name
        ''', (run_number,))
        
        new_meals = cursor.fetchall()
        
        if new_meals:
            print(f"\n🆕 NEW MEALS ADDED IN RUN #{run_number}")
            print("-" * 60)
            for i, (name, category, area) in enumerate(new_meals, 1):
                print(f"{i:2d}. {name[:35]:35} | {category or 'N/A':10} | {area or 'N/A'}")
        
        conn.close()
    
    def run_demo(self, meal_count=15):
        """Run enhanced demo with tracking"""
        run_number = self.get_next_run_number()
        
        print("🍽️ ENHANCED MEALDB ETL DEMO")
        print("=" * 50)
        print(f"🔄 Run #{run_number}")
        print("Tracks new additions and avoids duplicates!")
        print()
        
        # Show current stats
        current_stats = self.get_stats()
        print(f"📊 Current Database: {current_stats['meals']} meals, {current_stats['ingredients']} ingredients")
        print()
        
        try:
            # Test API
            print("Testing API connectivity...")
            response = requests.get("https://www.themealdb.com/api/json/v1/1/random.php", timeout=10)
            if response.status_code == 200:
                print("✓ TheMealDB API is accessible")
                print()
            else:
                print("❌ API test failed")
                return
            
            # Fetch NEW meals
            meals = self.get_random_meals(meal_count)
            
            if meals:
                # Save to database
                meals_added, ingredients_added = self.save_meals(meals, run_number)
                
                # Show updated stats
                new_stats = self.get_stats()
                print(f"\n📊 UPDATED DATABASE STATISTICS")
                print("=" * 50)
                print(f"Total Meals:      {new_stats['meals']:,} (+{meals_added})")
                print(f"Total Ingredients: {new_stats['ingredients']:,} (+{ingredients_added})")
                print(f"Categories:       {new_stats['categories']:,}")
                print(f"Areas/Cuisines:   {new_stats['areas']:,}")
                print("=" * 50)
                
                # Show what was added
                if meals_added > 0:
                    self.show_latest_additions(run_number)
                
                # Show run history
                self.show_run_history()
                
                print(f"\n🎉 Run #{run_number} completed successfully!")
                print(f"Database file: {os.path.abspath(self.db_path)}")
                print(f"File size: {os.path.getsize(self.db_path):,} bytes")
                
                print(f"\n🔄 Run again to add more unique recipes!")
                
            else:
                print("❌ No NEW meals were found. Try again later!")
                
        except Exception as e:
            print(f"❌ Demo failed: {e}")

def main():
    """Main function"""
    etl = EnhancedETL()
    etl.run_demo(meal_count=12)

if __name__ == "__main__":
    main()
