import os
import requests

from dotenv import load_dotenv
from requests import Response
from src.ppl_screen_package.models import CraftBeneficialOwners, GraphQlFragment, GraphQlVariables, CraftPayload, CraftCompanyUbo

# Load environment variables
_ = load_dotenv()
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
def get_company_ubo(id: int) -> CraftCompanyUbo: #BeneficialOwners:
    query = construct_query_string(fragment_ubo)
    variables = GraphQlVariables(id=id)
    response: Response = requests.post(
        url=craft_url,
        headers={"X-Craft-Api-Key": craft_key},
        json=CraftPayload(query=query, variables=variables).model_dump(),
    )
    response_body = response.json()
    company_ubo = CraftCompanyUbo.model_validate(response_body['data']['company'])
    return company_ubo

def get_individual_owners(ubo_company: CraftCompanyUbo) -> CraftBeneficialOwners:
    beneficial_owners = CraftBeneficialOwners.model_validate(ubo_company.dnb.beneficialOwnershipStructure)
    individual_owners = CraftBeneficialOwners(beneficialOwners=[beneficial_owner for beneficial_owner in beneficial_owners.beneficialOwners if beneficial_owner.beneficiaryType.description == 'Individual' and beneficial_owner.beneficialOwnershipPercentage > 0])
    return individual_owners


def main():
    id: int = 60903
    ubo = get_company_ubo(id)
    individuals = get_individual_owners(ubo)
    print(individuals)

if __name__ == "__main__":
    main()
