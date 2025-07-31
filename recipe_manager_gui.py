#!/usr/bin/env python3
"""
MealDB Recipe Manager - Modern GUI Application
User-friendly interface for managing your recipe database
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import requests
import threading
import os
from datetime import datetime

class RecipeManagerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🍽️ MealDB Recipe Manager")
        self.root.geometry("1200x800")
        
        # Modern color scheme
        self.colors = {
            'primary': '#2c3e50',      # Dark blue-gray
            'secondary': '#34495e',     # Slightly lighter blue-gray
            'accent': '#3498db',        # Bright blue
            'success': '#27ae60',       # Green
            'warning': '#f39c12',       # Orange
            'danger': '#e74c3c',        # Red
            'background': '#ecf0f1',    # Light gray
            'surface': '#ffffff',       # White
            'text': '#2c3e50',          # Dark text
            'text_light': '#7f8c8d',    # Light gray text
            'border': '#bdc3c7'         # Border gray
        }
        
        self.root.configure(bg=self.colors['background'])
        
        # Configure modern ttk style
        self.setup_styles()
        
        # Configure modern ttk style
        self.setup_styles()
        
        # Database path
        self.db_path = "mealdb_gui.db"
        self.setup_database()
        
        # Create GUI
        self.create_widgets()
        self.refresh_stats()
        self.load_recipes()
        
    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        
        # Configure button styles
        style.configure('Modern.TButton',
                       background=self.colors['accent'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10))
        
        style.map('Modern.TButton',
                 background=[('active', '#2980b9'),
                           ('pressed', '#1f5f8b')])
        
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(15, 8))
        
        style.map('Success.TButton',
                 background=[('active', '#229954'),
                           ('pressed', '#1e8449')])
        
        # Configure frame styles
        style.configure('Card.TFrame',
                       background=self.colors['surface'],
                       relief='flat',
                       borderwidth=1)
        
        # Configure label styles
        style.configure('Title.TLabel',
                       background=self.colors['background'],
                       foreground=self.colors['primary'],
                       font=('Segoe UI', 24, 'bold'))
        
        style.configure('Subtitle.TLabel',
                       background=self.colors['surface'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 12, 'bold'))
        
        style.configure('Stats.TLabel',
                       background=self.colors['surface'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 11))
        
        # Configure combobox styles
        style.configure('Modern.TCombobox',
                       fieldbackground=self.colors['surface'],
                       background=self.colors['surface'],
                       borderwidth=1,
                       relief='solid')
        
        # Configure labelframe styles
        style.configure('Modern.TLabelframe',
                       background=self.colors['background'],
                       foreground=self.colors['primary'],
                       borderwidth=2,
                       relief='flat')
        
        style.configure('Modern.TLabelframe.Label',
                       background=self.colors['background'],
                       foreground=self.colors['primary'],
                       font=('Segoe UI', 12, 'bold'))
        
    def setup_database(self):
        """Create SQLite database and tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create meals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS meals (
                id TEXT PRIMARY KEY,
                meal_name TEXT NOT NULL,
                category TEXT,
                area TEXT,
                instructions TEXT,
                meal_thumb TEXT,
                tags TEXT,
                youtube TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create ingredients table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                meal_id TEXT,
                ingredient_name TEXT,
                measurement TEXT,
                ingredient_order INTEGER,
                FOREIGN KEY (meal_id) REFERENCES meals(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def create_widgets(self):
        """Create all GUI widgets with modern styling"""
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.colors['background'])
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header section - made more compact
        header_frame = tk.Frame(main_container, bg=self.colors['background'])
        header_frame.pack(fill="x", pady=(0, 15))
        
        # Modern title with gradient effect - reduced height
        title_frame = tk.Frame(header_frame, bg=self.colors['primary'], height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🍽️ MealDB Recipe Manager",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors['primary'],
            fg='white',
            pady=15
        )
        title_label.pack()
        
        # Compact header info section
        info_container = tk.Frame(main_container, bg=self.colors['background'])
        info_container.pack(fill="x", pady=(0, 15))
        
        # Statistics cards - made more compact
        self.create_compact_stats_cards(info_container)
        
        # Control panel - made more compact
        self.create_compact_controls(info_container)
        
        # Recipe display area - now gets most of the space
        self.create_modern_recipe_area(main_container)
        
        # Modern status bar
        self.create_status_bar()
        
    def create_compact_stats_cards(self, parent):
        """Create compact statistics cards"""
        # Title
        stats_title = tk.Label(
            parent,
            text="📊 Database Overview",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['background'],
            fg=self.colors['primary']
        )
        stats_title.pack(anchor="w", pady=(0, 8))
        
        # Cards frame
        cards_frame = tk.Frame(parent, bg=self.colors['background'])
        cards_frame.pack(fill="x", pady=(0, 10))
        
        # Create 4 stat cards - more compact
        self.stat_cards = {}
        stats = [
            ("meals", "🍽️", "Meals", self.colors['accent']),
            ("ingredients", "🥕", "Ingredients", self.colors['success']),
            ("categories", "📂", "Categories", self.colors['warning']),
            ("cuisines", "🌍", "Cuisines", self.colors['danger'])
        ]
        
        for i, (key, icon, label, color) in enumerate(stats):
            card = self.create_compact_stat_card(cards_frame, icon, label, "0", color)
            card.grid(row=0, column=i, padx=8, sticky="ew")
            self.stat_cards[key] = card
            
        # Configure grid weights
        for i in range(4):
            cards_frame.grid_columnconfigure(i, weight=1)
            
    def create_compact_stat_card(self, parent, icon, title, value, color):
        """Create a compact statistics card"""
        card_frame = tk.Frame(
            parent,
            bg=self.colors['surface'],
            relief='solid',
            bd=1,
            padx=15,
            pady=10
        )
        
        # Horizontal layout for compact display
        content_frame = tk.Frame(card_frame, bg=self.colors['surface'])
        content_frame.pack(fill="x")
        
        # Icon
        icon_label = tk.Label(
            content_frame,
            text=icon,
            font=("Segoe UI", 16),
            bg=self.colors['surface'],
            fg=color
        )
        icon_label.pack(side="left", padx=(0, 10))
        
        # Value and title in vertical layout
        text_frame = tk.Frame(content_frame, bg=self.colors['surface'])
        text_frame.pack(side="left", fill="x", expand=True)
        
        # Value
        value_label = tk.Label(
            text_frame,
            text=value,
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['primary']
        )
        value_label.pack(anchor="w")
        
        # Title
        title_label = tk.Label(
            text_frame,
            text=title,
            font=("Segoe UI", 9),
            bg=self.colors['surface'],
            fg=self.colors['text_light']
        )
        title_label.pack(anchor="w")
        
        # Store labels for updating
        card_frame.value_label = value_label
        return card_frame
        
    def create_compact_controls(self, parent):
        """Create compact control panel"""
        # Control panel background - more compact
        control_panel = tk.Frame(
            parent,
            bg=self.colors['surface'],
            relief='solid',
            bd=1,
            padx=20,
            pady=12
        )
        control_panel.pack(fill="x", pady=(0, 15))
        
        # Title
        controls_title = tk.Label(
            control_panel,
            text="🎮 Recipe Controls",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['primary']
        )
        controls_title.pack(anchor="w", pady=(0, 10))
        
        # Single row layout for all controls
        controls_row = tk.Frame(control_panel, bg=self.colors['surface'])
        controls_row.pack(fill="x")
        
        # Pull recipes button
        self.pull_button = tk.Button(
            controls_row,
            text="🔄 Pull New Recipes",
            command=self.pull_more_recipes,
            bg=self.colors['accent'],
            fg='white',
            font=("Segoe UI", 10, "bold"),
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2'
        )
        self.pull_button.pack(side="left", padx=(0, 10))
        
        # Amount selector
        tk.Label(
            controls_row,
            text="Amount:",
            font=("Segoe UI", 9),
            bg=self.colors['surface'],
            fg=self.colors['text']
        ).pack(side="left", padx=(0, 5))
        
        self.amount_var = tk.StringVar(value="10")
        amount_spin = tk.Spinbox(
            controls_row,
            from_=1,
            to=50,
            textvariable=self.amount_var,
            width=6,
            font=("Segoe UI", 9),
            relief='solid',
            bd=1
        )
        amount_spin.pack(side="left", padx=(0, 15))
        
        # Refresh button
        refresh_button = tk.Button(
            controls_row,
            text="🔄 Refresh",
            command=self.refresh_all,
            bg=self.colors['success'],
            fg='white',
            font=("Segoe UI", 10, "bold"),
            relief='flat',
            padx=15,
            pady=8,
            cursor='hand2'
        )
        refresh_button.pack(side="left", padx=(0, 20))
        
        # Search
        tk.Label(
            controls_row,
            text="🔍 Search:",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['text']
        ).pack(side="left", padx=(0, 8))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_recipes)
        search_entry = tk.Entry(
            controls_row,
            textvariable=self.search_var,
            width=20,
            font=("Segoe UI", 9),
            relief='solid',
            bd=1,
            bg=self.colors['surface']
        )
        search_entry.pack(side="left", padx=(0, 15))
        
        # Category filter
        tk.Label(
            controls_row,
            text="Category:",
            font=("Segoe UI", 9),
            bg=self.colors['surface'],
            fg=self.colors['text']
        ).pack(side="left", padx=(0, 5))
        
        self.category_var = tk.StringVar(value="All")
        self.category_combo = ttk.Combobox(
            controls_row,
            textvariable=self.category_var,
            width=12,
            font=("Segoe UI", 8),
            style='Modern.TCombobox'
        )
        self.category_combo.pack(side="left", padx=(0, 10))
        self.category_combo.bind('<<ComboboxSelected>>', self.filter_recipes)
        
        # Cuisine filter
        tk.Label(
            controls_row,
            text="Cuisine:",
            font=("Segoe UI", 9),
            bg=self.colors['surface'],
            fg=self.colors['text']
        ).pack(side="left", padx=(0, 5))
        
        self.cuisine_var = tk.StringVar(value="All")
        self.cuisine_combo = ttk.Combobox(
            controls_row,
            textvariable=self.cuisine_var,
            width=12,
            font=("Segoe UI", 8),
            style='Modern.TCombobox'
        )
        self.cuisine_combo.pack(side="left")
        self.cuisine_combo.bind('<<ComboboxSelected>>', self.filter_recipes)
        
    def create_modern_recipe_area(self, parent):
        """Create modern recipe display area"""
        recipe_container = tk.Frame(parent, bg=self.colors['background'])
        recipe_container.pack(fill="both", expand=True)
        
        # Title
        recipe_title = tk.Label(
            recipe_container,
            text="🍽️ Your Recipe Collection",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['background'],
            fg=self.colors['primary']
        )
        recipe_title.pack(anchor="w", pady=(0, 10))
        
        # Main recipe area with modern styling
        recipe_frame = tk.Frame(
            recipe_container,
            bg=self.colors['surface'],
            relief='solid',
            bd=1
        )
        recipe_frame.pack(fill="both", expand=True)
        
        # Create paned window for split view
        paned = ttk.PanedWindow(recipe_frame, orient=tk.HORIZONTAL)
        paned.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Left panel - Recipe list
        left_panel = tk.Frame(paned, bg=self.colors['surface'])
        paned.add(left_panel, weight=1)
        
        # Recipe list header
        list_header = tk.Frame(left_panel, bg=self.colors['secondary'], height=40)
        list_header.pack(fill="x")
        list_header.pack_propagate(False)
        
        tk.Label(
            list_header,
            text="📋 Recipe List",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['secondary'],
            fg='white',
            pady=10
        ).pack()
        
        # Recipe listbox with modern styling
        listbox_frame = tk.Frame(left_panel, bg=self.colors['surface'])
        listbox_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Custom listbox styling
        self.recipe_listbox = tk.Listbox(
            listbox_frame,
            font=("Segoe UI", 10),
            bg=self.colors['surface'],
            fg=self.colors['text'],
            selectbackground=self.colors['accent'],
            selectforeground='white',
            relief='flat',
            bd=0,
            highlightthickness=0,
            activestyle='none'
        )
        
        # Modern scrollbar
        scrollbar = tk.Scrollbar(
            listbox_frame,
            orient="vertical",
            bg=self.colors['border'],
            troughcolor=self.colors['background'],
            borderwidth=0,
            width=12
        )
        
        self.recipe_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.recipe_listbox.yview)
        
        self.recipe_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.recipe_listbox.bind('<<ListboxSelect>>', self.show_recipe_details)
        
        # Right panel - Recipe details
        right_panel = tk.Frame(paned, bg=self.colors['surface'])
        paned.add(right_panel, weight=2)
        
        # Details header
        details_header = tk.Frame(right_panel, bg=self.colors['secondary'], height=40)
        details_header.pack(fill="x")
        details_header.pack_propagate(False)
        
        tk.Label(
            details_header,
            text="📖 Recipe Details",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['secondary'],
            fg='white',
            pady=10
        ).pack()
        
        # Recipe details with modern styling
        details_frame = tk.Frame(right_panel, bg=self.colors['surface'])
        details_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.details_text = scrolledtext.ScrolledText(
            details_frame,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            bg=self.colors['surface'],
            fg=self.colors['text'],
            relief='flat',
            bd=0,
            highlightthickness=0,
            selectbackground=self.colors['accent'],
            selectforeground='white'
        )
        self.details_text.pack(fill="both", expand=True)
        
    def create_status_bar(self):
        """Create modern status bar"""
        status_frame = tk.Frame(self.root, bg=self.colors['primary'], height=30)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            font=("Segoe UI", 9),
            bg=self.colors['primary'],
            fg='white',
            anchor=tk.W,
            padx=20,
            pady=5
        )
        self.status_label.pack(fill="both", expand=True)
        
    def pull_more_recipes(self):
        """Pull more recipes from API in background thread"""
        amount = int(self.amount_var.get())
        self.pull_button.config(
            state="disabled", 
            text="🔄 Pulling...",
            bg=self.colors['text_light']
        )
        self.status_label.config(text=f"Fetching {amount} recipes from API...")
        
        # Run in background thread to avoid freezing GUI
        thread = threading.Thread(target=self._fetch_recipes, args=(amount,))
        thread.daemon = True
        thread.start()
        
    def _fetch_recipes(self, amount):
        """Fetch recipes from API (background thread)"""
        try:
            recipes = []
            existing_ids = self.get_existing_meal_ids()
            
            attempts = 0
            max_attempts = amount * 3
            
            while len(recipes) < amount and attempts < max_attempts:
                attempts += 1
                try:
                    response = requests.get("https://www.themealdb.com/api/json/v1/1/random.php", timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        
                        if data and 'meals' in data and data['meals']:
                            meal = data['meals'][0]
                            meal_id = meal.get('idMeal')
                            
                            if meal_id not in existing_ids:
                                recipes.append(meal)
                                existing_ids.add(meal_id)
                                
                                # Update status
                                self.root.after(0, lambda: self.status_label.config(
                                    text=f"Found {len(recipes)}/{amount} new recipes..."
                                ))
                                
                except Exception as e:
                    print(f"Error fetching recipe: {e}")
                    
            # Save recipes to database
            saved_count = self.save_recipes(recipes)
            
            # Update GUI in main thread
            self.root.after(0, self._fetch_complete, saved_count)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to fetch recipes: {e}"))
            self.root.after(0, self._fetch_complete, 0)
            
    def _fetch_complete(self, saved_count):
        """Called when fetch is complete (main thread)"""
        self.pull_button.config(
            state="normal", 
            text="🔄 Pull New Recipes",
            bg=self.colors['accent']
        )
        self.status_label.config(text=f"Added {saved_count} new recipes!")
        
        # Refresh all data
        self.refresh_all()
        
        if saved_count > 0:
            messagebox.showinfo("Success", f"Successfully added {saved_count} new recipes!")
        else:
            messagebox.showwarning("No New Recipes", "No new unique recipes found. Try again later!")
            
    def get_existing_meal_ids(self):
        """Get existing meal IDs from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM meals')
        existing_ids = {row[0] for row in cursor.fetchall()}
        conn.close()
        return existing_ids
        
    def save_recipes(self, recipes):
        """Save recipes to database"""
        if not recipes:
            return 0
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        saved_count = 0
        
        for recipe in recipes:
            try:
                # Insert meal
                cursor.execute('''
                    INSERT OR REPLACE INTO meals 
                    (id, meal_name, category, area, instructions, meal_thumb, tags, youtube)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    recipe.get('idMeal'),
                    recipe.get('strMeal'),
                    recipe.get('strCategory'),
                    recipe.get('strArea'),
                    recipe.get('strInstructions'),
                    recipe.get('strMealThumb'),
                    recipe.get('strTags'),
                    recipe.get('strYoutube')
                ))
                
                # Insert ingredients
                ingredients = self.extract_ingredients(recipe)
                
                # Delete existing ingredients
                cursor.execute('DELETE FROM ingredients WHERE meal_id = ?', (recipe.get('idMeal'),))
                
                # Insert new ingredients
                for ingredient in ingredients:
                    cursor.execute('''
                        INSERT INTO ingredients (meal_id, ingredient_name, measurement, ingredient_order)
                        VALUES (?, ?, ?, ?)
                    ''', (
                        recipe.get('idMeal'),
                        ingredient['ingredient_name'],
                        ingredient['measurement'],
                        ingredient['ingredient_order']
                    ))
                
                saved_count += 1
                
            except Exception as e:
                print(f"Error saving recipe {recipe.get('strMeal', 'Unknown')}: {e}")
        
        conn.commit()
        conn.close()
        
        return saved_count
        
    def extract_ingredients(self, meal):
        """Extract ingredients from meal data"""
        ingredients = []
        
        for i in range(1, 21):
            ingredient = meal.get(f'strIngredient{i}', '').strip()
            measure = meal.get(f'strMeasure{i}', '').strip()
            
            if ingredient and ingredient.lower() not in ['', 'null', 'none']:
                ingredients.append({
                    'ingredient_name': ingredient,
                    'measurement': measure if measure else None,
                    'ingredient_order': i
                })
        
        return ingredients
        
    def refresh_stats(self):
        """Refresh database statistics with modern display"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM meals')
        meals_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM ingredients')
        ingredients_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT category) FROM meals WHERE category IS NOT NULL')
        categories_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT area) FROM meals WHERE area IS NOT NULL')
        cuisines_count = cursor.fetchone()[0]
        
        conn.close()
        
        # Update stat cards
        if hasattr(self, 'stat_cards'):
            self.stat_cards['meals'].value_label.config(text=str(meals_count))
            self.stat_cards['ingredients'].value_label.config(text=str(ingredients_count))
            self.stat_cards['categories'].value_label.config(text=str(categories_count))
            self.stat_cards['cuisines'].value_label.config(text=str(cuisines_count))
        
    def load_recipes(self):
        """Load recipes into listbox"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all recipes
        cursor.execute('''
            SELECT id, meal_name, category, area 
            FROM meals 
            ORDER BY meal_name
        ''')
        
        self.all_recipes = cursor.fetchall()
        
        # Load categories for filter
        cursor.execute('SELECT DISTINCT category FROM meals WHERE category IS NOT NULL ORDER BY category')
        categories = ["All"] + [row[0] for row in cursor.fetchall()]
        self.category_combo['values'] = categories
        
        # Load cuisines for filter
        cursor.execute('SELECT DISTINCT area FROM meals WHERE area IS NOT NULL ORDER BY area')
        cuisines = ["All"] + [row[0] for row in cursor.fetchall()]
        self.cuisine_combo['values'] = cuisines
        
        conn.close()
        
        # Display all recipes initially
        self.display_recipes(self.all_recipes)
        
    def display_recipes(self, recipes):
        """Display recipes in listbox with modern formatting"""
        self.recipe_listbox.delete(0, tk.END)
        
        for recipe_id, name, category, area in recipes:
            # Format with nice icons and spacing
            category_display = category or 'Unknown'
            area_display = area or 'Unknown'
            display_text = f"🍽️ {name}   •   📂 {category_display}   •   🌍 {area_display}"
            self.recipe_listbox.insert(tk.END, display_text)
            
        # Store current recipes for selection
        self.current_recipes = recipes
        
    def filter_recipes(self, *args):
        """Filter recipes based on search and category/cuisine"""
        search_text = self.search_var.get().lower()
        selected_category = self.category_var.get()
        selected_cuisine = self.cuisine_var.get()
        
        filtered_recipes = []
        
        for recipe in self.all_recipes:
            recipe_id, name, category, area = recipe
            
            # Check search text
            if search_text and search_text not in name.lower():
                continue
                
            # Check category filter
            if selected_category != "All" and category != selected_category:
                continue
                
            # Check cuisine filter
            if selected_cuisine != "All" and area != selected_cuisine:
                continue
                
            filtered_recipes.append(recipe)
            
        self.display_recipes(filtered_recipes)
        
    def show_recipe_details(self, event):
        """Show detailed recipe information with modern formatting"""
        selection = self.recipe_listbox.curselection()
        if not selection:
            return
            
        index = selection[0]
        if index >= len(self.current_recipes):
            return
            
        recipe_id = self.current_recipes[index][0]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get meal details
        cursor.execute('''
            SELECT meal_name, category, area, instructions, meal_thumb, tags, youtube
            FROM meals 
            WHERE id = ?
        ''', (recipe_id,))
        
        meal_details = cursor.fetchone()
        
        if meal_details:
            name, category, area, instructions, thumb, tags, youtube = meal_details
            
            # Get ingredients
            cursor.execute('''
                SELECT ingredient_name, measurement
                FROM ingredients 
                WHERE meal_id = ?
                ORDER BY ingredient_order
            ''', (recipe_id,))
            
            ingredients = cursor.fetchall()
            
            # Format details with modern styling
            details = f"🍽️ {name}\n"
            details += "═" * (len(name) + 4) + "\n\n"
            
            # Info section with modern icons
            details += "📋 RECIPE INFO\n"
            details += "─" * 30 + "\n"
            details += f"📂 Category: {category or 'N/A'}\n"
            details += f"🌍 Cuisine: {area or 'N/A'}\n"
            
            if tags:
                details += f"🏷️  Tags: {tags}\n"
                
            if youtube:
                details += f"📺 Video: {youtube}\n"
                
            if thumb:
                details += f"🖼️  Image: {thumb}\n"
                
            # Ingredients section
            details += f"\n🥕 INGREDIENTS ({len(ingredients)} items)\n"
            details += "─" * 30 + "\n"
            
            for i, (ingredient, measure) in enumerate(ingredients, 1):
                bullet = "•" if i % 2 == 1 else "◦"
                if measure and measure.strip():
                    details += f"{bullet} {measure} {ingredient}\n"
                else:
                    details += f"{bullet} {ingredient}\n"
                    
            # Instructions section
            if instructions and instructions.strip():
                details += f"\n👨‍🍳 COOKING INSTRUCTIONS\n"
                details += "─" * 30 + "\n"
                
                # Format instructions with better spacing
                formatted_instructions = instructions.replace('. ', '.\n\n')
                details += formatted_instructions
                
            # Display in text area
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(1.0, details)
            
            # Configure text tags for better formatting
            self.details_text.tag_configure("title", font=("Segoe UI", 14, "bold"), foreground=self.colors['primary'])
            self.details_text.tag_configure("section", font=("Segoe UI", 11, "bold"), foreground=self.colors['accent'])
            
        conn.close()
        
    def refresh_all(self):
        """Refresh all data"""
        self.refresh_stats()
        self.load_recipes()
        self.status_label.config(text="Data refreshed")
        
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

def main():
    """Main function"""
    try:
        app = RecipeManagerGUI()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
