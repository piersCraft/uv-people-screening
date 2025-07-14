from pandas import DataFrame
import streamlit as st
from app_modules.fetch_company import SubjectCompany


# - STREAMLIT APP - #
# Title and layout
def app_config(subjectCompany: SubjectCompany) -> None:
    # Page title and layout
    st.set_page_config(
        page_title=f"Key People Report: {subjectCompany.displayName}",
        page_icon="src/assets/craft_favicon.png",
        layout='centered',
        initial_sidebar_state='collapsed',
        # custom_css=""""""
    )

    # Logo
    CRAFT_FAVICON = "src/assets/craft_favicon.png"
    st.logo(CRAFT_FAVICON,size="large")

# Subject company information
def company_info(subjectCompany: SubjectCompany) -> None:
    col1, col2  = st.columns([0.1,0.9], vertical_alignment="bottom")
    with col1:
        _ = st.image(subjectCompany.logo, width=50)
    with col2:
        _ = st.markdown(f"### {subjectCompany.displayName}")

    # Subheading
    _ = st.markdown("Key People Screening Report")
    _ = st.divider()

# Beneficial Owner Summary Table
def owner_summaries(owner_summaries: DataFrame) -> None:
    _ = st.dataframe(owner_summaries)


def main():

if __name__ == "__main__":
    main()

