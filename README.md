# 🍽️ MealDB ETL Project

A comprehensive Python-based ETL (Extract, Transform, Load) pipeline for TheMealDB API that extracts random recipes, transforms key data fields, and stores them in a database. **Features a modern desktop GUI, SQLite (no setup required), and MySQL (production-ready) support**.

## 🚀 Quick Start (30 seconds)

**New! Modern Desktop GUI - No database setup required:**

```bash
# 1. Install requests (only requirement for quick start)
pip install requests

# 2. Launch the modern GUI application
python recipe_manager_gui.py

# OR run the original demos:
# 3. Run the demo - creates database and adds 15 recipes
python simple_demo.py

# 4. View your recipes
python view_database.py
```

**Your database will grow every time you pull more recipes from the GUI!**

## ✨ Features

✅ **🎨 Modern Desktop GUI (NEW!)**
- 🖥️ Beautiful, modern interface with professional design
- 🔄 One-click recipe pulling with customizable amounts (1-50 recipes)
- 📊 Real-time statistics cards showing database growth
- 🔍 Advanced search and filtering by cuisine, category, and name
- 📖 Rich recipe details with formatted ingredients and instructions
- 🎯 Smart duplicate detection - never get the same recipe twice
- ⚡ Background processing - GUI stays responsive during API calls

✅ **Instant SQLite Version**
- ⚡ No MySQL setup required - works immediately
- 🔄 Run multiple times to grow your recipe database
- 📊 Smart duplicate detection (enhanced version)
- 🔍 Interactive database viewer included

✅ **Production MySQL Version**
- 🗄️ Full MySQL database with optimized schema
- 📈 ETL operation logging and monitoring
- 🔄 Data upsert capabilities (insert new, update existing)
- ⚙️ Command-line interface for automation

✅ **Interactive Features**
- 🌐 Streamlit web dashboard for recipe browsing
- 🔍 Filter by category, area/cuisine, and search by name
- 📊 Visual analytics with charts and statistics
- 💻 Multiple interfaces: GUI, CLI, Web, and Python scripts

✅ **Growing Recipe Database**
- 🍽️ **306 total recipes available** from TheMealDB API (as of 2025)
- 📈 Database grows with each pull: 15 → 30 → 45 → 100+ recipes
- 🌍 Discover cuisines from 30+ countries across 14 categories
- 🏷️ Categories include: Beef (48), Dessert (65), Chicken (36), Seafood (29), and more

## 📁 Project Structure & File Explanations

```
api/
├── 🎨 Modern GUI Application
│   └── recipe_manager_gui.py  # 🌟 NEW! Modern desktop GUI with all features
│
├── 📄 Core ETL Files
│   ├── config.py              # Configuration management (SQLite/MySQL switching)
│   ├── api_client.py         # TheMealDB API client (all endpoint calls)
│   ├── data_transformer.py   # Data cleaning & transformation logic
│   ├── database_manager.py   # Database operations (MySQL version)
│   └── etl_pipeline.py       # Full ETL pipeline (production version)
│
├── 🎯 Quick Start Files (SQLite - No Setup Required)
│   ├── simple_demo.py        # 🌟 Main demo - adds 15 recipes each run
│   ├── enhanced_demo.py      # 🧠 Smart demo - avoids duplicates, tracks runs
│   ├── view_database.py      # 👀 Interactive database browser
│   └── test_api.py          # 🧪 API connectivity tester
│
├── 🌐 Web Interface
│   ├── dashboard.py          # Streamlit web dashboard
│   └── cli.py               # Command line interface
│
├── 🔧 Utilities
│   └── count_meals.py        # 📊 Check total meals available in API
│
├── ⚙️ Setup & Configuration
│   ├── requirements.txt      # Python dependencies
│   ├── .env                 # Environment variables
│   ├── setup.py             # Python setup script
│   ├── setup.bat            # Windows batch setup
│   ├── database_schema.sql   # MySQL database schema
│   └── database_schema_sqlite.sql  # SQLite schema
│
└── 📚 Documentation
    ├── README.md            # This file
    ├── GETTING_STARTED.md   # Detailed setup guide
    └── MYSQL_SOLUTION.md    # MySQL troubleshooting guide
```

### 🌟 **Key Files Explained:**

#### **`recipe_manager_gui.py`** - Modern Desktop GUI 🎨 (NEW!)
- **What it does**: Beautiful desktop application for managing your recipe collection
- **Features**: Modern UI, one-click recipe pulling, search/filter, detailed recipe view
- **Perfect for**: Users who prefer graphical interfaces over command line
- **Usage**: `python recipe_manager_gui.py`
- **Highlights**: Professional design, real-time stats, background processing

#### **`simple_demo.py`** - Your Command Line Tool 🎯
- **What it does**: Fetches 15 random recipes and adds them to your database
- **Run multiple times**: Database grows each time (15 → 30 → 45...)
- **Perfect for**: Quick recipe collection, no technical setup needed
- **Usage**: `python simple_demo.py`

#### **`enhanced_demo.py`** - Smart Version 🧠
- **What it does**: Same as simple demo but avoids duplicate recipes
- **Features**: Run tracking, duplicate detection, shows what's new
- **Perfect for**: Building large unique recipe collections
- **Usage**: `python enhanced_demo.py`

#### **`view_database.py`** - Database Explorer 👀
- **What it does**: Interactive menu to browse your recipe collection
- **Features**: Search, filter by category/cuisine, view full recipes
- **Perfect for**: Exploring your growing recipe database
- **Usage**: `python view_database.py`

#### **`count_meals.py`** - API Statistics 📊 (NEW!)
- **What it does**: Checks how many total recipes are available in TheMealDB API
- **Features**: Shows breakdown by category, current total count
- **Perfect for**: Understanding the scope of available data
- **Usage**: `python count_meals.py`

#### **`etl_pipeline.py`** - Production ETL 🏭
- **What it does**: Full-featured ETL with MySQL, logging, monitoring
- **Features**: Incremental loads, search by cuisine/ingredient, production-ready
- **Perfect for**: Large-scale deployments, automated systems
- **Usage**: `python cli.py etl full --count 50`

## 🚀 Installation & Setup

### Option 1: Modern GUI (Recommended) 🎨

**Beautiful desktop interface - works immediately:**

```bash
# 1. Install minimal requirements
pip install requests

# 2. Launch the modern GUI application
python recipe_manager_gui.py

# 3. Use the GUI to:
#    - Pull recipes with one click
#    - Browse your collection with search/filter
#    - View detailed recipe information
#    - Monitor database growth with real-time stats
```

### Option 2: Quick Start (SQLite Command Line) ⚡

**No database setup required! Works immediately:**

```bash
# 1. Install minimal requirements
pip install requests

# 2. Test API connection
python test_api.py

# 3. Create your first recipe database
python simple_demo.py

# 4. Browse your recipes
python view_database.py

# 5. Check total available recipes in API
python count_meals.py
```

### Option 3: Full Setup (All Features) 🔧

**For web dashboard and advanced features:**

```bash
# 1. Install all dependencies
pip install -r requirements.txt

# 2. Configure environment (optional for SQLite)
# Edit .env file with your preferences

# 3. Run enhanced demo with duplicate detection
python enhanced_demo.py

# 4. Launch web dashboard
streamlit run dashboard.py
```

### Option 4: Production MySQL Setup 🏭

**For production deployments:**

1. **Install MySQL Server**
   ```bash
   # Download from: https://dev.mysql.com/downloads/
   # Or use XAMPP for easier setup
   ```

2. **Create database**
   ```sql
   CREATE DATABASE mealdb_etl;
   ```

3. **Configure environment**
   ```env
   DB_TYPE=mysql
   DB_HOST=localhost
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_NAME=mealdb_etl
   ```

4. **Initialize and run**
   ```bash
   python cli.py db init
   python cli.py etl full --count 50
   ```

## 🍽️ Usage & Commands

### � Modern Desktop GUI (NEW!)

**The easiest way to manage your recipe collection:**
```bash
# Launch the beautiful desktop application
python recipe_manager_gui.py

# Features in the GUI:
# ✅ Pull 1-50 recipes with one click
# ✅ Real-time database statistics (meals, ingredients, categories, cuisines)
# ✅ Search recipes by name
# ✅ Filter by category (Beef, Dessert, Chicken, etc.)
# ✅ Filter by cuisine (Italian, Thai, Mexican, etc.)
# ✅ View detailed recipe information with ingredients and instructions
# ✅ Smart duplicate detection - never get the same recipe twice
# ✅ Modern, professional interface with beautiful design
```

### �🎯 Quick Recipe Collection (SQLite)

**Add recipes to your database:**
```bash
# Add 15 random recipes (run multiple times to grow database)
python simple_demo.py

# Add recipes with smart duplicate detection
python enhanced_demo.py

# Browse your recipe collection
python view_database.py

# Check how many recipes are available in the API
python count_meals.py
```

**Database Growth Examples:**
```bash
# Start fresh
python simple_demo.py        # Database: 15 meals
python simple_demo.py        # Database: 30 meals  
python simple_demo.py        # Database: 45 meals
python enhanced_demo.py      # Database: 45+ unique meals (skips duplicates)
```

### 🌐 Web Dashboard

**Launch interactive web interface:**
```bash
# Install streamlit first
pip install streamlit plotly

# Launch dashboard
streamlit run dashboard.py
# Opens at: http://localhost:8501
```

**Dashboard Features:**
- 📊 **Overview**: Database statistics, growth tracking
- 🔍 **Recipe Browser**: Filter by cuisine, category, search by name
- 📈 **Analytics**: Visual charts of your recipe collection
- ⚙️ **ETL Operations**: Add more recipes from web interface

### 💻 Command Line Interface (Production)

**Database management:**
```bash
# Initialize MySQL database
python cli.py db init

# Show database statistics
python cli.py db stats
```

**ETL operations:**
```bash
# Load 20 random recipes
python cli.py etl full --count 20

# Add 5 more recipes (incremental)
python cli.py etl incremental --count 5

# Load specific cuisines/categories
python cli.py etl search "Italian" --type area
python cli.py etl search "chicken" --type ingredient
python cli.py etl search "Dessert" --type category
python cli.py etl search "Pasta" --type name
```

**Advanced usage:**
```bash
# Load 100 recipes for large database
python cli.py etl full --count 100

# Load all Italian recipes
python cli.py etl search "Italian" --type area

# Load all chicken recipes  
python cli.py etl search "chicken" --type ingredient

# Launch web dashboard
python cli.py dashboard
```

### 🐍 Direct Python Usage

**For custom integrations:**
```python
# Modern GUI version (recommended)
from recipe_manager_gui import RecipeManagerGUI

app = RecipeManagerGUI()
app.run()  # Launch the desktop GUI

# SQLite version (simple)
from simple_demo import SimpleETL

etl = SimpleETL()
etl.run_demo(meal_count=25)  # Add 25 recipes
stats = etl.get_stats()      # Get database statistics

# Enhanced version (duplicate detection)
from enhanced_demo import EnhancedETL

etl = EnhancedETL()
etl.run_demo(meal_count=20)   # Add 20 unique recipes
etl.show_run_history()        # Show all previous runs

# Production version (MySQL)
from etl_pipeline import MealETL

etl = MealETL()
etl.db_manager.execute_schema()           # Setup database
etl.run_full_etl(meal_count=50)          # Load 50 recipes
etl.search_and_load_meals('Thai', 'area') # Load Thai cuisine
etl.cleanup()                             # Close connections
```

## 📊 Database Schema & Data

### SQLite Tables (Quick Start)
```sql
meals          # Recipe information (name, category, area, instructions)
ingredients    # Recipe ingredients with measurements
```

### MySQL Tables (Production)
```sql
meals          # Main recipe information
ingredients    # Recipe ingredients with measurements  
categories     # Recipe categories (Dessert, Seafood, etc.)
areas          # Geographic areas/cuisines (Italian, Thai, etc.)
etl_logs       # ETL operation tracking and monitoring
```

### Sample Data Structure
```
🍽️ Chicken Alfredo (Italian, Main Course)
   📋 Ingredients: 
   • 500g Penne pasta
   • 300ml Heavy cream  
   • 200g Parmesan cheese
   • 2 Chicken breasts
   • 3 cloves Garlic
   
🍽️ Thai Green Curry (Thai, Chicken)
   📋 Ingredients:
   • 400ml Coconut milk
   • 2 tbsp Thai curry paste
   • 500g Chicken thighs
   • 1 Aubergine
```

## 🌐 API Integration & Data Sources

### TheMealDB API Statistics (Updated 2025)
- **🍽️ Total Recipes Available**: **306 unique meals**
- **📂 Categories**: 14 (Beef: 48, Dessert: 65, Chicken: 36, Seafood: 29, etc.)
- **🌍 Cuisines**: 25+ countries represented
- **📈 API Updates**: Database grows periodically with community contributions
- **🔄 Your Limit**: You can collect all 306 recipes - no API restrictions!

### TheMealDB API Endpoints Used
- **Random meals**: `www.themealdb.com/api/json/v1/1/random.php`
- **Search by name**: `www.themealdb.com/api/json/v1/1/search.php?s={name}`
- **Search by letter**: `www.themealdb.com/api/json/v1/1/search.php?f={letter}`
- **Lookup by ID**: `www.themealdb.com/api/json/v1/1/lookup.php?i={id}`
- **Categories**: `www.themealdb.com/api/json/v1/1/categories.php`
- **Areas**: `www.themealdb.com/api/json/v1/1/list.php?a=list`
- **Filter by category**: `www.themealdb.com/api/json/v1/1/filter.php?c={category}`
- **Filter by area**: `www.themealdb.com/api/json/v1/1/filter.php?a={area}`
- **Filter by ingredient**: `www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}`

### Data Transformation Pipeline
- **Text cleaning**: Remove extra whitespace, HTML tags, normalize text
- **Data validation**: Handle null values, empty strings
- **Ingredient extraction**: Parse ingredients and measurements from API format
- **Date parsing**: Convert date strings to proper datetime objects
- **Data type conversion**: Ensure proper data types for database storage

## 🔧 Advanced Features

### Smart Duplicate Detection
```python
# Enhanced demo avoids duplicate recipes
existing_ids = get_existing_meal_ids()
if meal_id not in existing_ids:
    add_to_database(meal)
```

### Run Tracking & History
```bash
# View your ETL run history
python enhanced_demo.py
# Shows: Run #1: 15 meals, Run #2: 12 new meals, etc.
```

### Multi-Database Support
```python
# Switch between SQLite and MySQL
DB_TYPE=sqlite    # Quick start, no setup
DB_TYPE=mysql     # Production ready
```

### Performance Optimizations
- **Batch processing**: Process data in configurable batch sizes
- **Database indexing**: Optimized indexes for query performance
- **Connection pooling**: Efficient database connection management
- **Caching**: Streamlit caching for dashboard performance

## 🚀 Getting More Recipes

### Grow Your Database Systematically
```bash
# Start with random global recipes
python simple_demo.py           # 15 random recipes
python simple_demo.py           # 15 more (30 total)

# Add specific cuisines
python cli.py etl search "Italian" --type area      # All Italian recipes
python cli.py etl search "Thai" --type area         # All Thai recipes
python cli.py etl search "Mexican" --type area      # All Mexican recipes

# Add by categories  
python cli.py etl search "Dessert" --type category  # All desserts
python cli.py etl search "Seafood" --type category  # All seafood

# Add by ingredients
python cli.py etl search "chicken" --type ingredient # All chicken recipes
python cli.py etl search "beef" --type ingredient    # All beef recipes
```

### Building a Complete Recipe Database
```bash
# Method 1: GUI (easiest and most enjoyable)
python recipe_manager_gui.py
# Use the GUI to pull recipes with progress tracking
# Pull 10-20 recipes at a time until you have the full collection

# Method 2: Random collection (command line)
for i in {1..20}; do python simple_demo.py; done
# Result: 300 random recipes from around the world (with some duplicates)

# Method 3: Systematic collection (complete)
python cli.py etl search "Italian" --type area
python cli.py etl search "Thai" --type area  
python cli.py etl search "Indian" --type area
python cli.py etl search "Chinese" --type area
python cli.py etl search "Mexican" --type area
# Result: Complete cuisine collections

# Method 4: Category collection (organized)
python cli.py etl search "Dessert" --type category   # All 65 desserts
python cli.py etl search "Beef" --type category      # All 48 beef recipes
python cli.py etl search "Chicken" --type category   # All 36 chicken recipes
python cli.py etl search "Seafood" --type category   # All 29 seafood recipes
# Result: Well-organized recipe database by type
```

**🎯 Pro Tip**: The GUI application (`recipe_manager_gui.py`) is the most user-friendly way to collect all 306 recipes!

## 🛠️ Development & Customization

### Adding New Features
1. **New API endpoints**: Extend `api_client.py`
2. **Data transformations**: Modify `data_transformer.py`
3. **Database operations**: Update `database_manager.py`
4. **Dashboard features**: Enhance `dashboard.py`

### Testing Your Setup
```bash
# Test API connectivity
python test_api.py

# Test with small dataset
python simple_demo.py

# Check database
python view_database.py

# Full pipeline test (MySQL)
python cli.py etl full --count 5
```

### Monitoring & Logging
```bash
# Check ETL logs (MySQL version)
python cli.py db stats

# View log file
tail -f etl.log

# Database statistics
python view_database.py  # Choose option 6 for schema
```

## 🔍 Troubleshooting

### Common Issues & Solutions

**🚫 "No module named 'requests'"**
```bash
pip install requests
```

**🚫 "Database file not found"**
```bash
# Run demo first to create database
python simple_demo.py
```

**🚫 MySQL connection failed**
```bash
# Use SQLite version instead (no setup required)
python simple_demo.py

# Or fix MySQL - see MYSQL_SOLUTION.md
```

**🚫 API rate limiting**
- The free API has rate limits
- Add delays between requests if needed
- Use enhanced demo for better handling

**🚫 Memory issues**
- Reduce batch size in configuration
- Process data in smaller chunks

### Getting Help
1. Check the `etl.log` file for detailed error messages
2. Verify API connectivity with `python test_api.py`
3. Start with SQLite version: `python simple_demo.py`
4. Read `GETTING_STARTED.md` for detailed setup
5. Check `MYSQL_SOLUTION.md` for MySQL issues

## 📈 Project Status & Stats

### What's Working Right Now ✅
- ✅ SQLite demos (no setup required)
- ✅ Recipe database growth (15 → 30 → 45...)
- ✅ Interactive database viewer
- ✅ API connectivity (tested and working)
- ✅ Data transformation pipeline
- ✅ Web dashboard (with streamlit)
- ✅ MySQL production version

### Current Capabilities
- 🌍 **25+ cuisines**: Italian, Thai, Indian, Mexican, Chinese, etc.
- 🏷️ **14 categories**: Dessert (65), Beef (48), Chicken (36), Seafood (29), etc.
- 🍽️ **306 total recipes**: Complete TheMealDB collection available
- 📊 **Full analytics**: Charts, statistics, trends
- 🔍 **Smart search**: By name, ingredient, cuisine, category
- 🎨 **Modern GUI**: Beautiful desktop interface for easy recipe management

## 🎯 Quick Commands Cheat Sheet

```bash
# 🚀 QUICK START (Modern GUI)
python recipe_manager_gui.py           # Launch beautiful desktop app

# 🚀 QUICK START (SQLite Command Line)
python simple_demo.py                  # Add 15 recipes (repeatable)
python enhanced_demo.py                 # Add unique recipes only  
python view_database.py                 # Browse your collection
python count_meals.py                   # Check total API recipes (306)

# 🌐 WEB INTERFACE
streamlit run dashboard.py              # Launch web dashboard

# 💻 PRODUCTION (MySQL)
python cli.py db init                   # Setup MySQL database
python cli.py etl full --count 50       # Load 50 random recipes
python cli.py etl search "Italian" --type area  # Load Italian cuisine

# 🔧 UTILITIES
python test_api.py                      # Test API connection
python cli.py db stats                  # Database statistics
```

## 📚 Documentation Files

- **README.md** (this file): Complete project overview
- **GETTING_STARTED.md**: Step-by-step setup guide
- **MYSQL_SOLUTION.md**: MySQL troubleshooting guide

## 🎉 Success Indicators

After setup, you should see:
- ✅ `python test_api.py` passes connectivity test
- ✅ `python recipe_manager_gui.py` launches modern desktop GUI
- ✅ `python simple_demo.py` creates database with recipes
- ✅ `python view_database.py` shows your recipe collection
- ✅ `python count_meals.py` shows "TOTAL MEALS: 306"
- ✅ Database file created (e.g., `mealdb_simple.db` or `mealdb_gui.db`)
- ✅ Growing recipe count with each demo run or GUI pull

## 🌟 What's Next?

1. **Start with GUI**: Run `python recipe_manager_gui.py` for the best experience
2. **Or start simple**: Run `python simple_demo.py` a few times
3. **Explore data**: Use `python view_database.py` to browse recipes  
4. **Go visual**: Launch web dashboard with `streamlit run dashboard.py`
5. **Check progress**: Use `python count_meals.py` to see you can collect all 306 recipes
6. **Scale up**: Try MySQL version for production use
7. **Customize**: Modify code for your specific needs

---

**🍳 Happy cooking and coding! 👨‍💻**

*This project demonstrates a complete ETL pipeline with real-world data, from simple demos to production-ready deployments.*
