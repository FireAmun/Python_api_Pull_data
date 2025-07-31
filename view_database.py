#!/usr/bin/env python3
"""
Simple SQLite Database Viewer for MealDB
View your recipe data without external tools
"""

import sqlite3
import os

def view_database(db_path="mealdb_simple.db"):
    """View contents of the SQLite database"""
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        print("Run 'python simple_demo.py' first to create the database.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🍽️ MEALDB DATABASE VIEWER")
    print("=" * 50)
    
    # Database stats
    cursor.execute('SELECT COUNT(*) FROM meals')
    meals_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM ingredients')
    ingredients_count = cursor.fetchone()[0]
    
    print(f"📊 Total Meals: {meals_count}")
    print(f"📊 Total Ingredients: {ingredients_count}")
    print()
    
    while True:
        print("Choose an option:")
        print("1. View all meals")
        print("2. View meals by category")
        print("3. View meals by cuisine")
        print("4. Search meals by name")
        print("5. View detailed recipe")
        print("6. View database schema")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-6): ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            view_all_meals(cursor)
        elif choice == "2":
            view_by_category(cursor)
        elif choice == "3":
            view_by_cuisine(cursor)
        elif choice == "4":
            search_meals(cursor)
        elif choice == "5":
            view_detailed_recipe(cursor)
        elif choice == "6":
            view_schema(cursor)
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")
        print()
    
    conn.close()
    print("👋 Thanks for using MealDB Viewer!")

def view_all_meals(cursor):
    """View all meals"""
    print("\n📋 ALL MEALS")
    print("-" * 60)
    
    cursor.execute('''
        SELECT id, meal_name, category, area 
        FROM meals 
        ORDER BY meal_name
    ''')
    
    meals = cursor.fetchall()
    
    for i, (meal_id, name, category, area) in enumerate(meals, 1):
        print(f"{i:2d}. {name[:40]:40} | {category or 'N/A':12} | {area or 'N/A'}")
    
    print(f"\nTotal: {len(meals)} meals")

def view_by_category(cursor):
    """View meals grouped by category"""
    print("\n📂 MEALS BY CATEGORY")
    print("-" * 50)
    
    cursor.execute('''
        SELECT category, COUNT(*) as count
        FROM meals 
        WHERE category IS NOT NULL
        GROUP BY category
        ORDER BY count DESC, category
    ''')
    
    categories = cursor.fetchall()
    
    for category, count in categories:
        print(f"\n🏷️  {category} ({count} meals)")
        
        cursor.execute('''
            SELECT meal_name 
            FROM meals 
            WHERE category = ?
            ORDER BY meal_name
            LIMIT 5
        ''', (category,))
        
        meals = cursor.fetchall()
        for meal_name, in meals:
            print(f"   • {meal_name}")
        
        if count > 5:
            print(f"   ... and {count - 5} more")

def view_by_cuisine(cursor):
    """View meals grouped by cuisine/area"""
    print("\n🌍 MEALS BY CUISINE")
    print("-" * 50)
    
    cursor.execute('''
        SELECT area, COUNT(*) as count
        FROM meals 
        WHERE area IS NOT NULL
        GROUP BY area
        ORDER BY count DESC, area
    ''')
    
    areas = cursor.fetchall()
    
    for area, count in areas:
        print(f"\n🍽️  {area} ({count} meals)")
        
        cursor.execute('''
            SELECT meal_name 
            FROM meals 
            WHERE area = ?
            ORDER BY meal_name
            LIMIT 5
        ''', (area,))
        
        meals = cursor.fetchall()
        for meal_name, in meals:
            print(f"   • {meal_name}")
        
        if count > 5:
            print(f"   ... and {count - 5} more")

def search_meals(cursor):
    """Search meals by name"""
    search_term = input("\nEnter search term: ").strip()
    
    if not search_term:
        print("No search term entered.")
        return
    
    print(f"\n🔍 SEARCH RESULTS FOR '{search_term}'")
    print("-" * 50)
    
    cursor.execute('''
        SELECT id, meal_name, category, area 
        FROM meals 
        WHERE meal_name LIKE ?
        ORDER BY meal_name
    ''', (f'%{search_term}%',))
    
    meals = cursor.fetchall()
    
    if meals:
        for i, (meal_id, name, category, area) in enumerate(meals, 1):
            print(f"{i:2d}. {name} ({category or 'N/A'}, {area or 'N/A'})")
        print(f"\nFound {len(meals)} meals")
    else:
        print("No meals found matching your search.")

def view_detailed_recipe(cursor):
    """View detailed recipe with ingredients"""
    print("\n📋 AVAILABLE MEALS")
    print("-" * 40)
    
    cursor.execute('''
        SELECT id, meal_name 
        FROM meals 
        ORDER BY meal_name
    ''')
    
    meals = cursor.fetchall()
    
    for i, (meal_id, name) in enumerate(meals, 1):
        print(f"{i:2d}. {name}")
    
    try:
        choice = int(input(f"\nEnter meal number (1-{len(meals)}): "))
        if 1 <= choice <= len(meals):
            meal_id, meal_name = meals[choice - 1]
            show_recipe_details(cursor, meal_id, meal_name)
        else:
            print("Invalid meal number.")
    except ValueError:
        print("Please enter a valid number.")

def show_recipe_details(cursor, meal_id, meal_name):
    """Show detailed recipe information"""
    print(f"\n🍽️ RECIPE: {meal_name}")
    print("=" * (len(meal_name) + 10))
    
    # Get meal details
    cursor.execute('''
        SELECT category, area, instructions, meal_thumb, tags, youtube
        FROM meals 
        WHERE id = ?
    ''', (meal_id,))
    
    result = cursor.fetchone()
    if result:
        category, area, instructions, thumb, tags, youtube = result
        
        print(f"Category: {category or 'N/A'}")
        print(f"Cuisine: {area or 'N/A'}")
        if tags:
            print(f"Tags: {tags}")
        if youtube:
            print(f"Video: {youtube}")
        if thumb:
            print(f"Image: {thumb}")
        print()
        
        # Get ingredients
        cursor.execute('''
            SELECT ingredient_name, measurement
            FROM ingredients 
            WHERE meal_id = ?
            ORDER BY ingredient_order
        ''', (meal_id,))
        
        ingredients = cursor.fetchall()
        
        if ingredients:
            print("📋 INGREDIENTS:")
            print("-" * 20)
            for ingredient, measure in ingredients:
                if measure:
                    print(f"• {measure} {ingredient}")
                else:
                    print(f"• {ingredient}")
            print()
        
        # Show instructions
        if instructions:
            print("👨‍🍳 INSTRUCTIONS:")
            print("-" * 15)
            # Break instructions into paragraphs
            paragraphs = instructions.split('\r\n\r\n')
            for para in paragraphs:
                if para.strip():
                    print(f"{para.strip()}\n")

def view_schema(cursor):
    """View database schema"""
    print("\n🗄️ DATABASE SCHEMA")
    print("-" * 30)
    
    # Get table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    for table_name, in tables:
        print(f"\n📊 Table: {table_name}")
        
        # Get column info
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        for col_info in columns:
            col_id, name, col_type, not_null, default, pk = col_info
            pk_marker = " (PRIMARY KEY)" if pk else ""
            print(f"   • {name}: {col_type}{pk_marker}")

def main():
    """Main function"""
    print("Welcome to MealDB Database Viewer!")
    print()
    
    # Check for database files
    db_files = [f for f in os.listdir('.') if f.endswith('.db')]
    
    if not db_files:
        print("❌ No database files found in current directory.")
        print("Run 'python simple_demo.py' first to create a database.")
        return
    
    if len(db_files) == 1:
        db_path = db_files[0]
        print(f"Using database: {db_path}")
    else:
        print("Multiple database files found:")
        for i, db_file in enumerate(db_files, 1):
            print(f"{i}. {db_file}")
        
        try:
            choice = int(input(f"Choose database (1-{len(db_files)}): "))
            if 1 <= choice <= len(db_files):
                db_path = db_files[choice - 1]
            else:
                print("Invalid choice.")
                return
        except ValueError:
            print("Please enter a valid number.")
            return
    
    print()
    view_database(db_path)

if __name__ == "__main__":
    main()
