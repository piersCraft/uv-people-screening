import os
import requests
from dotenv import load_dotenv
from src.ppl_screen_package.models import AcurisPayload, AcurisMatchResults, CraftBeneficialOwners, CraftBeneficialOwner, MatchedOwner, MatchedOwners


_ = load_dotenv()
acuris_key: str | bytes = os.getenv("KEY_ACURIS_TEST")
acuris_url: str | bytes = os.getenv('URL_ACURIS_INDIVIDUAL')


# Get matches for a beneficial owner name
def post_acuris_search(owner_name: str) -> AcurisMatchResults:
    payload = AcurisPayload(name=owner_name)
    response  = requests.post(url=acuris_url,headers={"X-Api-Key": acuris_key},json=payload.model_dump())
    response.raise_for_status()
    acurisResult = AcurisMatchResults.model_validate(response.json())
    return acurisResult

# Add matches to beneficial owner object
def acuris_match_owner(beneficial_owner: CraftBeneficialOwner) -> MatchedOwner:
    matchedOwner = MatchedOwner(**beneficial_owner.model_dump(),acurisMatchResults=post_acuris_search(f"{beneficial_owner.name}"))
    return matchedOwner

# Loop over owners and add matches to each ubo record
def acuris_match_owners(beneficial_owners: CraftBeneficialOwners) -> MatchedOwners:
    matched_owners = MatchedOwners(matchedOwners=[acuris_match_owner(beneficial_owner) for beneficial_owner in beneficial_owners.beneficialOwners])
    return matched_owners


# - GET COMPLIANCE DATA - #
def get_compliance_data(resource_id: str):
    resource_url = f"{acuris_url}{resource_id}"
    response = requests.get(url=resource_url,headers={"X-Api-Key": acuris_key})
    response.raise_for_status()
    data = response.json()

    return data

# Testing wit Jfrog ID
def main():
    print("main")

if __name__ == "__main__":
    main()
