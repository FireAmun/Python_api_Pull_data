-- SQLite-compatible Database Schema for MealDB ETL Project
-- This schema works with both SQLite and MySQL

-- Create meals table
CREATE TABLE IF NOT EXISTS meals (
    id TEXT PRIMARY KEY,
    meal_name TEXT NOT NULL,
    category TEXT,
    area TEXT,
    instructions TEXT,
    meal_thumb TEXT,
    tags TEXT,
    youtube TEXT,
    source TEXT,
    image_source TEXT,
    creative_commons_confirmed TEXT,
    date_modified TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create ingredients table
CREATE TABLE IF NOT EXISTS ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meal_id TEXT,
    ingredient_name TEXT,
    measurement TEXT,
    ingredient_order INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (meal_id) REFERENCES meals(id) ON DELETE CASCADE
);

-- Create categories table
CREATE TABLE IF NOT EXISTS categories (
    id TEXT PRIMARY KEY,
    category_name TEXT NOT NULL,
    category_thumb TEXT,
    category_description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create areas table
CREATE TABLE IF NOT EXISTS areas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    area_name TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create ETL log table
CREATE TABLE IF NOT EXISTS etl_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operation_type TEXT,
    status TEXT,
    records_processed INTEGER,
    error_message TEXT,
    execution_time REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_meal_category ON meals(category);
CREATE INDEX IF NOT EXISTS idx_meal_area ON meals(area);
CREATE INDEX IF NOT EXISTS idx_meal_name ON meals(meal_name);
CREATE INDEX IF NOT EXISTS idx_ingredients_meal_id ON ingredients(meal_id);
CREATE INDEX IF NOT EXISTS idx_etl_logs_date ON etl_logs(created_at);
