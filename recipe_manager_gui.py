#!/usr/bin/env python3
"""
MealDB Recipe Manager - Ultra Modern GUI Application
Advanced interface with animations, images, and smart cooking suggestions
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import requests
import threading
import os
import random
import time
from datetime import datetime
from PIL import Image, ImageTk, ImageOps, ImageDraw, ImageFilter
from io import BytesIO
import urllib.request
import urllib.error

class RecipeManagerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🍽️ MealDB Recipe Manager - Ultra Modern Edition")
        self.root.geometry("1400x900")
        self.root.state('zoomed')  # Maximize window
        
        # Modern gradient color scheme
        self.colors = {
            'primary': '#1e3a8a',        # Deep blue
            'primary_light': '#3b82f6',   # Bright blue
            'secondary': '#1f2937',       # Dark gray
            'accent': '#f59e0b',          # Warm amber
            'accent_light': '#fbbf24',    # Light amber
            'success': '#10b981',         # Emerald green
            'warning': '#f59e0b',         # Orange
            'danger': '#ef4444',          # Red
            'background': '#f8fafc',      # Very light blue-gray
            'surface': '#ffffff',         # Pure white
            'surface_dark': '#f1f5f9',    # Light gray
            'text': '#1e293b',            # Dark slate
            'text_light': '#64748b',      # Slate gray
            'text_muted': '#94a3b8',      # Light slate
            'border': '#e2e8f0',          # Light border
            'shadow': '#0f172a20',        # Transparent black
            'gradient_start': '#667eea',   # Purple-blue
            'gradient_end': '#764ba2'      # Purple
        }
        
        self.root.configure(bg=self.colors['background'])
        
        # Animation variables
        self.animation_frame = 0
        self.suggestion_animation = False
        self.current_suggestion = None
        self.image_cache = {}
        self.placeholder_image = None
        
        # Configure modern ttk style
        self.setup_advanced_styles()
        
        # Database path
        self.db_path = "mealdb_gui.db"
        self.setup_database()
        
        # Create placeholder image
        self.create_placeholder_image()
        
        # Create enhanced GUI
        self.create_enhanced_widgets()
        self.refresh_stats()
        self.load_recipes()
        
        # Start animation loop
        self.animate()
        
    def create_placeholder_image(self):
        """Create a beautiful placeholder image for recipes without images"""
        try:
            # Create a gradient placeholder
            size = (200, 150)
            image = Image.new('RGB', size, color=self.colors['surface_dark'])
            
            # Create gradient effect
            for y in range(size[1]):
                for x in range(size[0]):
                    # Create a radial gradient
                    center_x, center_y = size[0] // 2, size[1] // 2
                    distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                    max_distance = (center_x ** 2 + center_y ** 2) ** 0.5
                    
                    # Gradient from center to edge
                    ratio = min(distance / max_distance, 1)
                    r = int(59 + ratio * 40)   # Light gray to darker gray
                    g = int(130 + ratio * 40)
                    b = int(246 - ratio * 60)
                    
                    image.putpixel((x, y), (r, g, b))
            
            # Add cooking emoji overlay
            draw = ImageDraw.Draw(image)
            
            # Draw a circle for the emoji background
            center = (size[0] // 2, size[1] // 2)
            radius = 30
            draw.ellipse([center[0] - radius, center[1] - radius, 
                         center[0] + radius, center[1] + radius], 
                        fill=(255, 255, 255, 200))
            
            self.placeholder_image = ImageTk.PhotoImage(image)
            
        except Exception as e:
            print(f"Error creating placeholder image: {e}")
            # Create simple colored rectangle as fallback
            image = Image.new('RGB', (200, 150), color='#e2e8f0')
            self.placeholder_image = ImageTk.PhotoImage(image)
        
    def setup_advanced_styles(self):
        """Configure ultra-modern ttk styles with animations"""
        style = ttk.Style()
        
        # Configure modern button styles with hover effects
        style.configure('Ultra.TButton',
                       background=self.colors['primary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(25, 12),
                       font=('Segoe UI', 10, 'bold'))
        
        style.map('Ultra.TButton',
                 background=[('active', self.colors['primary_light']),
                           ('pressed', self.colors['secondary'])])
        
        style.configure('Accent.TButton',
                       background=self.colors['accent'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10),
                       font=('Segoe UI', 10, 'bold'))
        
        style.map('Accent.TButton',
                 background=[('active', self.colors['accent_light']),
                           ('pressed', '#d97706')])
        
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10),
                       font=('Segoe UI', 10, 'bold'))
        
        style.map('Success.TButton',
                 background=[('active', '#059669'),
                           ('pressed', '#047857')])
        
        # Configure frame styles with modern borders
        style.configure('Glass.TFrame',
                       background=self.colors['surface'],
                       relief='flat',
                       borderwidth=0)
        
        style.configure('Card.TFrame',
                       background=self.colors['surface'],
                       relief='flat',
                       borderwidth=1,
                       bordercolor=self.colors['border'])
        
        # Configure label styles with modern typography
        style.configure('Hero.TLabel',
                       background=self.colors['background'],
                       foreground=self.colors['primary'],
                       font=('Segoe UI', 28, 'bold'))
        
        style.configure('Title.TLabel',
                       background=self.colors['surface'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 16, 'bold'))
        
        style.configure('Subtitle.TLabel',
                       background=self.colors['surface'],
                       foreground=self.colors['text_light'],
                       font=('Segoe UI', 12))
        
        style.configure('Stats.TLabel',
                       background=self.colors['surface'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 14, 'bold'))
        
        style.configure('Caption.TLabel',
                       background=self.colors['surface'],
                       foreground=self.colors['text_muted'],
                       font=('Segoe UI', 9))
        
        # Configure modern combobox styles
        style.configure('Ultra.TCombobox',
                       fieldbackground=self.colors['surface'],
                       background=self.colors['surface'],
                       borderwidth=1,
                       relief='solid',
                       bordercolor=self.colors['border'],
                       padding=10)
        
        # Configure modern progressbar
        style.configure('Ultra.Horizontal.TProgressbar',
                       background=self.colors['accent'],
                       troughcolor=self.colors['surface_dark'],
                       borderwidth=0,
                       lightcolor=self.colors['accent'],
                       darkcolor=self.colors['accent'])
        
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
        
    def create_enhanced_widgets(self):
        """Create ultra-modern GUI with animations and advanced features"""
        # Create main scrollable canvas
        self.main_canvas = tk.Canvas(self.root, bg=self.colors['background'], highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview,
                                     bg=self.colors['border'], troughcolor=self.colors['surface_dark'])
        self.scrollable_frame = tk.Frame(self.main_canvas, bg=self.colors['background'])
        
        # Configure scrollable frame to update scroll region
        def configure_scroll_region(event):
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        
        def configure_canvas_width(event):
            # Update the scrollable frame width to match canvas width
            canvas_width = event.width
            self.main_canvas.itemconfig(self.canvas_window, width=canvas_width)
        
        self.scrollable_frame.bind("<Configure>", configure_scroll_region)
        self.main_canvas.bind("<Configure>", configure_canvas_width)
        
        # Create window with proper expansion
        self.canvas_window = self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Hero header section with gradient effect
        self.create_hero_header()
        
        # Smart cooking suggestion panel
        self.create_suggestion_panel()
        
        # Modern statistics cards with animations
        self.create_animated_stats_cards()
        
        # Advanced control panel with filters
        self.create_advanced_controls()
        
        # Recipe gallery with image previews
        self.create_recipe_gallery()
        
        # Enhanced status bar with animations
        self.create_animated_status_bar()
        
        # Bind mouse wheel to canvas
        self.bind_mousewheel()
        
    def create_hero_header(self):
        """Create animated hero header"""
        hero_frame = tk.Frame(self.scrollable_frame, bg=self.colors['primary'], height=120)
        hero_frame.pack(fill="x", padx=0, pady=0)
        hero_frame.pack_propagate(False)
        
        # Hero content
        hero_content = tk.Frame(hero_frame, bg=self.colors['primary'])
        hero_content.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Main title container
        title_container = tk.Frame(hero_content, bg=self.colors['primary'])
        title_container.pack(fill="x")
        
        # Animated title
        self.hero_title = tk.Label(
            title_container,
            text="🍽️ Ultra Modern Recipe Manager",
            font=("Segoe UI", 28, "bold"),
            bg=self.colors['primary'],
            fg='white',
            anchor="w"
        )
        self.hero_title.pack(side="left")
        
        # Subtitle with current time
        current_time = datetime.now().strftime("%A, %B %d, %Y")
        self.hero_subtitle = tk.Label(
            hero_content,
            text=f"✨ Discover amazing recipes • {current_time}",
            font=("Segoe UI", 14),
            bg=self.colors['primary'],
            fg='white',
            anchor="w"
        )
        self.hero_subtitle.pack(anchor="w", pady=(5, 0))
        
        
    def create_suggestion_panel(self):
        """Create smart cooking suggestion panel with animations"""
        suggestion_frame = tk.Frame(self.scrollable_frame, bg=self.colors['surface'], 
                                   relief='solid', bd=1, padx=30, pady=20)
        suggestion_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # Header with animation
        header_frame = tk.Frame(suggestion_frame, bg=self.colors['surface'])
        header_frame.pack(fill="x", pady=(0, 15))
        
        self.suggestion_title = tk.Label(
            header_frame,
            text="🎯 Smart Cooking Suggestion",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['primary']
        )
        self.suggestion_title.pack(side="left")
        
        # Animated refresh button
        self.refresh_suggestion_btn = tk.Button(
            header_frame,
            text="🔄",
            command=self.animate_suggestion_refresh,
            bg=self.colors['accent'],
            fg='white',
            font=("Segoe UI", 12, "bold"),
            relief='flat',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        self.refresh_suggestion_btn.pack(side="right")
        
        # Suggestion content area
        self.suggestion_content = tk.Frame(suggestion_frame, bg=self.colors['surface'])
        self.suggestion_content.pack(fill="x")
        
        # Initialize with first suggestion
        self.update_cooking_suggestion()
        
    def create_animated_stats_cards(self):
        """Create animated statistics cards"""
        stats_frame = tk.Frame(self.scrollable_frame, bg=self.colors['background'])
        stats_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # Stats title
        stats_title = tk.Label(
            stats_frame,
            text="📊 Database Analytics",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors['background'],
            fg=self.colors['primary']
        )
        stats_title.pack(anchor="w", pady=(0, 15))
        
        # Cards container
        cards_container = tk.Frame(stats_frame, bg=self.colors['background'])
        cards_container.pack(fill="x")
        
        # Create animated stat cards
        self.stat_cards = {}
        stats = [
            ("meals", "🍽️", "Total Recipes", "0", self.colors['primary']),
            ("ingredients", "🥕", "Ingredients", "0", self.colors['success']),
            ("categories", "📂", "Categories", "0", self.colors['accent']),
            ("cuisines", "🌍", "Cuisines", "0", self.colors['danger']),
            ("recent", "⏰", "Added Today", "0", self.colors['secondary'])
        ]
        
        for i, (key, icon, label, value, color) in enumerate(stats):
            card = self.create_animated_stat_card(cards_container, icon, label, value, color)
            card.grid(row=0, column=i, padx=8, sticky="ew")
            self.stat_cards[key] = card
            
        # Configure grid weights
        for i in range(len(stats)):
            cards_container.grid_columnconfigure(i, weight=1)
            
    def create_animated_stat_card(self, parent, icon, title, value, color):
        """Create an animated statistics card"""
        card_frame = tk.Frame(
            parent,
            bg=self.colors['surface'],
            relief='solid',
            bd=1,
            padx=20,
            pady=15
        )
        
        # Icon with color background
        icon_frame = tk.Frame(card_frame, bg=color, width=50, height=50)
        icon_frame.pack_propagate(False)
        icon_frame.pack(pady=(0, 10))
        
        icon_label = tk.Label(
            icon_frame,
            text=icon,
            font=("Segoe UI", 18),
            bg=color,
            fg='white'
        )
        icon_label.pack(expand=True)
        
        # Animated value
        value_label = tk.Label(
            card_frame,
            text=value,
            font=("Segoe UI", 24, "bold"),
            bg=self.colors['surface'],
            fg=color
        )
        value_label.pack()
        
        # Title
        title_label = tk.Label(
            card_frame,
            text=title,
            font=("Segoe UI", 10),
            bg=self.colors['surface'],
            fg=self.colors['text_light']
        )
        title_label.pack()
        
        # Store labels for updating
        card_frame.value_label = value_label
        card_frame.color = color
        return card_frame
        
    def create_advanced_controls(self):
        """Create advanced control panel with modern filters"""
        controls_frame = tk.Frame(self.scrollable_frame, bg=self.colors['surface'], 
                                 relief='solid', bd=1, padx=30, pady=20)
        controls_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # Controls title
        controls_title = tk.Label(
            controls_frame,
            text="🎮 Advanced Controls & Filters",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['primary']
        )
        controls_title.pack(anchor="w", pady=(0, 20))
        
        # Create tabbed interface for controls
        self.create_control_tabs(controls_frame)
        
    def create_control_tabs(self, parent):
        """Create tabbed control interface"""
        notebook = ttk.Notebook(parent)
        notebook.pack(fill="x")
        
        # Tab 1: Recipe Management
        recipe_tab = tk.Frame(notebook, bg=self.colors['surface'])
        notebook.add(recipe_tab, text="📥 Recipe Management")
        
        self.create_recipe_management_tab(recipe_tab)
        
        # Tab 2: Search & Filter
        search_tab = tk.Frame(notebook, bg=self.colors['surface'])
        notebook.add(search_tab, text="🔍 Search & Filter")
        
        self.create_search_filter_tab(search_tab)
        
        # Tab 3: Cuisine Explorer
        cuisine_tab = tk.Frame(notebook, bg=self.colors['surface'])
        notebook.add(cuisine_tab, text="🌍 Cuisine Explorer")
        
        self.create_cuisine_explorer_tab(cuisine_tab)
        
    def create_recipe_management_tab(self, parent):
        """Create recipe management controls"""
        management_frame = tk.Frame(parent, bg=self.colors['surface'])
        management_frame.pack(fill="x", padx=20, pady=15)
        
        # Pull recipes section
        pull_frame = tk.Frame(management_frame, bg=self.colors['surface'])
        pull_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(
            pull_frame,
            text="🔄 Pull New Recipes:",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['text']
        ).pack(side="left", padx=(0, 15))
        
        # Amount selector with modern styling
        tk.Label(
            pull_frame,
            text="Amount:",
            font=("Segoe UI", 10),
            bg=self.colors['surface'],
            fg=self.colors['text_light']
        ).pack(side="left", padx=(0, 5))
        
        self.amount_var = tk.StringVar(value="10")
        amount_spin = tk.Spinbox(
            pull_frame,
            from_=1,
            to=100,
            textvariable=self.amount_var,
            width=8,
            font=("Segoe UI", 10),
            relief='solid',
            bd=1,
            bg=self.colors['surface']
        )
        amount_spin.pack(side="left", padx=(0, 15))
        
        # Pull button with progress bar
        self.pull_button = tk.Button(
            pull_frame,
            text="🚀 Pull Recipes",
            command=self.pull_more_recipes,
            bg=self.colors['primary'],
            fg='white',
            font=("Segoe UI", 11, "bold"),
            relief='flat',
            bd=0,
            padx=25,
            pady=10,
            cursor='hand2'
        )
        self.pull_button.pack(side="left", padx=(0, 20))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            pull_frame,
            variable=self.progress_var,
            maximum=100,
            length=200,
            style='Ultra.Horizontal.TProgressbar'
        )
        self.progress_bar.pack(side="left")
        
    def create_search_filter_tab(self, parent):
        """Create search and filter controls"""
        search_frame = tk.Frame(parent, bg=self.colors['surface'])
        search_frame.pack(fill="x", padx=20, pady=15)
        
        # Search section
        search_section = tk.Frame(search_frame, bg=self.colors['surface'])
        search_section.pack(fill="x", pady=(0, 15))
        
        tk.Label(
            search_section,
            text="🔍 Smart Search:",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['text']
        ).pack(anchor="w", pady=(0, 8))
        
        # Search entry with modern styling
        search_container = tk.Frame(search_section, bg=self.colors['surface'])
        search_container.pack(fill="x")
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_recipes)
        
        search_entry = tk.Entry(
            search_container,
            textvariable=self.search_var,
            font=("Segoe UI", 12),
            relief='solid',
            bd=1,
            bg=self.colors['surface'],
            fg=self.colors['text'],
            insertbackground=self.colors['primary'],
            selectbackground=self.colors['accent']
        )
        search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Clear search button
        clear_btn = tk.Button(
            search_container,
            text="✖",
            command=lambda: self.search_var.set(""),
            bg=self.colors['text_light'],
            fg='white',
            font=("Segoe UI", 10),
            relief='flat',
            bd=0,
            padx=10,
            pady=8,
            cursor='hand2'
        )
        clear_btn.pack(side="right")
        
        # Filter section
        filter_section = tk.Frame(search_frame, bg=self.colors['surface'])
        filter_section.pack(fill="x")
        
        # Category filter
        category_frame = tk.Frame(filter_section, bg=self.colors['surface'])
        category_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        tk.Label(
            category_frame,
            text="📂 Category:",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['text']
        ).pack(anchor="w")
        
        self.category_var = tk.StringVar(value="All Categories")
        self.category_combo = ttk.Combobox(
            category_frame,
            textvariable=self.category_var,
            font=("Segoe UI", 10),
            style='Ultra.TCombobox',
            state="readonly"
        )
        self.category_combo.pack(fill="x", pady=(5, 0))
        self.category_combo.bind('<<ComboboxSelected>>', self.filter_recipes)
        
        # Cuisine filter
        cuisine_frame = tk.Frame(filter_section, bg=self.colors['surface'])
        cuisine_frame.pack(side="left", fill="x", expand=True)
        
        tk.Label(
            cuisine_frame,
            text="🌍 Cuisine:",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['text']
        ).pack(anchor="w")
        
        self.cuisine_var = tk.StringVar(value="All Cuisines")
        self.cuisine_combo = ttk.Combobox(
            cuisine_frame,
            textvariable=self.cuisine_var,
            font=("Segoe UI", 10),
            style='Ultra.TCombobox',
            state="readonly"
        )
        self.cuisine_combo.pack(fill="x", pady=(5, 0))
        self.cuisine_combo.bind('<<ComboboxSelected>>', self.filter_recipes)
        
    def create_cuisine_explorer_tab(self, parent):
        """Create cuisine exploration controls"""
        explorer_frame = tk.Frame(parent, bg=self.colors['surface'])
        explorer_frame.pack(fill="x", padx=20, pady=15)
        
        # Cuisine shuffle section
        shuffle_section = tk.Frame(explorer_frame, bg=self.colors['surface'])
        shuffle_section.pack(fill="x")
        
        tk.Label(
            shuffle_section,
            text="🎲 Cuisine Adventure:",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['text']
        ).pack(anchor="w", pady=(0, 10))
        
        # Cuisine buttons
        cuisine_buttons_frame = tk.Frame(shuffle_section, bg=self.colors['surface'])
        cuisine_buttons_frame.pack(fill="x")
        
        cuisines = [
            ("🇮🇹 Italian", "Italian"),
            ("🇨🇳 Chinese", "Chinese"),
            ("🇮🇳 Indian", "Indian"),
            ("🇲🇽 Mexican", "Mexican"),
            ("🇫🇷 French", "French"),
            ("🇯🇵 Japanese", "Japanese"),
            ("🇹🇭 Thai", "Thai"),
            ("🎲 Random", "Random")
        ]
        
        for i, (text, cuisine) in enumerate(cuisines):
            btn = tk.Button(
                cuisine_buttons_frame,
                text=text,
                command=lambda c=cuisine: self.explore_cuisine(c),
                bg=self.colors['accent'],
                fg='white',
                font=("Segoe UI", 9, "bold"),
                relief='flat',
                bd=0,
                padx=15,
                pady=8,
                cursor='hand2'
            )
            btn.grid(row=i//4, column=i%4, padx=5, pady=5, sticky="ew")
            
        # Configure grid weights
        for j in range(4):
            cuisine_buttons_frame.grid_columnconfigure(j, weight=1)
            
    def create_recipe_gallery(self):
        """Create modern recipe gallery with image previews"""
        gallery_frame = tk.Frame(self.scrollable_frame, bg=self.colors['surface'], 
                                relief='solid', bd=1, padx=30, pady=20)
        gallery_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        # Gallery title
        gallery_title = tk.Label(
            gallery_frame,
            text="🖼️ Recipe Gallery",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['primary']
        )
        gallery_title.pack(anchor="w", pady=(0, 15))
        
        # View mode selector
        view_frame = tk.Frame(gallery_frame, bg=self.colors['surface'])
        view_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(
            view_frame,
            text="View Mode:",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['text']
        ).pack(side="left", padx=(0, 10))
        
        self.view_mode = tk.StringVar(value="Gallery")
        view_modes = ["Gallery", "List", "Cards"]
        
        for mode in view_modes:
            btn = tk.Radiobutton(
                view_frame,
                text=mode,
                variable=self.view_mode,
                value=mode,
                command=self.change_view_mode,
                bg=self.colors['surface'],
                fg=self.colors['text'],
                selectcolor=self.colors['accent'],
                font=("Segoe UI", 10),
                cursor='hand2'
            )
            btn.pack(side="left", padx=(0, 15))
        
        # Main gallery container - simplified without nested canvas
        self.gallery_container = tk.Frame(gallery_frame, bg=self.colors['surface'])
        self.gallery_container.pack(fill="both", expand=True)
        
        # Direct recipe display area
        self.gallery_scrollable = tk.Frame(self.gallery_container, bg=self.colors['surface'])
        self.gallery_scrollable.pack(fill="both", expand=True)
        
        # Initialize gallery
        self.display_gallery_mode()
        
    def create_gallery_view(self):
        """Create the main gallery view with recipe cards"""
        # Clear existing content
        for widget in self.gallery_container.winfo_children():
            widget.destroy()
            
        # Create scrollable gallery with proper width expansion
        gallery_canvas = tk.Canvas(self.gallery_container, bg=self.colors['surface'], 
                                  highlightthickness=0, height=400)
        gallery_scrollbar = tk.Scrollbar(self.gallery_container, orient="vertical", 
                                        command=gallery_canvas.yview)
        self.gallery_scrollable = tk.Frame(gallery_canvas, bg=self.colors['surface'])
        
        # Configure proper expansion for gallery canvas
        def configure_gallery_scroll(event):
            gallery_canvas.configure(scrollregion=gallery_canvas.bbox("all"))
        
        def configure_gallery_width(event):
            # Update the scrollable frame width to match canvas width
            canvas_width = event.width
            gallery_canvas.itemconfig(gallery_window, width=canvas_width)
        
        self.gallery_scrollable.bind("<Configure>", configure_gallery_scroll)
        gallery_canvas.bind("<Configure>", configure_gallery_width)
        
        gallery_window = gallery_canvas.create_window((0, 0), window=self.gallery_scrollable, anchor="nw")
        gallery_canvas.configure(yscrollcommand=gallery_scrollbar.set)
        
        gallery_canvas.pack(side="left", fill="both", expand=True)
        gallery_scrollbar.pack(side="right", fill="y")
        
        # Store references
        self.gallery_canvas = gallery_canvas
        self.gallery_scrollbar = gallery_scrollbar
        
    def create_recipe_card(self, parent, recipe_data, row, col):
        """Create a modern recipe card with image"""
        recipe_id, name, category, area = recipe_data
        
        # Card frame with shadow effect
        card_frame = tk.Frame(
            parent,
            bg=self.colors['surface'],
            relief='solid',
            bd=1,
            padx=15,
            pady=15
        )
        card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Image section
        image_frame = tk.Frame(card_frame, bg=self.colors['surface_dark'], 
                              width=200, height=150)
        image_frame.pack_propagate(False)
        image_frame.pack(pady=(0, 10))
        
        # Load recipe image
        self.load_recipe_image(image_frame, recipe_id)
        
        # Recipe info section
        info_frame = tk.Frame(card_frame, bg=self.colors['surface'])
        info_frame.pack(fill="x")
        
        # Recipe name
        name_label = tk.Label(
            info_frame,
            text=name,
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['text'],
            wraplength=180
        )
        name_label.pack(anchor="w")
        
        # Category and cuisine
        details_frame = tk.Frame(info_frame, bg=self.colors['surface'])
        details_frame.pack(fill="x", pady=(5, 0))
        
        if category:
            category_label = tk.Label(
                details_frame,
                text=f"📂 {category}",
                font=("Segoe UI", 9),
                bg=self.colors['surface'],
                fg=self.colors['text_light']
            )
            category_label.pack(anchor="w")
            
        if area:
            area_label = tk.Label(
                details_frame,
                text=f"🌍 {area}",
                font=("Segoe UI", 9),
                bg=self.colors['surface'],
                fg=self.colors['text_light']
            )
            area_label.pack(anchor="w")
        
        # Action buttons
        actions_frame = tk.Frame(info_frame, bg=self.colors['surface'])
        actions_frame.pack(fill="x", pady=(10, 0))
        
        view_btn = tk.Button(
            actions_frame,
            text="👁️ View",
            command=lambda: self.show_recipe_details_popup(recipe_id),
            bg=self.colors['primary'],
            fg='white',
            font=("Segoe UI", 9, "bold"),
            relief='flat',
            bd=0,
            padx=15,
            pady=6,
            cursor='hand2'
        )
        view_btn.pack(side="left", padx=(0, 5))
        
        cook_btn = tk.Button(
            actions_frame,
            text="👨‍🍳 Cook",
            command=lambda: self.start_cooking_mode(recipe_id),
            bg=self.colors['success'],
            fg='white',
            font=("Segoe UI", 9, "bold"),
            relief='flat',
            bd=0,
            padx=15,
            pady=6,
            cursor='hand2'
        )
        cook_btn.pack(side="right")
        
        # Add hover effects
        def on_card_hover(e):
            card_frame.config(bg=self.colors['surface_dark'])
            
        def on_card_leave(e):
            card_frame.config(bg=self.colors['surface'])
            
        card_frame.bind("<Enter>", on_card_hover)
        card_frame.bind("<Leave>", on_card_leave)
        
        return card_frame
        
    def load_recipe_image(self, image_frame, recipe_id):
        """Load recipe image asynchronously"""
        # Check cache first
        if recipe_id in self.image_cache:
            self.display_image(image_frame, self.image_cache[recipe_id])
            return
            
        # Display placeholder while loading
        placeholder_label = tk.Label(
            image_frame,
            image=self.placeholder_image,
            bg=self.colors['surface_dark']
        )
        placeholder_label.pack(expand=True)
        
        # Load actual image in thread
        thread = threading.Thread(target=self._load_image_async, 
                                args=(image_frame, recipe_id, placeholder_label))
        thread.daemon = True
        thread.start()
        
    def _load_image_async(self, image_frame, recipe_id, placeholder_label):
        """Load image asynchronously"""
        try:
            # Get image URL from database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT meal_thumb FROM meals WHERE id = ?', (recipe_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result and result[0]:
                image_url = result[0]
                
                # Download and process image
                response = urllib.request.urlopen(image_url, timeout=10)
                image_data = response.read()
                
                # Process image
                pil_image = Image.open(BytesIO(image_data))
                pil_image = pil_image.resize((200, 150), Image.Resampling.LANCZOS)
                
                # Add rounded corners
                pil_image = self.add_rounded_corners(pil_image, 10)
                
                # Convert to PhotoImage
                tk_image = ImageTk.PhotoImage(pil_image)
                
                # Cache the image
                self.image_cache[recipe_id] = tk_image
                
                # Update UI in main thread
                self.root.after(0, lambda: self.display_image(image_frame, tk_image, placeholder_label))
                
        except Exception as e:
            print(f"Error loading image for recipe {recipe_id}: {e}")
            # Keep placeholder on error
            
    def add_rounded_corners(self, image, radius):
        """Add rounded corners to image"""
        # Create mask for rounded corners
        mask = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0) + image.size, radius, fill=255)
        
        # Apply mask
        result = Image.new('RGBA', image.size, (0, 0, 0, 0))
        result.paste(image, (0, 0))
        result.putalpha(mask)
        
        return result
        
    def display_image(self, image_frame, tk_image, placeholder_label=None):
        """Display image in frame"""
        if placeholder_label:
            placeholder_label.destroy()
            
        image_label = tk.Label(
            image_frame,
            image=tk_image,
            bg=self.colors['surface_dark']
        )
        image_label.pack(expand=True)
        
        # Keep reference to prevent garbage collection
        image_label.image = tk_image
        
    def create_animated_status_bar(self):
        """Create animated status bar"""
        status_frame = tk.Frame(self.root, bg=self.colors['primary'], height=35)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        status_frame.pack_propagate(False)
        
        # Left side - status text
        self.status_label = tk.Label(
            status_frame,
            text="✨ Ready to cook amazing meals!",
            font=("Segoe UI", 10),
            bg=self.colors['primary'],
            fg='white',
            anchor=tk.W,
            padx=20,
            pady=8
        )
        self.status_label.pack(side="left", fill="both", expand=True)
        
        # Right side - animated indicators
        indicators_frame = tk.Frame(status_frame, bg=self.colors['primary'])
        indicators_frame.pack(side="right", padx=20)
        
        # Connection status
        self.connection_indicator = tk.Label(
            indicators_frame,
            text="🟢 Connected",
            font=("Segoe UI", 9),
            bg=self.colors['primary'],
            fg='white'
        )
        self.connection_indicator.pack(side="right", padx=(0, 15))
        
        # Loading indicator
        self.loading_indicator = tk.Label(
            indicators_frame,
            text="",
            font=("Segoe UI", 12),
            bg=self.colors['primary'],
            fg='white'
        )
        self.loading_indicator.pack(side="right", padx=(0, 10))
        
    def bind_mousewheel(self):
        """Bind mouse wheel to canvas scrolling"""
        def _on_mousewheel(event):
            self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
        self.root.bind("<MouseWheel>", _on_mousewheel)
        
    def animate(self):
        """Main animation loop"""
        self.animation_frame += 1
        
        # Animate loading indicator
        if hasattr(self, 'loading_indicator'):
            animations = ["⚡", "✨", "🔥", "⭐", "💫"]
            if self.suggestion_animation:
                self.loading_indicator.config(text=animations[self.animation_frame % len(animations)])
            else:
                self.loading_indicator.config(text="")
        
        # Animate hero title color
        if hasattr(self, 'hero_title'):
            if self.animation_frame % 100 == 0:  # Change every 5 seconds
                colors = ['white', '#fbbf24', '#10b981', '#f59e0b']
                color = colors[(self.animation_frame // 100) % len(colors)]
                self.hero_title.config(fg=color)
        
        # Continue animation
        self.root.after(50, self.animate)
        
    def animate_suggestion_refresh(self):
        """Animate suggestion refresh"""
        self.suggestion_animation = True
        self.refresh_suggestion_btn.config(state="disabled", text="🔄")
        
        # Simulate loading
        self.root.after(1500, self._finish_suggestion_animation)
        
        # Update suggestion
        self.update_cooking_suggestion()
        
    def _finish_suggestion_animation(self):
        """Finish suggestion animation"""
        self.suggestion_animation = False
        self.refresh_suggestion_btn.config(state="normal", text="🔄")
        
    def update_cooking_suggestion(self):
        """Update the cooking suggestion panel"""
        # Clear existing content
        for widget in self.suggestion_content.winfo_children():
            widget.destroy()
            
        # Get random recipe for suggestion
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, meal_name, category, area, meal_thumb 
                FROM meals 
                ORDER BY RANDOM() 
                LIMIT 1
            ''')
            recipe = cursor.fetchone()
            conn.close()
            
            if recipe:
                recipe_id, name, category, area, thumb = recipe
                
                # Create suggestion card
                suggestion_card = tk.Frame(self.suggestion_content, bg=self.colors['surface'])
                suggestion_card.pack(fill="x")
                
                # Left side - image
                image_frame = tk.Frame(suggestion_card, bg=self.colors['surface_dark'], 
                                     width=120, height=90)
                image_frame.pack_propagate(False)
                image_frame.pack(side="left", padx=(0, 20))
                
                # Load suggestion image
                self.load_recipe_image(image_frame, recipe_id)
                
                # Right side - info
                info_frame = tk.Frame(suggestion_card, bg=self.colors['surface'])
                info_frame.pack(side="left", fill="both", expand=True)
                
                # Recipe name
                name_label = tk.Label(
                    info_frame,
                    text=f"🎯 Today's Suggestion: {name}",
                    font=("Segoe UI", 14, "bold"),
                    bg=self.colors['surface'],
                    fg=self.colors['primary'],
                    wraplength=400,
                    anchor="w"
                )
                name_label.pack(anchor="w")
                
                # Details
                details_text = f"📂 {category or 'Unknown'} • 🌍 {area or 'Unknown'}"
                details_label = tk.Label(
                    info_frame,
                    text=details_text,
                    font=("Segoe UI", 11),
                    bg=self.colors['surface'],
                    fg=self.colors['text_light'],
                    anchor="w"
                )
                details_label.pack(anchor="w", pady=(5, 10))
                
                # Action buttons
                actions_frame = tk.Frame(info_frame, bg=self.colors['surface'])
                actions_frame.pack(anchor="w")
                
                cook_btn = tk.Button(
                    actions_frame,
                    text="👨‍🍳 Cook This!",
                    command=lambda: self.start_cooking_mode(recipe_id),
                    bg=self.colors['success'],
                    fg='white',
                    font=("Segoe UI", 11, "bold"),
                    relief='flat',
                    bd=0,
                    padx=20,
                    pady=8,
                    cursor='hand2'
                )
                cook_btn.pack(side="left", padx=(0, 10))
                
                view_btn = tk.Button(
                    actions_frame,
                    text="👁️ View Details",
                    command=lambda: self.show_recipe_details_popup(recipe_id),
                    bg=self.colors['primary'],
                    fg='white',
                    font=("Segoe UI", 11, "bold"),
                    relief='flat',
                    bd=0,
                    padx=20,
                    pady=8,
                    cursor='hand2'
                )
                view_btn.pack(side="left")
                
                self.current_suggestion = recipe_id
                
        except Exception as e:
            print(f"Error updating suggestion: {e}")
            # Show fallback message
            fallback_label = tk.Label(
                self.suggestion_content,
                text="🔄 Pull some recipes to get smart suggestions!",
                font=("Segoe UI", 12),
                bg=self.colors['surface'],
                fg=self.colors['text_light']
            )
            fallback_label.pack(pady=20)
            
    def get_random_recipe(self):
        """Get a random recipe and show it"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM meals ORDER BY RANDOM() LIMIT 1')
            result = cursor.fetchone()
            conn.close()
            
            if result:
                self.show_recipe_details_popup(result[0])
            else:
                messagebox.showinfo("No Recipes", "Pull some recipes first!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error getting random recipe: {e}")
            
    def get_trending_recipes(self):
        """Show trending/popular recipes"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            # Get recipes from popular categories
            cursor.execute('''
                SELECT id, meal_name, category 
                FROM meals 
                WHERE category IN ('Chicken', 'Dessert', 'Pasta', 'Beef') 
                ORDER BY RANDOM() 
                LIMIT 5
            ''')
            recipes = cursor.fetchall()
            conn.close()
            
            if recipes:
                self.show_trending_popup(recipes)
            else:
                messagebox.showinfo("No Trending Recipes", "Pull some recipes first!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error getting trending recipes: {e}")
            
    def shuffle_cuisine(self):
        """Shuffle through different cuisines"""
        cuisines = ['Italian', 'Chinese', 'Indian', 'Mexican', 'French', 'Japanese', 'Thai', 'American']
        random_cuisine = random.choice(cuisines)
        self.explore_cuisine(random_cuisine)
        
    def explore_cuisine(self, cuisine):
        """Explore recipes from a specific cuisine"""
        if cuisine == "Random":
            self.shuffle_cuisine()
            return
            
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, meal_name, category, area 
                FROM meals 
                WHERE area = ? 
                ORDER BY RANDOM() 
                LIMIT 6
            ''', (cuisine,))
            recipes = cursor.fetchall()
            conn.close()
            
            if recipes:
                self.show_cuisine_explorer_popup(cuisine, recipes)
            else:
                # Filter by category if no area matches
                self.cuisine_var.set(cuisine)
                self.filter_recipes()
                messagebox.showinfo("Cuisine Explorer", f"Filtered recipes for {cuisine}!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error exploring cuisine: {e}")
            
    def suggest_for_today(self):
        """Suggest what to cook today based on time and preferences"""
        current_hour = datetime.now().hour
        
        if current_hour < 11:  # Morning
            meal_type = "Breakfast"
            suggestions = ["Pancakes", "Eggs", "Oatmeal"]
        elif current_hour < 15:  # Lunch
            meal_type = "Lunch"
            suggestions = ["Sandwich", "Salad", "Soup"]
        else:  # Dinner
            meal_type = "Dinner"
            suggestions = ["Chicken", "Pasta", "Seafood"]
            
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Try to find recipes matching suggestions
            for suggestion in suggestions:
                cursor.execute('''
                    SELECT id, meal_name, category 
                    FROM meals 
                    WHERE meal_name LIKE ? OR category LIKE ?
                    ORDER BY RANDOM() 
                    LIMIT 3
                ''', (f'%{suggestion}%', f'%{suggestion}%'))
                recipes = cursor.fetchall()
                
                if recipes:
                    conn.close()
                    self.show_daily_suggestion_popup(meal_type, recipes)
                    return
                    
            # Fallback to random recipes
            cursor.execute('SELECT id, meal_name, category FROM meals ORDER BY RANDOM() LIMIT 3')
            recipes = cursor.fetchall()
            conn.close()
            
            if recipes:
                self.show_daily_suggestion_popup(meal_type, recipes)
            else:
                messagebox.showinfo("No Suggestions", "Pull some recipes first!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error getting suggestions: {e}")
            
    def change_view_mode(self):
        """Change the recipe view mode"""
        mode = self.view_mode.get()
        if mode == "Gallery":
            self.display_gallery_mode()
        elif mode == "List":
            self.display_list_mode()
        elif mode == "Cards":
            self.display_cards_mode()
            
    def display_gallery_mode(self):
        """Display recipes in gallery mode"""
        # Clear gallery
        for widget in self.gallery_scrollable.winfo_children():
            widget.destroy()
            
        # Get current recipes
        if hasattr(self, 'current_recipes') and self.current_recipes:
            cols = 3  # 3 recipes per row
            for i, recipe in enumerate(self.current_recipes[:12]):  # Show max 12
                row = i // cols
                col = i % cols
                self.create_recipe_card(self.gallery_scrollable, recipe, row, col)
                
            # Configure grid weights
            for j in range(cols):
                self.gallery_scrollable.grid_columnconfigure(j, weight=1)
                
    def display_list_mode(self):
        """Display recipes in list mode"""
        # Clear gallery
        for widget in self.gallery_scrollable.winfo_children():
            widget.destroy()
            
        # Create list header
        header_frame = tk.Frame(self.gallery_scrollable, bg=self.colors['surface_dark'], height=40)
        header_frame.pack(fill="x", pady=(0, 1))
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="Recipe Name", font=("Segoe UI", 11, "bold"),
                bg=self.colors['surface_dark'], fg=self.colors['text']).pack(side="left", padx=20, pady=10)
        
        # Display recipes as list items
        if hasattr(self, 'current_recipes') and self.current_recipes:
            for recipe in self.current_recipes:
                self.create_list_item(self.gallery_scrollable, recipe)
                
    def display_cards_mode(self):
        """Display recipes in compact cards mode"""
        # Clear gallery
        for widget in self.gallery_scrollable.winfo_children():
            widget.destroy()
            
        # Get current recipes
        if hasattr(self, 'current_recipes') and self.current_recipes:
            cols = 4  # 4 recipes per row
            for i, recipe in enumerate(self.current_recipes):
                row = i // cols
                col = i % cols
                self.create_compact_card(self.gallery_scrollable, recipe, row, col)
                
            # Configure grid weights
            for j in range(cols):
                self.gallery_scrollable.grid_columnconfigure(j, weight=1)
                
    def create_list_item(self, parent, recipe):
        """Create a list item for a recipe"""
        recipe_id, name, category, area = recipe
        
        item_frame = tk.Frame(parent, bg=self.colors['surface'], height=50)
        item_frame.pack(fill="x", pady=1)
        item_frame.pack_propagate(False)
        
        # Recipe info
        info_frame = tk.Frame(item_frame, bg=self.colors['surface'])
        info_frame.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        
        name_label = tk.Label(
            info_frame,
            text=name,
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['text'],
            anchor="w"
        )
        name_label.pack(side="left")
        
        details_label = tk.Label(
            info_frame,
            text=f" • {category or 'Unknown'} • {area or 'Unknown'}",
            font=("Segoe UI", 10),
            bg=self.colors['surface'],
            fg=self.colors['text_light'],
            anchor="w"
        )
        details_label.pack(side="left")
        
        # Action button
        view_btn = tk.Button(
            item_frame,
            text="View",
            command=lambda: self.show_recipe_details_popup(recipe_id),
            bg=self.colors['primary'],
            fg='white',
            font=("Segoe UI", 9, "bold"),
            relief='flat',
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        view_btn.pack(side="right", padx=20)
        
    def create_compact_card(self, parent, recipe, row, col):
        """Create a compact recipe card"""
        recipe_id, name, category, area = recipe
        
        card_frame = tk.Frame(
            parent,
            bg=self.colors['surface'],
            relief='solid',
            bd=1,
            padx=10,
            pady=10
        )
        card_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        # Recipe name
        name_label = tk.Label(
            card_frame,
            text=name,
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['text'],
            wraplength=150
        )
        name_label.pack()
        
        # Details
        if category:
            category_label = tk.Label(
                card_frame,
                text=f"📂 {category}",
                font=("Segoe UI", 9),
                bg=self.colors['surface'],
                fg=self.colors['text_light']
            )
            category_label.pack(pady=(5, 0))
            
        # View button
        view_btn = tk.Button(
            card_frame,
            text="View",
            command=lambda: self.show_recipe_details_popup(recipe_id),
            bg=self.colors['accent'],
            fg='white',
            font=("Segoe UI", 8, "bold"),
            relief='flat',
            bd=0,
            padx=10,
            pady=4,
            cursor='hand2'
        )
        view_btn.pack(pady=(5, 0))
        
    def show_recipe_details_popup(self, recipe_id):
        """Show recipe details in a modern popup window"""
        popup = tk.Toplevel(self.root)
        popup.title("Recipe Details")
        popup.geometry("800x600")
        popup.configure(bg=self.colors['background'])
        popup.transient(self.root)
        popup.grab_set()
        
        # Get recipe details
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT meal_name, category, area, instructions, meal_thumb, tags, youtube
            FROM meals WHERE id = ?
        ''', (recipe_id,))
        meal_details = cursor.fetchone()
        
        cursor.execute('''
            SELECT ingredient_name, measurement
            FROM ingredients WHERE meal_id = ?
            ORDER BY ingredient_order
        ''', (recipe_id,))
        ingredients = cursor.fetchall()
        
        conn.close()
        
        if not meal_details:
            popup.destroy()
            messagebox.showerror("Error", "Recipe not found!")
            return
            
        name, category, area, instructions, thumb, tags, youtube = meal_details
        
        # Create popup content with modern styling
        main_frame = tk.Frame(popup, bg=self.colors['background'])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header with recipe name
        header_frame = tk.Frame(main_frame, bg=self.colors['primary'], height=80)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        header_title = tk.Label(
            header_frame,
            text=name,
            font=("Segoe UI", 20, "bold"),
            bg=self.colors['primary'],
            fg='white',
            wraplength=600
        )
        header_title.pack(expand=True, pady=15)
        
        # Content area with scrolling
        content_canvas = tk.Canvas(main_frame, bg=self.colors['background'], highlightthickness=0)
        content_scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=content_canvas.yview)
        content_frame = tk.Frame(content_canvas, bg=self.colors['background'])
        
        content_frame.bind(
            "<Configure>",
            lambda e: content_canvas.configure(scrollregion=content_canvas.bbox("all"))
        )
        
        content_canvas.create_window((0, 0), window=content_frame, anchor="nw")
        content_canvas.configure(yscrollcommand=content_scrollbar.set)
        
        content_canvas.pack(side="left", fill="both", expand=True)
        content_scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel scrolling to the canvas
        def _on_popup_mousewheel(event):
            content_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind mouse wheel events to popup and canvas
        popup.bind("<MouseWheel>", _on_popup_mousewheel)
        content_canvas.bind("<MouseWheel>", _on_popup_mousewheel)
        content_frame.bind("<MouseWheel>", _on_popup_mousewheel)
        
        # Recipe info section
        info_frame = tk.Frame(content_frame, bg=self.colors['surface'], relief='solid', bd=1, padx=20, pady=20)
        info_frame.pack(fill="x", pady=(0, 20))
        
        if category:
            tk.Label(info_frame, text=f"📂 Category: {category}", 
                    font=("Segoe UI", 12), bg=self.colors['surface'], fg=self.colors['text']).pack(anchor="w", pady=2)
        if area:
            tk.Label(info_frame, text=f"🌍 Cuisine: {area}", 
                    font=("Segoe UI", 12), bg=self.colors['surface'], fg=self.colors['text']).pack(anchor="w", pady=2)
        if tags:
            tk.Label(info_frame, text=f"🏷️ Tags: {tags}", 
                    font=("Segoe UI", 12), bg=self.colors['surface'], fg=self.colors['text'], wraplength=300).pack(anchor="w", pady=2)
        if youtube:
            tk.Label(info_frame, text="📺 Video Available", 
                    font=("Segoe UI", 12), bg=self.colors['surface'], fg=self.colors['success']).pack(anchor="w", pady=2)
        
        # Ingredients section
        if ingredients:
            ingredients_frame = tk.Frame(content_frame, bg=self.colors['surface'], relief='solid', bd=1, padx=20, pady=20)
            ingredients_frame.pack(fill="x", pady=(0, 20))
            
            tk.Label(ingredients_frame, text=f"🥕 Ingredients ({len(ingredients)} items)", 
                    font=("Segoe UI", 14, "bold"), bg=self.colors['surface'], fg=self.colors['primary']).pack(anchor="w", pady=(0, 10))
            
            for i, (ingredient, measure) in enumerate(ingredients):
                bullet = "•" if i % 2 == 1 else "◦"
                text = f"{bullet} {measure} {ingredient}" if measure and measure.strip() else f"{bullet} {ingredient}"
                tk.Label(ingredients_frame, text=text, font=("Segoe UI", 11), 
                        bg=self.colors['surface'], fg=self.colors['text'], anchor="w").pack(anchor="w", pady=1)
        
        # Instructions section
        if instructions and instructions.strip():
            instructions_frame = tk.Frame(content_frame, bg=self.colors['surface'], relief='solid', bd=1, padx=20, pady=20)
            instructions_frame.pack(fill="x", pady=(0, 20))
            
            tk.Label(instructions_frame, text="👨‍🍳 Cooking Instructions", 
                    font=("Segoe UI", 14, "bold"), bg=self.colors['surface'], fg=self.colors['primary']).pack(anchor="w", pady=(0, 10))
            
            # Format instructions with better spacing
            formatted_instructions = instructions.replace('. ', '.\n\n')
            
            instructions_text = tk.Text(
                instructions_frame,
                wrap=tk.WORD,
                font=("Segoe UI", 11),
                bg=self.colors['surface'],
                fg=self.colors['text'],
                relief='flat',
                bd=0,
                height=10,
                highlightthickness=0
            )
            instructions_text.pack(fill="both", expand=True)
            instructions_text.insert(1.0, formatted_instructions)
            instructions_text.config(state='disabled')
        
        # Action buttons
        buttons_frame = tk.Frame(content_frame, bg=self.colors['background'])
        buttons_frame.pack(fill="x", pady=20)
        
        cook_btn = tk.Button(
            buttons_frame,
            text="👨‍🍳 Start Cooking Mode",
            command=lambda: [popup.destroy(), self.start_cooking_mode(recipe_id)],
            bg=self.colors['success'],
            fg='white',
            font=("Segoe UI", 12, "bold"),
            relief='flat',
            bd=0,
            padx=25,
            pady=12,
            cursor='hand2'
        )
        cook_btn.pack(side="left", padx=(0, 10))
        
        if youtube:
            video_btn = tk.Button(
                buttons_frame,
                text="📺 Watch Video",
                command=lambda: self.open_video(youtube),
                bg=self.colors['danger'],
                fg='white',
                font=("Segoe UI", 12, "bold"),
                relief='flat',
                bd=0,
                padx=25,
                pady=12,
                cursor='hand2'
            )
            video_btn.pack(side="left", padx=(0, 10))
        
        close_btn = tk.Button(
            buttons_frame,
            text="✖ Close",
            command=popup.destroy,
            bg=self.colors['text_light'],
            fg='white',
            font=("Segoe UI", 12, "bold"),
            relief='flat',
            bd=0,
            padx=25,
            pady=12,
            cursor='hand2'
        )
        close_btn.pack(side="right")
        
    def start_cooking_mode(self, recipe_id):
        """Start interactive cooking mode"""
        messagebox.showinfo("Cooking Mode", f"Starting cooking mode for recipe {recipe_id}!\n\n🍳 Timer features and step-by-step instructions coming soon!")
        
    def show_trending_popup(self, recipes):
        """Show trending recipes popup"""
        messagebox.showinfo("Trending", f"Found {len(recipes)} trending recipes!")
        
    def show_cuisine_explorer_popup(self, cuisine, recipes):
        """Show cuisine explorer popup"""
        messagebox.showinfo("Cuisine Explorer", f"Exploring {cuisine} cuisine with {len(recipes)} recipes!")
        
    def show_daily_suggestion_popup(self, meal_type, recipes):
        """Show daily cooking suggestions popup"""
        messagebox.showinfo("Daily Suggestion", f"{meal_type} suggestions ready with {len(recipes)} recipes!")
        
    def open_video(self, youtube_url):
        """Open YouTube video"""
        import webbrowser
        webbrowser.open(youtube_url)
        
        
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
        
        # Reset progress bar
        if hasattr(self, 'progress_var'):
            self.progress_var.set(0)
        
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
                                
                                # Update progress and status
                                progress = (len(recipes) / amount) * 100
                                if hasattr(self, 'progress_var'):
                                    self.root.after(0, lambda p=progress: self.progress_var.set(p))
                                
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
            text="� Pull Recipes",
            bg=self.colors['primary']
        )
        self.status_label.config(text=f"✨ Added {saved_count} new recipes!")
        
        # Reset progress bar
        if hasattr(self, 'progress_var'):
            self.progress_var.set(100)
            self.root.after(2000, lambda: self.progress_var.set(0))
        
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
        
        # Count recipes added today
        cursor.execute("SELECT COUNT(*) FROM meals WHERE DATE(created_at) = DATE('now')")
        recent_count = cursor.fetchone()[0]
        
        conn.close()
        
        # Update stat cards
        if hasattr(self, 'stat_cards'):
            self.stat_cards['meals'].value_label.config(text=str(meals_count))
            self.stat_cards['ingredients'].value_label.config(text=str(ingredients_count))
            self.stat_cards['categories'].value_label.config(text=str(categories_count))
            self.stat_cards['cuisines'].value_label.config(text=str(cuisines_count))
            if 'recent' in self.stat_cards:
                self.stat_cards['recent'].value_label.config(text=str(recent_count))
        
    def load_recipes(self):
        """Load recipes and populate gallery"""
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
        categories = ["All Categories"] + [row[0] for row in cursor.fetchall()]
        if hasattr(self, 'category_combo'):
            self.category_combo['values'] = categories
        
        # Load cuisines for filter
        cursor.execute('SELECT DISTINCT area FROM meals WHERE area IS NOT NULL ORDER BY area')
        cuisines = ["All Cuisines"] + [row[0] for row in cursor.fetchall()]
        if hasattr(self, 'cuisine_combo'):
            self.cuisine_combo['values'] = cuisines
        
        conn.close()
        
        # Display all recipes initially
        self.display_recipes(self.all_recipes)
        
    def display_recipes(self, recipes):
        """Display recipes in the current view mode"""
        # Store current recipes for selection
        self.current_recipes = recipes
        
        # Update gallery based on current view mode
        if hasattr(self, 'view_mode'):
            mode = self.view_mode.get()
            if mode == "Gallery":
                self.display_gallery_mode()
            elif mode == "List":
                self.display_list_mode()
            elif mode == "Cards":
                self.display_cards_mode()
        else:
            # Fallback to gallery mode
            self.display_gallery_mode()
        self.current_recipes = recipes
        
    def filter_recipes(self, *args):
        """Filter recipes based on search and category/cuisine"""
        if not hasattr(self, 'search_var') or not hasattr(self, 'all_recipes'):
            return
            
        search_text = self.search_var.get().lower()
        selected_category = self.category_var.get() if hasattr(self, 'category_var') else "All Categories"
        selected_cuisine = self.cuisine_var.get() if hasattr(self, 'cuisine_var') else "All Cuisines"
        
        filtered_recipes = []
        
        for recipe in self.all_recipes:
            recipe_id, name, category, area = recipe
            
            # Check search text
            if search_text and search_text not in name.lower():
                continue
                
            # Check category filter
            if selected_category not in ["All Categories", "All"] and category != selected_category:
                continue
                
            # Check cuisine filter
            if selected_cuisine not in ["All Cuisines", "All"] and area != selected_cuisine:
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
