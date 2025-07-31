import pandas as pd
import logging
from typing import Dict, List, Any, Optional
import re
from datetime import datetime

class DataTransformer:
    """Transform raw API data for database storage"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text data"""
        if not text or text == 'null' or text == '':
            return None
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove HTML tags if any
        text = re.sub(r'<[^>]+>', '', text)
        
        return text
    
    def extract_ingredients(self, meal: Dict) -> List[Dict]:
        """Extract ingredients and measurements from meal data"""
        ingredients = []
        
        for i in range(1, 21):  # API has ingredients 1-20
            ingredient_key = f'strIngredient{i}'
            measure_key = f'strMeasure{i}'
            
            ingredient = meal.get(ingredient_key, '').strip()
            measure = meal.get(measure_key, '').strip()
            
            if ingredient and ingredient.lower() not in ['', 'null', 'none']:
                ingredients.append({
                    'ingredient_name': self.clean_text(ingredient),
                    'measurement': self.clean_text(measure) if measure else None,
                    'ingredient_order': i
                })
        
        return ingredients
    
    def transform_meal(self, meal: Dict) -> Dict:
        """Transform a single meal record"""
        try:
            transformed = {
                'id': meal.get('idMeal'),
                'meal_name': self.clean_text(meal.get('strMeal')),
                'category': self.clean_text(meal.get('strCategory')),
                'area': self.clean_text(meal.get('strArea')),
                'instructions': self.clean_text(meal.get('strInstructions')),
                'meal_thumb': meal.get('strMealThumb'),
                'tags': self.clean_text(meal.get('strTags')),
                'youtube': meal.get('strYoutube'),
                'source': meal.get('strSource'),
                'image_source': meal.get('strImageSource'),
                'creative_commons_confirmed': meal.get('strCreativeCommonsConfirmed'),
                'date_modified': self._parse_date(meal.get('dateModified'))
            }
            
            return transformed
            
        except Exception as e:
            self.logger.error(f"Error transforming meal {meal.get('idMeal', 'Unknown')}: {e}")
            return None
    
    def transform_meals_to_dataframe(self, meals: List[Dict]) -> pd.DataFrame:
        """Transform list of meals to pandas DataFrame"""
        transformed_meals = []
        
        for meal in meals:
            transformed = self.transform_meal(meal)
            if transformed:
                transformed_meals.append(transformed)
        
        if not transformed_meals:
            return pd.DataFrame()
        
        df = pd.DataFrame(transformed_meals)
        
        # Data type conversions and cleaning
        df['id'] = df['id'].astype(str)
        df['meal_name'] = df['meal_name'].astype(str)
        
        # Handle missing values
        df = df.fillna('')
        
        return df
    
    def transform_ingredients_to_dataframe(self, meals: List[Dict]) -> pd.DataFrame:
        """Transform ingredients from meals to pandas DataFrame"""
        all_ingredients = []
        
        for meal in meals:
            meal_id = meal.get('idMeal')
            if not meal_id:
                continue
                
            ingredients = self.extract_ingredients(meal)
            for ingredient in ingredients:
                ingredient['meal_id'] = meal_id
                all_ingredients.append(ingredient)
        
        if not all_ingredients:
            return pd.DataFrame()
        
        df = pd.DataFrame(all_ingredients)
        return df
    
    def transform_categories_to_dataframe(self, categories: List[Dict]) -> pd.DataFrame:
        """Transform categories to pandas DataFrame"""
        transformed_categories = []
        
        for category in categories:
            transformed = {
                'id': category.get('idCategory'),
                'category_name': self.clean_text(category.get('strCategory')),
                'category_thumb': category.get('strCategoryThumb'),
                'category_description': self.clean_text(category.get('strCategoryDescription'))
            }
            transformed_categories.append(transformed)
        
        if not transformed_categories:
            return pd.DataFrame()
        
        return pd.DataFrame(transformed_categories)
    
    def transform_areas_to_dataframe(self, areas: List[Dict]) -> pd.DataFrame:
        """Transform areas to pandas DataFrame"""
        area_names = [area.get('strArea') for area in areas if area.get('strArea')]
        
        if not area_names:
            return pd.DataFrame()
        
        return pd.DataFrame({'area_name': area_names})
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string to datetime object"""
        if not date_str or date_str == 'null':
            return None
        
        try:
            return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                return datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                self.logger.warning(f"Could not parse date: {date_str}")
                return None
