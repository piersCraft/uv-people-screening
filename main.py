from dotenv import load_dotenv
import os
import json
from pydantic import BaseModel, Json
from typing import Any
import requests

# Load environment variables
load_dotenv()
craft_key: str  = os.getenv("KEY_CRAFT_SOLENG")
craft_url: str = os.getenv("URL_CRAFT_QUERY")

# Define classes
class SubjectCompany(BaseModel):
    id: int
    displayName: str
    shortDescription: str

class BeneficialOwner(BaseModel):
    name: str
    beneficiaryType: str
    country: str
    beneficialOwnershipPercentage: float
    degreeOfSeparation: int

class BeneficialOwners(BaseModel):
    owners: list[BeneficialOwner]

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


# Create instances
ubo_data = QueryFragment(
    name="ubo",
    on_type="Company",
    fields="""\n  id\n  displayName\n  shortDescription\n  dnb {\n   beneficialOwnershipStructure {\n    beneficialOwners {\n     name\n     beneficiaryType {\n      description\n     }\n     address {\n      country\n     }\n     appliedControlType {\n      description\n     }\n     beneficialOwnershipPercentage\n     degreeOfSeparation\n    }\n   }\n  }""")


# - FUNCTIONS - #
def constructQuery(fragment: QueryFragment) -> str:
    query_string: str = f"""query company($id: ID) {{\n company(id: $id) {{\n  ...{fragment.name}\n }}\n}}\nfragment {fragment.name} on {fragment.on_type} {{ {fragment.fields}\n}}"""

    return(query_string)


def fetchCompanyData(fragment: QueryFragment, id: int) -> Json[Any]:
    query = constructQuery(fragment)
    variables = Variables(id=id)
    response = requests.post(
        url=craft_url,
        headers={"X-Craft-Api-Key": craft_key},
        json=CraftPayload(query=query, variables=variables).model_dump(),
    )

    return json.dumps(response.json())


# - MAIN - #
def main():
    ubo = fetchCompanyData(ubo_data, 253712)
    print(ubo)


if __name__ == "__main__":
    main()
