from dotenv import load_dotenv
import os
import requests
from requests import Response
from models import CraftBeneficialOwners, GraphQlFragment, Variables, CraftPayload, SubjectCompanyUbo

# Load environment variables
load_dotenv()
craft_key: str = os.getenv("KEY_CRAFT_SOLENG")
craft_url: str = os.getenv("URL_CRAFT_QUERY")
# Instantiate ubo fragment
fragment_ubo = GraphQlFragment(
    name="ubo",
    on_type="Company",
    fields=""" id displayName shortDescription dnb { beneficialOwnershipStructure { beneficialOwners { name beneficiaryType { description } address { country } beneficialOwnershipPercentage degreeOfSeparation } } }""")


# Build graphQL query string
def construct_query_string(fragment: GraphQlFragment) -> str:
    query_string: str = f"""query company($id: ID) {{ company(id: $id) {{ ...{fragment.name} }} }} fragment {fragment.name} on {fragment.on_type} {{ {fragment.fields} }}"""
    return(query_string)

# Get company UBO data
def get_beneficial_owners(id: int) -> SubjectCompanyUbo: #BeneficialOwners:
    query = construct_query_string(fragment_ubo)
    variables = Variables(id=id)
    response: Response = requests.post(
        url=craft_url,
        headers={"X-Craft-Api-Key": craft_key},
        json=CraftPayload(query=query, variables=variables).model_dump(),
    )
    response_body = response.json()
    ubo_company = SubjectCompanyUbo.model_validate(response_body['data']['company'])
    return ubo_company

def get_individual_owners(ubo_company: SubjectCompanyUbo) -> CraftBeneficialOwners:
    beneficial_owners = CraftBeneficialOwners.model_validate(ubo_company.dnb.beneficialOwnershipStructure)
    individual_owners = CraftBeneficialOwners(beneficialOwners=[beneficial_owner for beneficial_owner in beneficial_owners.beneficialOwners if beneficial_owner.beneficiaryType.description == 'Individual' and beneficial_owner.beneficialOwnershipPercentage > 0])
    return individual_owners


def main():
    id: int = 60903
    ubo = get_beneficial_owners(id)
    individuals = get_individual_owners(ubo)
    print(individuals)

if __name__ == "__main__":
    main()
