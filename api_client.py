import requests
import pandas as pd
import logging
from typing import Dict, List, Optional, Any
from config import Config

class MealDBAPI:
    """API client for TheMealDB API"""
    
    def __init__(self):
        self.config = Config()
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)
        
    def _make_request(self, url: str, params: Dict = None) -> Optional[Dict]:
        """Make HTTP request to the API"""
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {e}")
            return None
    
    def get_random_meal(self) -> Optional[Dict]:
        """Get a random meal"""
        data = self._make_request(self.config.ENDPOINTS['random'])
        return data.get('meals', [None])[0] if data else None
    
    def get_multiple_random_meals(self, count: int = 10) -> List[Dict]:
        """Get multiple random meals"""
        meals = []
        for _ in range(count):
            meal = self.get_random_meal()
            if meal:
                meals.append(meal)
        return meals
    
    def search_meal_by_name(self, name: str) -> List[Dict]:
        """Search meals by name"""
        params = {'s': name}
        data = self._make_request(self.config.ENDPOINTS['search_by_name'], params)
        return data.get('meals', []) if data else []
    
    def search_meal_by_letter(self, letter: str) -> List[Dict]:
        """Search meals by first letter"""
        params = {'f': letter}
        data = self._make_request(self.config.ENDPOINTS['search_by_letter'], params)
        return data.get('meals', []) if data else []
    
    def lookup_meal_by_id(self, meal_id: str) -> Optional[Dict]:
        """Lookup meal by ID"""
        params = {'i': meal_id}
        data = self._make_request(self.config.ENDPOINTS['lookup_by_id'], params)
        return data.get('meals', [None])[0] if data else None
    
    def get_categories(self) -> List[Dict]:
        """Get all meal categories"""
        data = self._make_request(self.config.ENDPOINTS['categories'])
        return data.get('categories', []) if data else []
    
    def get_areas(self) -> List[Dict]:
        """Get all areas"""
        data = self._make_request(self.config.ENDPOINTS['areas'])
        return data.get('meals', []) if data else []
    
    def get_ingredients(self) -> List[Dict]:
        """Get all ingredients"""
        data = self._make_request(self.config.ENDPOINTS['ingredients'])
        return data.get('meals', []) if data else []
    
    def filter_by_category(self, category: str) -> List[Dict]:
        """Filter meals by category"""
        params = {'c': category}
        data = self._make_request(self.config.ENDPOINTS['filter_by_category'], params)
        return data.get('meals', []) if data else []
    
    def filter_by_area(self, area: str) -> List[Dict]:
        """Filter meals by area"""
        params = {'a': area}
        data = self._make_request(self.config.ENDPOINTS['filter_by_area'], params)
        return data.get('meals', []) if data else []
    
    def filter_by_ingredient(self, ingredient: str) -> List[Dict]:
        """Filter meals by main ingredient"""
        params = {'i': ingredient}
        data = self._make_request(self.config.ENDPOINTS['filter_by_ingredient'], params)
        return data.get('meals', []) if data else []
