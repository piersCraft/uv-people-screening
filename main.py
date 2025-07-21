from src.ppl_screen_package.fetch_ubo import get_company_ubo, get_individual_owners
from src.ppl_screen_package.models import CraftCompanyDetails, OwnerSummaries
from src.ppl_screen_package.fetch_acuris_individuals import acuris_match_owners

import streamlit as st


    
# - STREAMLIT APP - #
# Title and layout
def app_config(subjectCompany: CraftCompanyDetails) -> None:
    # Page title and layout
    st.set_page_config(
        page_title=f"Key People Report: {subjectCompany.displayName}",
        page_icon="src/assets/craft_favicon.png",
        layout='centered',
        initial_sidebar_state='collapsed',
        # custom_css=""""""
    )

    # Logo
    CRAFT_FAVICON = "assets/craft_favicon.png"
    st.logo(CRAFT_FAVICON,size="large")

# Subject company information
def company_info(subject_company: CraftCompanyDetails) -> None:
    col1, col2  = st.columns([1,19], vertical_alignment="center")
    with col1:
        st.image(subject_company.logo, width=70)
    with col2:
        st.markdown(f"### {subject_company.displayName}")

    col3, col4  = st.columns([1,19], vertical_alignment="center")
    with col3:
        st.empty()
    with col4: 
        st.markdown("#### People Screening Report")

    _ = st.divider()


def main():
    # Execute data pipeline
    craft_id: int = 60903  #  craft ID : jfrog=60903 shenzen=1915183
    beneficial_owners = get_company_ubo(craft_id)
    individual_owners = get_individual_owners(beneficial_owners)
    matched_owners = acuris_match_owners(individual_owners)
    owner_summaries = OwnerSummaries.model_validate(matched_owners.model_dump())

    print(owner_summaries.model_dump())

if __name__ == "__main__":
    main()
