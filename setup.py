#!/usr/bin/env python3
"""
Setup script for MealDB ETL Project
"""

import os
import sys
import subprocess

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install requirements: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        print("Creating .env file...")
        env_content = """# MySQL Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=mealdb_etl

# API Configuration
BASE_URL=https://www.themealdb.com/api/json/v1/1

# Application Configuration
LOG_LEVEL=INFO
BATCH_SIZE=10"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✓ .env file created")
        print("⚠️  Please edit .env file with your MySQL credentials")
    else:
        print("✓ .env file already exists")

def check_mysql():
    """Check if MySQL is available"""
    try:
        import mysql.connector
        print("✓ MySQL connector available")
        return True
    except ImportError:
        print("✗ MySQL connector not available")
        return False

def main():
    print("🍽️ MealDB ETL Project Setup")
    print("=" * 40)
    
    # Install requirements
    if not install_requirements():
        print("Setup failed. Please install requirements manually.")
        return
    
    # Create .env file
    create_env_file()
    
    # Check MySQL
    check_mysql()
    
    print("\n" + "=" * 40)
    print("Setup completed!")
    print("\nNext steps:")
    print("1. Edit .env file with your MySQL credentials")
    print("2. Create MySQL database: CREATE DATABASE mealdb_etl;")
    print("3. Run: python cli.py db init")
    print("4. Run demo: python demo.py")
    print("5. Launch dashboard: python cli.py dashboard")

if __name__ == "__main__":
    main()
