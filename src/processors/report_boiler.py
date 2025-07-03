
import streamlit as st
from pydantic import BaseModel, Field
import pandas as pd

def create_streamlit_app(
    title: str,
    page_icon: str | None = "📊",
    layout: str = "centered",
    initial_sidebar_state: str = "collapsed",
) -> None:
    """
    Creates a simple Streamlit application with custom styling.
    
    Args:
        title: The title of the Streamlit app
        page_icon: Icon to display in the browser tab
        layout: Page layout ("centered", "wide")
        initial_sidebar_state: Initial state of the sidebar
        custom_css: Additional custom CSS to apply
    """
    # Configure the page
    st.set_page_config(
        page_title=title,
        page_icon=page_icon,
        layout=layout,
        initial_sidebar_state=initial_sidebar_state
    )
    
    
    # Display the app title
    st.title(title)


def render_markdown(markdown_text: str) -> None:
    """
    Renders a markdown block in the Streamlit app.
    
    Args:
        markdown_text: The markdown text to render
    """
    st.markdown(markdown_text)


def render_table_from_model(
    model_instances: list[BaseModel], 
    title: str | None = None,
    description: str | None = None
) -> None:
    """
    Renders a table based on a list of Pydantic model instances.
    
    Args:
        model_instances: List of Pydantic model instances to display as a table
        title: Optional title for the table section
        description: Optional description text to display above the table
    """
    if not model_instances:
        st.warning("No data to display in the table.")
        return
    
    if title:
        st.subheader(title)
    
    if description:
        st.markdown(description)
    
    # Convert list of model instances to DataFrame
    data = [instance.model_dump() for instance in model_instances]
    df = pd.DataFrame(data)
    
    # Display the table
    st.dataframe(df, use_container_width=True)


# Example usage
if __name__ == "__main__":
    # Define Pydantic models for data
    class Product(BaseModel):
        id: int = Field(..., description="Product ID")
        name: str = Field(..., description="Product name")
        category: str = Field(..., description="Product category")
        price: float = Field(..., description="Product price")
        in_stock: bool = Field(..., description="Whether the product is in stock")
    
    class SalesData(BaseModel):
        quarter: str = Field(..., description="Quarter (e.g., Q1, Q2)")
        revenue: float = Field(..., description="Total revenue")
        units_sold: int = Field(..., description="Number of units sold")
        growth_rate: float = Field(..., description="Growth rate compared to previous quarter")

    class Products(BaseModel):
        products: Product
    
    # Initialize the app
    create_streamlit_app(
        title="Product Dashboard",
        page_icon="📦",
        layout="wide"
    )
    
    # Create sample data
    products = [
        Product(id=1, name="Laptop Pro", category="Electronics", price=1299.99, in_stock=True),
        Product(id=2, name="Smartphone X", category="Electronics", price=799.99, in_stock=True),
        Product(id=3, name="Wireless Headphones", category="Audio", price=149.99, in_stock=False),
        Product(id=4, name="Ergonomic Chair", category="Furniture", price=249.99, in_stock=True),
        Product(id=5, name="Smart Watch", category="Wearables", price=199.99, in_stock=True),
    ]
    
    sales_data = [
        SalesData(quarter="Q1 2024", revenue=1250000, units_sold=2500, growth_rate=0.05),
        SalesData(quarter="Q2 2024", revenue=1425000, units_sold=2850, growth_rate=0.14),
        SalesData(quarter="Q3 2024", revenue=1575000, units_sold=3150, growth_rate=0.105),
        SalesData(quarter="Q4 2024", revenue=1850000, units_sold=3700, growth_rate=0.175),
    ]

    
    # Render markdown content
    render_markdown("""
    ## 🎛️Company Overview
    
    Welcome to the Product Dashboard. This dashboard provides a simple overview of our 
    product catalog and quarterly sales performance.
    
    ### Key Highlights
    
    * Tracking **5 products** across multiple categories
    * Monitoring quarterly sales performance
    * Identifying growth trends
    """)
    
    # Render tables from Pydantic models
    render_table_from_model(
        products, 
        title="Product Catalog",
        description="Current products available in our inventory:"
    )
    
    render_markdown("""
    ## Sales Performance
    
    Below is our quarterly sales performance for the year 2024.
    """)
    
    render_table_from_model(
        sales_data,
        title="Quarterly Sales (2024)",
        description="Revenue and units sold by quarter:"
    )
    
    # Add a simple text summary
    total_revenue = sum(data.revenue for data in sales_data)
    total_units = sum(data.units_sold for data in sales_data)
    
    render_markdown(f"""
    ### Annual Summary
    
    * **Total Revenue**: £{total_revenue:,.2f}
    * **Total Units Sold**: {total_units:,}
    * **Average Revenue per Unit**: £{total_revenue / total_units:.2f}
    """)
