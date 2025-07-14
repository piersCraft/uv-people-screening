from dotenv import load_dotenv
import os
import requests

from requests import Response
from .models import GraphQlFragment, Variables,  CraftPayload, SubjectCompany

# Load environment variables
_ = load_dotenv()
craft_key: str = os.getenv("KEY_CRAFT_SOLENG")
craft_url: str = os.getenv("URL_CRAFT_QUERY")

# Define classes
# class QueryFragment(BaseModel):
#     name: str
#     on_type: str
#     fields: str
#
# class Variables(BaseModel):
#     id: int
#
# class CraftPayload(BaseModel):
#     query: str
#     variables: Variables
#
# class SubjectCompany(BaseModel):
#     id: int
#     slug: str
#     displayName: str
#     shortDescription: str
#     craftUrl: str
#     logo: dict[str,str]
#     companyType: str
#
# class CraftApiResponse(BaseModel):
#     company: dict[str,SubjectCompany]


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
def fetchSubjectCompany(id: int) -> SubjectCompany:
    query = constructQuery(fragment_company)
    variables = Variables(id=id)
    response: Response = requests.post(url=craft_url,headers={"X-Craft-Api-Key": craft_key},json=CraftPayload(query=query, variables=variables).model_dump())
    subjectCompany = SubjectCompany(**response.json()['data']['company'])

    return subjectCompany


# Testing with jFrog ID
def main():
    id: int = 60903
    subject_company = fetchSubjectCompany(id)
    print(subject_company)


if __name__ == "__main__":
    main()
