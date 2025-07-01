from dotenv import load_dotenv
import os
from pydantic import BaseModel
from typing import Any
import requests

# Load environment variables
load_dotenv()
craft_key: str = os.getenv("KEY_CRAFT_SOLENG")
craft_url: str = os.getenv("URL_CRAFT_QUERY")

# Define classes
class QueryFragment(BaseModel):
    name: str
    on_type: str
    fields: str

class Variables(BaseModel):
    id: int

class CraftPayload(BaseModel):
    query: str
    variables: Variables

class SubjectCompany(BaseModel):
    id: int
    slug: str
    displayName: str
    shortDescription: str
    craftUrl: str
    logo: str
    companyType: str



# Instantiate company query fragment
fragment_test = QueryFragment(
    name="company",
    on_type="Company",
    fields=""" id slug displayName shortDescription craftUrl logo { url } companyType """)


# Build graphQL query string
def constructQuery(fragment: QueryFragment) -> str:
    query_string: str = f"""query company($id: ID) {{\n company(id: $id) {{\n  ...{fragment.name}\n }}\n}}\nfragment {fragment.name} on {fragment.on_type} {{ {fragment.fields}\n}}"""

    return(query_string)

# Fetch company data
def fetchSubjectCompany(id: int) -> SubjectCompany:
    query = constructQuery(fragment_test)
    variables = Variables(id=id)
    response = requests.post(
        url=craft_url,
        headers={"X-Craft-Api-Key": craft_key},
        json=CraftPayload(query=query, variables=variables).model_dump(),
    )

    response_body: dict[str, Any] = response.json()
    company: dict[str, Any] = response_body['data']['company']
    subjectCompany = SubjectCompany(
        id=company['id'],
        slug=company['slug'],
        displayName=company['displayName'],
        shortDescription=company['shortDescription'],
        craftUrl=company['craftUrl'],
        logo=company['logo']['url'],
        companyType=company['companyType']
    )

    return subjectCompany


# - MAIN - #
def main():
    id: int = 281
    subject_company = fetchSubjectCompany(id)
    print(subject_company)


if __name__ == "__main__":
    main()
