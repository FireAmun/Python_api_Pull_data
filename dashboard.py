import streamlit as st
import pandas as pd
import logging
from database_manager import DatabaseManager
from etl_pipeline import MealETL
from sqlalchemy import text
import plotly.express as px
import plotly.graph_objects as go

# Configure logging
logging.basicConfig(level=logging.INFO)

# Page configuration
st.set_page_config(
    page_title="MealDB ETL Dashboard",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

class MealDashboard:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.etl = MealETL()
    
    @st.cache_data
    def load_meals(_self) -> pd.DataFrame:
        """Load meals data from database"""
        try:
            query = """
                SELECT m.*, 
                       COUNT(i.id) as ingredient_count
                FROM meals m
                LEFT JOIN ingredients i ON m.id = i.meal_id
                GROUP BY m.id
                ORDER BY m.created_at DESC
            """
            return pd.read_sql(query, _self.db_manager.engine)
        except Exception as e:
            st.error(f"Failed to load meals: {e}")
            return pd.DataFrame()
    
    @st.cache_data
    def load_categories(_self) -> pd.DataFrame:
        """Load categories data"""
        try:
            query = "SELECT * FROM categories ORDER BY category_name"
            return pd.read_sql(query, _self.db_manager.engine)
        except Exception as e:
            st.error(f"Failed to load categories: {e}")
            return pd.DataFrame()
    
    @st.cache_data
    def load_areas(_self) -> pd.DataFrame:
        """Load areas data"""
        try:
            query = "SELECT * FROM areas ORDER BY area_name"
            return pd.read_sql(query, _self.db_manager.engine)
        except Exception as e:
            st.error(f"Failed to load areas: {e}")
            return pd.DataFrame()
    
    @st.cache_data
    def get_meal_ingredients(_self, meal_id: str) -> pd.DataFrame:
        """Get ingredients for a specific meal"""
        try:
            query = """
                SELECT ingredient_name, measurement, ingredient_order
                FROM ingredients 
                WHERE meal_id = :meal_id
                ORDER BY ingredient_order
            """
            return pd.read_sql(query, _self.db_manager.engine, params={'meal_id': meal_id})
        except Exception as e:
            st.error(f"Failed to load ingredients: {e}")
            return pd.DataFrame()
    
    def run_etl_job(self, job_type: str, **kwargs):
        """Run ETL job from dashboard"""
        try:
            if job_type == "random":
                count = kwargs.get('count', 10)
                self.etl.run_incremental_etl(count)
                st.success(f"Successfully loaded {count} random meals!")
                
            elif job_type == "search":
                search_term = kwargs.get('search_term')
                search_type = kwargs.get('search_type')
                self.etl.search_and_load_meals(search_term, search_type)
                st.success(f"Successfully loaded meals for {search_type}: {search_term}!")
                
            # Clear cache to refresh data
            st.cache_data.clear()
            
        except Exception as e:
            st.error(f"ETL job failed: {e}")

def main():
    dashboard = MealDashboard()
    
    st.title("🍽️ MealDB ETL Dashboard")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Overview", "Meals Browser", "Analytics", "ETL Operations"]
    )
    
    if page == "Overview":
        show_overview(dashboard)
    elif page == "Meals Browser":
        show_meals_browser(dashboard)
    elif page == "Analytics":
        show_analytics(dashboard)
    elif page == "ETL Operations":
        show_etl_operations(dashboard)

def show_overview(dashboard):
    st.header("📊 Database Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Get counts
    meals_count = dashboard.db_manager.get_table_count('meals')
    ingredients_count = dashboard.db_manager.get_table_count('ingredients')
    categories_count = dashboard.db_manager.get_table_count('categories')
    areas_count = dashboard.db_manager.get_table_count('areas')
    
    with col1:
        st.metric("Total Meals", meals_count)
    with col2:
        st.metric("Total Ingredients", ingredients_count)
    with col3:
        st.metric("Categories", categories_count)
    with col4:
        st.metric("Areas", areas_count)
    
    # Recent ETL logs
    st.subheader("Recent ETL Operations")
    etl_logs = dashboard.db_manager.get_recent_etl_logs(10)
    if not etl_logs.empty:
        st.dataframe(etl_logs)
    else:
        st.info("No ETL logs found")

def show_meals_browser(dashboard):
    st.header("🔍 Meals Browser")
    
    # Load data
    meals_df = dashboard.load_meals()
    categories_df = dashboard.load_categories()
    areas_df = dashboard.load_areas()
    
    if meals_df.empty:
        st.warning("No meals found in database. Run ETL operations first.")
        return
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category_filter = st.selectbox(
            "Filter by Category",
            ["All"] + sorted(meals_df['category'].dropna().unique().tolist())
        )
    
    with col2:
        area_filter = st.selectbox(
            "Filter by Area",
            ["All"] + sorted(meals_df['area'].dropna().unique().tolist())
        )
    
    with col3:
        search_text = st.text_input("Search meals by name")
    
    # Apply filters
    filtered_df = meals_df.copy()
    
    if category_filter != "All":
        filtered_df = filtered_df[filtered_df['category'] == category_filter]
    
    if area_filter != "All":
        filtered_df = filtered_df[filtered_df['area'] == area_filter]
    
    if search_text:
        filtered_df = filtered_df[
            filtered_df['meal_name'].str.contains(search_text, case=False, na=False)
        ]
    
    st.subheader(f"Found {len(filtered_df)} meals")
    
    # Display meals
    for idx, meal in filtered_df.iterrows():
        with st.expander(f"🍽️ {meal['meal_name']} ({meal['category']})"):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                if meal['meal_thumb']:
                    st.image(meal['meal_thumb'], width=200)
            
            with col2:
                st.write(f"**Category:** {meal['category']}")
                st.write(f"**Area:** {meal['area']}")
                st.write(f"**Ingredients:** {meal['ingredient_count']}")
                
                if meal['tags']:
                    st.write(f"**Tags:** {meal['tags']}")
                
                if meal['youtube']:
                    st.write(f"**YouTube:** [Watch Video]({meal['youtube']})")
                
                # Show ingredients
                ingredients_df = dashboard.get_meal_ingredients(meal['id'])
                if not ingredients_df.empty:
                    st.write("**Ingredients:**")
                    for _, ingredient in ingredients_df.iterrows():
                        measurement = ingredient['measurement'] or ""
                        st.write(f"- {measurement} {ingredient['ingredient_name']}")
                
                # Show instructions
                if meal['instructions']:
                    with st.expander("Instructions"):
                        st.write(meal['instructions'])

def show_analytics(dashboard):
    st.header("📈 Analytics")
    
    meals_df = dashboard.load_meals()
    
    if meals_df.empty:
        st.warning("No data available for analytics")
        return
    
    # Category distribution
    st.subheader("Meals by Category")
    category_counts = meals_df['category'].value_counts()
    fig1 = px.bar(
        x=category_counts.index,
        y=category_counts.values,
        labels={'x': 'Category', 'y': 'Number of Meals'},
        title="Distribution of Meals by Category"
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Area distribution
    st.subheader("Meals by Area/Cuisine")
    area_counts = meals_df['area'].value_counts().head(15)
    fig2 = px.pie(
        values=area_counts.values,
        names=area_counts.index,
        title="Top 15 Cuisines by Number of Meals"
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # Ingredient count distribution
    st.subheader("Ingredient Count Analysis")
    fig3 = px.histogram(
        meals_df,
        x='ingredient_count',
        nbins=20,
        title="Distribution of Ingredient Counts",
        labels={'ingredient_count': 'Number of Ingredients', 'count': 'Number of Meals'}
    )
    st.plotly_chart(fig3, use_container_width=True)
    
    # Summary statistics
    st.subheader("Summary Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Average Ingredients", f"{meals_df['ingredient_count'].mean():.1f}")
    with col2:
        st.metric("Max Ingredients", meals_df['ingredient_count'].max())
    with col3:
        st.metric("Min Ingredients", meals_df['ingredient_count'].min())

def show_etl_operations(dashboard):
    st.header("⚙️ ETL Operations")
    
    # Random meals ETL
    st.subheader("Load Random Meals")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        meal_count = st.number_input("Number of meals to load", min_value=1, max_value=50, value=10)
    
    with col2:
        if st.button("Load Random Meals"):
            with st.spinner("Loading meals..."):
                dashboard.run_etl_job("random", count=meal_count)
    
    st.markdown("---")
    
    # Search-based ETL
    st.subheader("Load Meals by Search")
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input("Search term")
    
    with col2:
        search_type = st.selectbox(
            "Search type",
            ["name", "category", "area", "ingredient", "letter"]
        )
    
    with col3:
        if st.button("Search & Load"):
            if search_term:
                with st.spinner(f"Searching for {search_term}..."):
                    dashboard.run_etl_job("search", search_term=search_term, search_type=search_type)
            else:
                st.error("Please enter a search term")
    
    st.markdown("---")
    
    # Manual schema setup
    st.subheader("Database Management")
    if st.button("Initialize Database Schema"):
        try:
            dashboard.db_manager.execute_schema()
            st.success("Database schema initialized successfully!")
        except Exception as e:
            st.error(f"Failed to initialize schema: {e}")

if __name__ == "__main__":
    main()
