from dotenv import load_dotenv
import os
from pydantic import BaseModel
from typing import Any
import requests
from requests import Response
# Load environment variables
load_dotenv()
craft_key: str = os.getenv("KEY_CRAFT_SOLENG")
craft_url: str = os.getenv("URL_CRAFT_QUERY")

# Define classes

class BeneficialOwner(BaseModel):
    name: str
    beneficiaryType: str | None
    country: str | None
    ownershipPercentage: float | None
    degreeOfSeparation: int | None

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
fragment_ubo = QueryFragment(
    name="ubo",
    on_type="Company",
    fields=""" id displayName shortDescription dnb { beneficialOwnershipStructure { beneficialOwners { name beneficiaryType { description } address { country } beneficialOwnershipPercentage degreeOfSeparation } } }""")

# Build graphQL query string
def construct_query_string(fragment: QueryFragment) -> str:
    query_string: str = f"""query company($id: ID) {{ company(id: $id) {{ ...{fragment.name} }} }} fragment {fragment.name} on {fragment.on_type} {{ {fragment.fields} }}"""
    return(query_string)

# Fetch data and process to dataframe
def get_beneficial_owners(id: int) -> list[dict[str,str | int | float | None]]:
    query = construct_query_string(fragment_ubo)
    variables = Variables(id=id)
    response: Response = requests.post(
        url=craft_url,
        headers={"X-Craft-Api-Key": craft_key},
        json=CraftPayload(query=query, variables=variables).model_dump(),
    )
    response_body = response.json()
    ubo = response_body['data']['company']['dnb']['beneficialOwnershipStructure']['beneficialOwners']
    owners = [
        {
            'name': o.get('name', None),
            'country': o.get('address', None).get('country','Unknown') if o.get('address') is not None else None,
            'ownershipPercentage': o.get('beneficialOwnershipPercentage', None),
            'beneficiaryType': o.get('beneficiaryType', None).get('description', None) if o.get('beneficiaryType') is not None else None,
            'degreeOfSeparation': o.get('degreeOfSeparation', None)
        }
        for o in ubo
    ]

    return owners

def get_individual_owners(owner_data: list[dict[str, Any]]) -> BeneficialOwners:
    individual_owners = [owner for owner in owner_data if owner['beneficiaryType'] == 'Individual' and owner['ownershipPercentage'] >= 1]
    return BeneficialOwners(beneficialOwners=individual_owners)


def main():
    id: int = 60903
    owners = get_beneficial_owners(id)
    return owners

if __name__ == "__main__":
    main()
