import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Database Configuration - SQLite alternative for easier setup
    DB_TYPE = os.getenv('DB_TYPE', 'sqlite')  # 'sqlite' or 'mysql'
    
    # SQLite configuration
    SQLITE_DB_PATH = os.getenv('SQLITE_DB_PATH', 'mealdb_etl.db')
    
    # MySQL configuration (for when MySQL is available)
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'mealdb_etl')
    
    # API Configuration
    BASE_URL = os.getenv('BASE_URL', 'https://www.themealdb.com/api/json/v1/1')
    
    # Application Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', 10))
    
    @property
    def database_url(self):
        if self.DB_TYPE.lower() == 'sqlite':
            return f"sqlite:///{self.SQLITE_DB_PATH}"
        else:
            return f"mysql+mysqlconnector://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # API Endpoints
    ENDPOINTS = {
        'random': f"{BASE_URL}/random.php",
        'search_by_name': f"{BASE_URL}/search.php",
        'search_by_letter': f"{BASE_URL}/search.php",
        'lookup_by_id': f"{BASE_URL}/lookup.php",
        'categories': f"{BASE_URL}/categories.php",
        'areas': f"{BASE_URL}/list.php?a=list",
        'ingredients': f"{BASE_URL}/list.php?i=list",
        'filter_by_category': f"{BASE_URL}/filter.php",
        'filter_by_area': f"{BASE_URL}/filter.php",
        'filter_by_ingredient': f"{BASE_URL}/filter.php"
    }
