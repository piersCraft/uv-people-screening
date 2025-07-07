import streamlit as st
from pydantic import BaseModel
from processors.fetch_company import SubjectCompany

# Classes

def create_report(subjectCompany: SubjectCompany) -> None:
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
        page_title=subjectCompany.displayName,
        page_icon='🚀',
        layout='centered',
        initial_sidebar_state='collapsed',
        # custom_css=""""""
    )
    # Display company information
    st.title(subjectCompany.displayName)
    st.image(subjectCompany.logo)
    st.markdown(f"""
    # Description
    {subjectCompany.shortDescription}
    """)

def build_cover_page():
    create_report(subjectCompany)
    render_markdown("""
    ## 🎛️ Company Overview
    
    * Identifying growth trends
    """)

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
    print(pageConfig)
