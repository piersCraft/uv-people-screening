
from app_modules.fetch_company import fetchSubjectCompany, SubjectCompany
from app_modules.fetch_ubo import get_beneficial_owners, get_individual_owners
from app_modules.fetch_acuris_individuals import acuris_match_owners, make_owner_summaries

import streamlit as st
import pandas as pd
from pandas import DataFrame

craft_id: int = 1915183  # initialise craft ID : jfrog=60903

subject_company = fetchSubjectCompany(craft_id)
beneficial_owners = get_beneficial_owners(craft_id) # Get all beneficial owners from the UBO object
individual_owners = get_individual_owners(beneficial_owners) # Filter to individuals with >0% ownership
matched_owners = acuris_match_owners(individual_owners) # Get acuris matches and join to individual owners
matched_owner_summaries = make_owner_summaries(matched_owners)

summaries_df: DataFrame = pd.DataFrame(matched_owner_summaries.model_dump()["owner_summaries"])

    
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
    CRAFT_FAVICON = "assets/craft_favicon.png"
    st.logo(CRAFT_FAVICON,size="large")

# Subject company information
def company_info(subject_company: SubjectCompany) -> None:
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

# Beneficial Owner Summary Table
def owner_summaries(owner_summaries: DataFrame) -> None:
    st.dataframe(owner_summaries,hide_index=True)

def main():
    # Execute data pipeline
    app_config(subject_company)
    company_info(subject_company)
    owner_summaries(summaries_df)

    


    # resource_id = owner_summaries.owner_summaries.pop(2).resource_id
    # compliance_data = get_compliance_data(resource_id)
    # print(compliance_data)
    # matches_per_owner = [matchedOwner.acurisMatchResults.results.matches[:5] for matchedOwner in matched_owners.matchedOwners]

if __name__ == "__main__":
    main()
