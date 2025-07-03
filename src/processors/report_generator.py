import streamlit as st
from pydantic import BaseModel

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
    
    if title:
        st.subheader(title)
    
    if description:
        st.markdown(description)


# Example usage
if __name__ == "__main__":
    # Initialize the app
    create_streamlit_app(
        title="Product Dashboard",
        page_icon="📦",
        layout="wide"
    )
    
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
    
    # Add a simple text summary
    # total_revenue = sum(data.revenue for data in sales_data)
    # total_units = sum(data.units_sold for data in sales_data)
    # render_markdown(f"""
    # ### Annual Summary
    #
    # * **Total Revenue**: £{total_revenue:,.2f}
    # * **Total Units Sold**: {total_units:,}
    # * **Average Revenue per Unit**: £{total_revenue / total_units:.2f}
    # """)
