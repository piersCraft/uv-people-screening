import pandas as pd
import streamlit as st
from pydantic import BaseModel

from app_modules.fetch_acuris_individuals import Dataset, acuris_match_owners
from app_modules.fetch_company import SubjectCompany, fetchSubjectCompany
from app_modules.fetch_ubo import get_beneficial_owners, get_individual_owners

# - DATA PIPELINE - #

# Subject Company ID and information
craft_id: int = 60903 # initialise craft ID
company_info: SubjectCompany = fetchSubjectCompany(craft_id) # Get company info for company id

# Beneficial Owners
beneficial_owners = get_beneficial_owners(craft_id) # Get all beneficial owners from the UBO object
individual_owners = get_individual_owners(beneficial_owners) # Filter to individuals with >0% ownership

# Acuris Matches
matched_owners  = acuris_match_owners(individual_owners) # Get acuris matches and join to individual owners

# Dataframes for Streamlit input
company_df = pd.DataFrame(company_info) # Get ubo data for company id
# individual_owners_df = pd.DataFrame(individual_owners) # Export individual owners to dataframe


class OwnerSummary (BaseModel):
    # TODO: add resourceID and hide the field when deserialized using pydantic field function
    beneficial_owner_name: str
    countries_of_residence: list[str | None]
    ownership_percentage: float | None
    degree_of_separation: int | None
    matched_name: str | None = None
    resource_id: str | None = None
    match_confidence: int | None = None
    # compliance_flags: list[Dataset] = Field(default_factory=lambda:[Dataset.NONE])
    datasets: list[Dataset] | None


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
        _ = st.image(subjectCompany.logo, width=50)
    with col2:
        _ = st.markdown(f"### {subjectCompany.displayName}")

    _ = st.markdown("Key People Screening Report")
    _ = st.divider()

    

def main():
    print(matched_owners.model_dump_json(indent=2))



if __name__ == "__main__":
    main()
