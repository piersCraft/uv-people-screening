from dotenv import load_dotenv
import os
import requests

from requests import Response
from src.ppl_screen_package.models import GraphQlFragment, GraphQlVariables,  CraftPayload, CraftCompanyDetails

# Load environment variables
_ = load_dotenv()
craft_key: str = os.getenv("KEY_CRAFT_SOLENG")
craft_url: str = os.getenv("URL_CRAFT_QUERY")

# Instantiate company query fragment
fragment_company = GraphQlFragment(
    name="company",
    on_type="Company",
    fields=""" id slug displayName shortDescription craftUrl logo { url } companyType """)

# Build graphQL query string
def constructQuery(fragment: GraphQlFragment) -> str:
    query_string: str = f"""query company($id: ID) {{ company(id: $id) {{ ...{fragment.name} }} }} fragment {fragment.name} on {fragment.on_type} {{ {fragment.fields} }}"""

    return query_string

# Fetch company data
def fetchSubjectCompany(id: int) -> CraftCompanyDetails:
    query = constructQuery(fragment_company)
    variables = GraphQlVariables(id=id)
    response: Response = requests.post(url=craft_url,headers={"X-Craft-Api-Key": craft_key},json=CraftPayload(query=query, variables=variables).model_dump())
    subjectCompany = CraftCompanyDetails.model_validate(response.json()['data']['company'])

    return subjectCompany

# Testing with jFrog ID
def main():
    id: int = 60903
    subject_company = fetchSubjectCompany(id)
    print(subject_company.model_dump())


if __name__ == "__main__":
    main()
