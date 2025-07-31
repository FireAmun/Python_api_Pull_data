@echo off
echo MealDB ETL Project - Quick Start
echo ================================

echo.
echo Installing Python dependencies...
python -m pip install -r requirements.txt

echo.
echo Setup completed!
echo.
echo Next steps:
echo 1. Edit .env file with your MySQL credentials
echo 2. Create MySQL database: CREATE DATABASE mealdb_etl;
echo 3. Run: python cli.py db init
echo 4. Run demo: python demo.py
echo 5. Launch dashboard: python cli.py dashboard
echo.
pause
