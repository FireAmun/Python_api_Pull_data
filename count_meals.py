#!/usr/bin/env python3
"""
Quick script to count total meals in TheMealDB API
"""

import requests

print("🔍 Counting meals in TheMealDB API...")

# Get all categories
response = requests.get('https://www.themealdb.com/api/json/v1/1/list.php?c=list')
categories = response.json()['meals']

total_meals = 0

print(f"\n📊 Meals by Category:")
print("-" * 30)

for cat in categories:
    cat_name = cat['strCategory']
    response = requests.get(f'https://www.themealdb.com/api/json/v1/1/filter.php?c={cat_name}')
    meals = response.json().get('meals', [])
    count = len(meals) if meals else 0
    total_meals += count
    print(f"{cat_name:15}: {count:3} meals")

print("-" * 30)
print(f"🍽️ TOTAL MEALS: {total_meals}")
print(f"📂 Categories: {len(categories)}")
print(f"📈 Average per category: {total_meals/len(categories):.1f}")
