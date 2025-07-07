from processors import fetch_company
from processors.fetch_company import SubjectCompany
from processors import fetch_ubo

import streamlit as st
import pandas as pd


# Initialise Craft company id
craft_id: int = 60903

# Get company info for company id
company_info: SubjectCompany = fetch_company.fetchSubjectCompany(craft_id)
company_df = pd.DataFrame(company_info)
# Get ubo data for company id
pipe_ubo_owners = fetch_ubo.fetchBeneficialOwners(craft_id)
# parse names of owners to a list
pipe_individual_owners = fetch_ubo.filter_individuals(pipe_ubo_owners)
owners_df = pd.DataFrame(pipe_individual_owners)

# - STREAMLIT APP - #

# Summary page
def create_summary_page(subjectCompany: SubjectCompany) -> None:
    # Page title and layout
    st.set_page_config(
        page_title=f"Key People Report: {subjectCompany.displayName}",
        page_icon="src/assets/craft_favicon.png",
        layout='centered',
        initial_sidebar_state='collapsed',
        # custom_css=""""""
    )

    # Craft Logo
    CRAFT_FAVICON = "src/assets/craft_favicon.png"
    st.logo(CRAFT_FAVICON,size="large")

    # Subject company information
    col1, col2  = st.columns([0.1,0.9], vertical_alignment="bottom")
    with col1:
        st.image(subjectCompany.logo, width=50)
    with col2:
        st.markdown(f"### {subjectCompany.displayName}")
    st.markdown("Key People Screening Report")
    st.divider()

    # Beneficial Owner summary table
    st.dataframe(
        owners_df,
        hide_index=True,
        height=500
    )

    

def main():
    create_summary_page(company_info)
    print(company_info)

if __name__ == "__main__":
    main()
