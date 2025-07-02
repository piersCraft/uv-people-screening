from dotenv import load_dotenv
import os
from pydantic import BaseModel
import requests
import pandas as pd
from pandas import DataFrame

# Load environment variables
load_dotenv()
craft_key: str = os.getenv("KEY_CRAFT_SOLENG")
craft_url: str = os.getenv("URL_CRAFT_QUERY")

# Define classes

class BeneficialOwner(BaseModel):
    name: str
    beneficiaryType: dict[str,str]
    address: dict[str,str]
    beneficialOwnershipPercentage: float
    degreeOfSeparation: int

class BeneficialOwners(BaseModel):
    beneficialOwners: list[BeneficialOwner]

class QueryFragment(BaseModel):
    name: str
    on_type: str
    fields: str

class Variables(BaseModel):
    id: int

class CraftPayload(BaseModel):
    query: str
    variables: Variables

class CraftResponse(BaseModel):
    data: dict[str, str]

# Instantiate ubo fragment
#  TODO: Try removing line breaks from the fields string (see fetch-company module)
fragment_ubo = QueryFragment(
    name="ubo",
    on_type="Company",
    fields="""\n  id\n  displayName\n  shortDescription\n  dnb {\n   beneficialOwnershipStructure {\n    beneficialOwners {\n     name\n     beneficiaryType {\n      description\n     }\n     address {\n      country\n     }\n    beneficialOwnershipPercentage\n     degreeOfSeparation\n    }\n   }\n  }""")

# Build graphQL query string
def constructQuery(fragment: QueryFragment) -> str:
    query_string: str = f"""query company($id: ID) {{\n company(id: $id) {{\n  ...{fragment.name}\n }}\n}}\nfragment {fragment.name} on {fragment.on_type} {{ {fragment.fields}\n}}"""

    return(query_string)

# Fetch data and process to dataframe
def fetchBeneficialOwners(id: int) -> DataFrame:
    query = constructQuery(fragment_ubo)
    variables = Variables(id=id)
    response = requests.post(
        url=craft_url,
        headers={"X-Craft-Api-Key": craft_key},
        json=CraftPayload(query=query, variables=variables).model_dump(),
    )
    response_body = response.json()
    beneficial_owners = response_body['data']['company']['dnb']['beneficialOwnershipStructure']['beneficialOwners']
    ubo_df = pd.json_normalize(beneficial_owners)

    return ubo_df

# Testing with Jfrog ID
def main():
    id: int = 60903
    print(fetchBeneficialOwners(id))

if __name__ == "__main__":
    main()
