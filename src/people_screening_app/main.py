from people_screening_app.fetch_company import SubjectCompany, fetchSubjectCompany
from people_screening_app.fetch_ubo import get_individual_owners, get_beneficial_owners
from people_screening_app.fetch_acuris_individuals import get_acuris_matches, MatchedOwners
import streamlit as st
import pandas as pd

# - DATA PIPELINE - #

# Subject Company ID and information
craft_id: int = 60903 # initialise craft ID
company_info: SubjectCompany = fetchSubjectCompany(craft_id) # Get company info for company id
company_df = pd.DataFrame(company_info) # Get ubo data for company id

# Beneficial Owners
beneficial_owners = get_beneficial_owners(craft_id) # Get all beneficial owners from the UBO object
individual_owners = get_individual_owners(beneficial_owners) # Filter to individuals with >0% ownership
# individual_owners_df = pd.DataFrame(individual_owners) # Export individual owners to dataframe

# Acuris Matches
matched_owners: MatchedOwners = get_acuris_matches(individual_owners) # Get acuris matches and join to individual owners


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
        individual_owners_df,
        hide_index=True,
        height=500
    )

    

def main():
    print(matched_owners)

if __name__ == "__main__":
    main()
