#!/usr/bin/env python3
"""
Quick Start ETL Demo - Works without MySQL setup
Uses SQLite database for easy setup
"""

import sqlite3
import requests
import json
import pandas as pd
from datetime import datetime
import os

class QuickETL:
    def __init__(self, db_path="mealdb_quick.db"):
        self.db_path = db_path
        self.setup_database()
        
    def setup_database(self):
        """Create SQLite database and tables"""
        print("Setting up SQLite database...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
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
        print(f"Fetching {count} random meals...")
        meals = []
        
        for i in range(count):
            try:
                response = requests.get("https://www.themealdb.com/api/json/v1/1/random.php", timeout=10)
                response.raise_for_status()
                data = response.json()
                
                if data and 'meals' in data and data['meals']:
                    meal = data['meals'][0]
                    meals.append(meal)
                    print(f"  {i+1}. {meal.get('strMeal', 'Unknown')}")
                    
            except Exception as e:
                print(f"  Error fetching meal {i+1}: {e}")
                
        print(f"✓ Successfully fetched {len(meals)} meals")
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
    
    def save_meals(self, meals):
        """Save meals to SQLite database"""
        print("Saving meals to database...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        meals_saved = 0
        ingredients_saved = 0
        
        for meal in meals:
            try:
                # Insert meal
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
                
                # Insert ingredients
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
    
    def show_stats(self):
        """Show database statistics"""
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
        
        print("\n" + "="*50)
        print("DATABASE STATISTICS")
        print("="*50)
        print(f"Total Meals: {meals_count}")
        print(f"Total Ingredients: {ingredients_count}")
        print(f"Categories: {categories_count}")
        print(f"Areas/Cuisines: {areas_count}")
        print("="*50)
    
    def show_sample_recipes(self, limit=5):
        """Show sample recipes from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, meal_name, category, area 
            FROM meals 
            LIMIT ?
        ''', (limit,))
        
        recipes = cursor.fetchall()
        
        print(f"\n📋 SAMPLE RECIPES (showing {len(recipes)} of {limit})")
        print("-" * 60)
        
        for recipe in recipes:
            meal_id, name, category, area = recipe
            print(f"🍽️  {name}")
            print(f"    Category: {category}")
            print(f"    Cuisine: {area}")
            
            # Get ingredients
            cursor.execute('''
                SELECT ingredient_name, measurement 
                FROM ingredients 
                WHERE meal_id = ? 
                ORDER BY ingredient_order 
                LIMIT 5
            ''', (meal_id,))
            
            ingredients = cursor.fetchall()
            print("    Ingredients:", end="")
            for i, (ingredient, measure) in enumerate(ingredients):
                if i == 0:
                    print(f" {measure or ''} {ingredient}", end="")
                else:
                    print(f", {measure or ''} {ingredient}", end="")
            if len(ingredients) >= 5:
                print("...")
            else:
                print()
            print()
        
        conn.close()
    
    def run_demo(self, meal_count=10):
        """Run complete demo"""
        print("🍽️ MealDB Quick ETL Demo")
        print("=" * 50)
        print("This demo works without MySQL setup!")
        print()
        
        try:
            # Fetch meals
            meals = self.get_random_meals(meal_count)
            
            if meals:
                # Save to database
                self.save_meals(meals)
                
                # Show results
                self.show_stats()
                self.show_sample_recipes()
                
                print(f"\n🎉 Demo completed successfully!")
                print(f"Database file: {os.path.abspath(self.db_path)}")
                print("\nYou can view the database with:")
                print("- SQLite Browser")
                print("- DB Browser for SQLite")
                print("- Or any SQLite client")
                
            else:
                print("❌ No meals were fetched. Check your internet connection.")
                
        except Exception as e:
            print(f"❌ Demo failed: {e}")

def main():
    # Test API connectivity first
    print("Testing API connectivity...")
    try:
        response = requests.get("https://www.themealdb.com/api/json/v1/1/random.php", timeout=10)
        response.raise_for_status()
        print("✓ API is accessible")
        print()
    except Exception as e:
        print(f"❌ API test failed: {e}")
        print("Please check your internet connection.")
        return
    
    # Run the demo
    etl = QuickETL()
    etl.run_demo(meal_count=15)

if __name__ == "__main__":
    main()
