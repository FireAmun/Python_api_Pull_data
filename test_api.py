#!/usr/bin/env python3
"""
Test script to verify TheMealDB API connectivity
"""

import requests
import json

def test_api_endpoints():
    """Test various TheMealDB API endpoints"""
    
    print("🧪 Testing TheMealDB API Endpoints")
    print("=" * 50)
    
    endpoints = {
        "Random Meal": "https://www.themealdb.com/api/json/v1/1/random.php",
        "Categories": "https://www.themealdb.com/api/json/v1/1/categories.php",
        "Areas": "https://www.themealdb.com/api/json/v1/1/list.php?a=list",
        "Search by Name": "https://www.themealdb.com/api/json/v1/1/search.php?s=Arrabiata",
        "Filter by Category": "https://www.themealdb.com/api/json/v1/1/filter.php?c=Seafood"
    }
    
    for name, url in endpoints.items():
        try:
            print(f"\nTesting {name}...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if name == "Random Meal":
                meal = data.get('meals', [{}])[0]
                print(f"   ✓ Success: Got meal '{meal.get('strMeal', 'Unknown')}'")
                
            elif name == "Categories":
                categories = data.get('categories', [])
                print(f"   ✓ Success: Found {len(categories)} categories")
                
            elif name == "Areas":
                areas = data.get('meals', [])
                print(f"   ✓ Success: Found {len(areas)} areas")
                
            elif name == "Search by Name":
                meals = data.get('meals', [])
                if meals:
                    print(f"   ✓ Success: Found {len(meals)} Arrabiata recipes")
                else:
                    print("   ⚠️  No meals found for Arrabiata")
                    
            elif name == "Filter by Category":
                meals = data.get('meals', [])
                print(f"   ✓ Success: Found {len(meals)} seafood recipes")
                
        except requests.exceptions.RequestException as e:
            print(f"   ✗ Failed: {e}")
        except Exception as e:
            print(f"   ✗ Error: {e}")
    
    print("\n" + "=" * 50)
    print("API connectivity test completed!")

def test_sample_data():
    """Show sample data structure"""
    print("\n📊 Sample Data Structure")
    print("=" * 30)
    
    try:
        response = requests.get("https://www.themealdb.com/api/json/v1/1/random.php", timeout=10)
        response.raise_for_status()
        
        data = response.json()
        meal = data.get('meals', [{}])[0]
        
        if meal:
            print(f"Meal Name: {meal.get('strMeal')}")
            print(f"Category: {meal.get('strCategory')}")
            print(f"Area: {meal.get('strArea')}")
            print(f"Instructions: {meal.get('strInstructions', '')[:100]}...")
            
            # Show first few ingredients
            print("\nIngredients:")
            for i in range(1, 6):
                ingredient = meal.get(f'strIngredient{i}', '').strip()
                measure = meal.get(f'strMeasure{i}', '').strip()
                if ingredient:
                    print(f"  - {measure} {ingredient}")
                    
    except Exception as e:
        print(f"Failed to get sample data: {e}")

if __name__ == "__main__":
    test_api_endpoints()
    test_sample_data()
