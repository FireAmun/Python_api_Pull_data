#!/usr/bin/env python3
"""
Super Simple ETL Demo - No external dependencies except requests
Works immediately without MySQL or complex setup
"""

import sqlite3
import requests
import json
from datetime import datetime
import os

class SimpleETL:
    def __init__(self, db_path="mealdb_simple.db"):
        self.db_path = db_path
        self.setup_database()
        
    def setup_database(self):
        """Create SQLite database and tables"""
        print("Setting up SQLite database...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create meals table
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
        
        conn.commit()
        conn.close()
        print("✓ Database setup complete")
        
    def get_random_meals(self, count=10):
        """Get random meals from API"""
        print(f"Fetching {count} random meals from TheMealDB API...")
        meals = []
        
        for i in range(count):
            try:
                response = requests.get("https://www.themealdb.com/api/json/v1/1/random.php", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    
                    if data and 'meals' in data and data['meals']:
                        meal = data['meals'][0]
                        meals.append(meal)
                        print(f"  {i+1:2d}. {meal.get('strMeal', 'Unknown')[:50]}")
                        
            except Exception as e:
                print(f"  Error fetching meal {i+1}: {e}")
                
        print(f"✓ Successfully fetched {len(meals)} meals")
        return meals
    
    def extract_ingredients(self, meal):
        """Extract ingredients from meal data"""
        ingredients = []
        
        for i in range(1, 21):  # API has ingredients 1-20
            ingredient = meal.get(f'strIngredient{i}', '').strip()
            measure = meal.get(f'strMeasure{i}', '').strip()
            
            if ingredient and ingredient.lower() not in ['', 'null', 'none']:
                ingredients.append({
                    'ingredient_name': ingredient,
                    'measurement': measure if measure else None,
                    'ingredient_order': i
                })
        
        return ingredients
    
    def save_meals(self, meals):
        """Save meals to SQLite database"""
        print("Saving meals to database...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        meals_saved = 0
        ingredients_saved = 0
        
        for meal in meals:
            try:
                # Insert meal (replace if exists)
                cursor.execute('''
                    INSERT OR REPLACE INTO meals 
                    (id, meal_name, category, area, instructions, meal_thumb, tags, youtube)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    meal.get('idMeal'),
                    meal.get('strMeal'),
                    meal.get('strCategory'),
                    meal.get('strArea'),
                    meal.get('strInstructions'),
                    meal.get('strMealThumb'),
                    meal.get('strTags'),
                    meal.get('strYoutube')
                ))
                
                # Get and insert ingredients
                ingredients = self.extract_ingredients(meal)
                
                # Delete existing ingredients for this meal
                cursor.execute('DELETE FROM ingredients WHERE meal_id = ?', (meal.get('idMeal'),))
                
                # Insert new ingredients
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
        
        conn.commit()
        conn.close()
        
        print(f"✓ Saved {meals_saved} meals and {ingredients_saved} ingredients")
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
    
    def show_stats(self):
        """Display database statistics"""
        stats = self.get_stats()
        
        print("\n" + "="*50)
        print("📊 DATABASE STATISTICS")
        print("="*50)
        print(f"Total Meals:      {stats['meals']:,}")
        print(f"Total Ingredients: {stats['ingredients']:,}")
        print(f"Categories:       {stats['categories']:,}")
        print(f"Areas/Cuisines:   {stats['areas']:,}")
        print("="*50)
    
    def show_sample_recipes(self, limit=5):
        """Show sample recipes from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, meal_name, category, area 
            FROM meals 
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))
        
        recipes = cursor.fetchall()
        
        print(f"\n🍽️ SAMPLE RECIPES (latest {len(recipes)})")
        print("-" * 70)
        
        for i, (meal_id, name, category, area) in enumerate(recipes, 1):
            print(f"\n{i}. {name}")
            print(f"   Category: {category or 'N/A'}")
            print(f"   Cuisine: {area or 'N/A'}")
            
            # Get ingredients
            cursor.execute('''
                SELECT ingredient_name, measurement 
                FROM ingredients 
                WHERE meal_id = ? 
                ORDER BY ingredient_order 
                LIMIT 6
            ''', (meal_id,))
            
            ingredients = cursor.fetchall()
            if ingredients:
                print("   Ingredients:", end="")
                for j, (ingredient, measure) in enumerate(ingredients):
                    if j == 0:
                        print(f" {measure or ''} {ingredient}".strip(), end="")
                    else:
                        print(f", {measure or ''} {ingredient}".strip(), end="")
                    if j >= 4:  # Show max 5 ingredients
                        print("...")
                        break
                else:
                    print()
        
        conn.close()
    
    def search_by_category(self):
        """Show meals by category"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT category, COUNT(*) as count
            FROM meals 
            WHERE category IS NOT NULL
            GROUP BY category
            ORDER BY count DESC
        ''')
        
        categories = cursor.fetchall()
        
        if categories:
            print(f"\n📂 MEALS BY CATEGORY")
            print("-" * 30)
            for category, count in categories:
                print(f"{category:15} {count:3d} meals")
        
        conn.close()
    
    def search_by_area(self):
        """Show meals by area/cuisine"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT area, COUNT(*) as count
            FROM meals 
            WHERE area IS NOT NULL
            GROUP BY area
            ORDER BY count DESC
        ''')
        
        areas = cursor.fetchall()
        
        if areas:
            print(f"\n🌍 MEALS BY CUISINE")
            print("-" * 30)
            for area, count in areas:
                print(f"{area:15} {count:3d} meals")
        
        conn.close()
    
    def run_demo(self, meal_count=12):
        """Run complete demo"""
        print("🍽️ SIMPLE MEALDB ETL DEMO")
        print("=" * 50)
        print("This demo uses only built-in Python libraries + requests")
        print("No MySQL setup required - uses SQLite!")
        print()
        
        try:
            # Test API first
            print("Testing API connectivity...")
            response = requests.get("https://www.themealdb.com/api/json/v1/1/random.php", timeout=10)
            if response.status_code == 200:
                print("✓ TheMealDB API is accessible")
                print()
            else:
                print("❌ API test failed")
                return
            
            # Fetch meals
            meals = self.get_random_meals(meal_count)
            
            if meals:
                # Save to database
                self.save_meals(meals)
                
                # Show results
                self.show_stats()
                self.show_sample_recipes()
                self.search_by_category()
                self.search_by_area()
                
                print(f"\n🎉 Demo completed successfully!")
                print(f"\nDatabase file created: {os.path.abspath(self.db_path)}")
                print(f"File size: {os.path.getsize(self.db_path):,} bytes")
                
                print("\n📋 What you can do next:")
                print("- View database with SQLite Browser")
                print("- Run this script again to add more meals")
                print("- Modify the code to add more features")
                print("- Set up MySQL later for production use")
                
            else:
                print("❌ No meals were fetched. Check your internet connection.")
                
        except Exception as e:
            print(f"❌ Demo failed: {e}")
            import traceback
            traceback.print_exc()

def main():
    """Main function"""
    etl = SimpleETL()
    etl.run_demo(meal_count=15)

if __name__ == "__main__":
    main()
