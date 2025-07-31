#!/usr/bin/env python3
"""
MealDB ETL Command Line Interface
Provides command-line access to ETL operations
"""

import argparse
import sys
from etl_pipeline import MealETL

def main():
    parser = argparse.ArgumentParser(description='MealDB ETL Pipeline CLI')
    
    # Add subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # ETL commands
    etl_parser = subparsers.add_parser('etl', help='ETL operations')
    etl_subparsers = etl_parser.add_subparsers(dest='etl_command')
    
    # Full ETL
    full_parser = etl_subparsers.add_parser('full', help='Run full ETL pipeline')
    full_parser.add_argument('--count', type=int, default=20, 
                           help='Number of random meals to load (default: 20)')
    
    # Incremental ETL
    inc_parser = etl_subparsers.add_parser('incremental', help='Run incremental ETL')
    inc_parser.add_argument('--count', type=int, default=5,
                          help='Number of meals to load (default: 5)')
    
    # Search ETL
    search_parser = etl_subparsers.add_parser('search', help='Search and load meals')
    search_parser.add_argument('term', help='Search term')
    search_parser.add_argument('--type', choices=['name', 'category', 'area', 'ingredient', 'letter'],
                             default='name', help='Search type (default: name)')
    
    # Database operations
    db_parser = subparsers.add_parser('db', help='Database operations')
    db_subparsers = db_parser.add_subparsers(dest='db_command')
    
    # Initialize schema
    db_subparsers.add_parser('init', help='Initialize database schema')
    
    # Show stats
    db_subparsers.add_parser('stats', help='Show database statistics')
    
    # Dashboard
    dashboard_parser = subparsers.add_parser('dashboard', help='Launch Streamlit dashboard')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        etl = MealETL()
        
        if args.command == 'etl':
            handle_etl_commands(etl, args)
        elif args.command == 'db':
            handle_db_commands(etl, args)
        elif args.command == 'dashboard':
            launch_dashboard()
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        if 'etl' in locals():
            etl.cleanup()

def handle_etl_commands(etl, args):
    """Handle ETL subcommands"""
    if args.etl_command == 'full':
        print(f"Running full ETL pipeline with {args.count} meals...")
        etl.db_manager.execute_schema()
        etl.run_full_etl(args.count)
        
    elif args.etl_command == 'incremental':
        print(f"Running incremental ETL with {args.count} meals...")
        etl.run_incremental_etl(args.count)
        
    elif args.etl_command == 'search':
        print(f"Searching for meals by {args.type}: {args.term}")
        etl.search_and_load_meals(args.term, args.type)
        
    else:
        print("Please specify an ETL command: full, incremental, or search")

def handle_db_commands(etl, args):
    """Handle database subcommands"""
    if args.db_command == 'init':
        print("Initializing database schema...")
        etl.db_manager.execute_schema()
        print("Database schema initialized successfully!")
        
    elif args.db_command == 'stats':
        show_database_stats(etl)
        
    else:
        print("Please specify a database command: init or stats")

def show_database_stats(etl):
    """Show database statistics"""
    try:
        meals_count = etl.db_manager.get_table_count('meals')
        ingredients_count = etl.db_manager.get_table_count('ingredients')
        categories_count = etl.db_manager.get_table_count('categories')
        areas_count = etl.db_manager.get_table_count('areas')
        
        print("\n" + "="*40)
        print("DATABASE STATISTICS")
        print("="*40)
        print(f"Meals:       {meals_count:,}")
        print(f"Ingredients: {ingredients_count:,}")
        print(f"Categories:  {categories_count:,}")
        print(f"Areas:       {areas_count:,}")
        print("="*40)
        
        # Show recent ETL logs
        logs = etl.db_manager.get_recent_etl_logs(5)
        if not logs.empty:
            print("\nRecent ETL Operations:")
            print("-" * 40)
            for _, log in logs.iterrows():
                status_icon = "✓" if log['status'] == 'SUCCESS' else "✗"
                print(f"{status_icon} {log['operation_type']} - {log['records_processed']} records - {log['created_at']}")
        
    except Exception as e:
        print(f"Failed to get database stats: {e}")

def launch_dashboard():
    """Launch Streamlit dashboard"""
    import subprocess
    import os
    
    dashboard_path = os.path.join(os.path.dirname(__file__), 'dashboard.py')
    
    try:
        print("Launching Streamlit dashboard...")
        subprocess.run(['streamlit', 'run', dashboard_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to launch dashboard: {e}")
        print("Make sure Streamlit is installed: pip install streamlit")
    except FileNotFoundError:
        print("Streamlit not found. Please install it: pip install streamlit")

if __name__ == "__main__":
    main()
