# 🍽️ MealDB ETL Project - Getting Started Guide

## Quick Start (5 minutes)

### Step 1: Install Dependencies
```bash
# Option 1: Windows batch file
setup.bat

# Option 2: Manual installation
python -m pip install -r requirements.txt
```

### Step 2: Configure Database
1. **Install and start MySQL**
2. **Create database:**
   ```sql
   CREATE DATABASE mealdb_etl;
   ```
3. **Edit `.env` file** with your MySQL credentials:
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=mealdb_etl
   ```

### Step 3: Initialize and Test
```bash
# Test API connectivity
python test_api.py

# Initialize database schema
python cli.py db init

# Run demo (loads sample data)
python demo.py
```

### Step 4: Launch Dashboard
```bash
# Start the interactive web dashboard
python cli.py dashboard
```

The dashboard will open at http://localhost:8501

## 🎯 What You Get

### ✅ Complete ETL Pipeline
- **Extract**: Pull data from TheMealDB API
- **Transform**: Clean and normalize recipe data
- **Load**: Store in MySQL with proper schema

### ✅ Interactive Dashboard
- Browse recipes with filters
- Visual analytics and charts
- Run ETL jobs from web interface
- Real-time database statistics

### ✅ Command Line Tools
```bash
# Load random meals
python cli.py etl full --count 20

# Search specific cuisines
python cli.py etl search "Italian" --type area

# Database statistics
python cli.py db stats
```

### ✅ Database Schema
- **meals**: Recipe information
- **ingredients**: Recipe components
- **categories**: Recipe types
- **areas**: Geographic cuisines
- **etl_logs**: Operation tracking

## 📊 Sample Commands

```bash
# Load 50 random recipes
python cli.py etl full --count 50

# Load all Italian recipes
python cli.py etl search "Italian" --type area

# Load all chicken recipes
python cli.py etl search "chicken" --type ingredient

# Load dessert category
python cli.py etl search "Dessert" --type category

# Show database stats
python cli.py db stats
```

## 🔧 Troubleshooting

**Can't connect to database?**
- Check MySQL is running
- Verify credentials in `.env`
- Ensure database exists

**API rate limiting?**
- Free API has limits
- Add delays between requests

**Missing dependencies?**
- Run `pip install -r requirements.txt`
- Check Python version (3.7+)

## 📈 Dashboard Features

### Overview Page
- Database statistics
- Recent ETL operations
- System health

### Meals Browser
- Filter by category, area, ingredients
- Search by recipe name
- View detailed recipe information
- See ingredient lists and instructions

### Analytics
- Recipe distribution charts
- Cuisine popularity
- Ingredient frequency analysis
- Interactive visualizations

### ETL Operations
- Load random recipes
- Search and import specific recipes
- Monitor ETL job progress
- Database management tools

## 🚀 Advanced Usage

### Custom ETL Jobs
```python
from etl_pipeline import MealETL

etl = MealETL()

# Load specific meal by ID
meal = etl.api_client.lookup_meal_by_id('52772')

# Search and load vegetarian meals
etl.search_and_load_meals('Vegetarian', 'category')
```

### Database Queries
```sql
-- Most popular cuisines
SELECT area, COUNT(*) as meal_count 
FROM meals 
GROUP BY area 
ORDER BY meal_count DESC;

-- Recipes with most ingredients
SELECT meal_name, COUNT(i.id) as ingredient_count
FROM meals m
JOIN ingredients i ON m.id = i.meal_id
GROUP BY m.id, meal_name
ORDER BY ingredient_count DESC;
```

## 📚 Project Structure

```
api/
├── 📄 config.py              # Configuration
├── 🌐 api_client.py         # API client
├── 🔄 data_transformer.py   # Data processing
├── 🗄️ database_manager.py   # Database ops
├── ⚙️ etl_pipeline.py       # Main pipeline
├── 📊 dashboard.py          # Web dashboard
├── 💻 cli.py               # Command line
├── 🧪 test_api.py          # API testing
├── 🎬 demo.py              # Demo script
└── 📋 requirements.txt      # Dependencies
```

## 🎉 Success Indicators

After setup, you should see:
- ✅ API connectivity test passes
- ✅ Database schema created
- ✅ Sample data loaded (demo.py)
- ✅ Dashboard accessible at localhost:8501
- ✅ CLI commands working

## 📞 Support

If you encounter issues:
1. Check the `etl.log` file for detailed error messages
2. Verify all dependencies are installed
3. Confirm database credentials are correct
4. Test API connectivity with `test_api.py`

## 🌟 Next Steps

1. **Explore the dashboard** - Browse recipes and analytics
2. **Load more data** - Use ETL commands to expand your database
3. **Customize** - Modify the code for your specific needs
4. **Analyze** - Run custom SQL queries on your recipe database

---

**Happy coding! 🍳👨‍💻**
