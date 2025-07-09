import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Any
import requests
from people_screening_app.fetch_ubo import BeneficialOwners, get_beneficial_owners, get_individual_owners


# Load environment variables
_ = load_dotenv()

acuris_key: str | bytes = os.getenv("KEY_ACURIS_TEST")
acuris_url: str | bytes = os.getenv('URL_ACURIS_INDIVIDUAL')

# - CLASSES - #

class Datasets(BaseModel):
    datasets: list[str]

class DatesOfBirth(BaseModel):
    datesOfBirth: list[str | None]

class Address(BaseModel):
    geography: str | None
    city: str | None

class Match(BaseModel):
    qrCode: str
    resourceId: str
    score: int
    match: str
    name: str
    countries: list[str]
    addresses: list[Address]
    datesOfBirth: list[str | None]
    gender: str = 'Unknown'
    profileImage: str = 'Not Available'
    datasets: list[str]
    resourceUri: str
    version: int
    currentSanBodyIds: list[int]
    formerSanBodyIds: list[int]

class Results(BaseModel):
    matchCount: int
    matches: list[Match]

class ApiResponse(BaseModel):
    results: Results

class Payload(BaseModel):
    name: str | None
    threshold: int = 95
    countries: list[str] = ['IL','US','GB']
    datasets: list[str] = ['PEP-CURRENT','PEP-FORMER','PEP-LINKED','SAN-CURRENT','SAN-FORMER','RRE','POI','REL']

class OwnerMatch(BaseModel):
    owner_name: str | None
    owner_matches: list[Match] | None

class MatchedOwners(BaseModel):
    ownerMatches: list[OwnerMatch]

    def add_owner_matches(self, ownerMatches: OwnerMatch) -> None:
        """
        Add matches for a beneficial owner
        """
        self.ownerMatches.append(ownerMatches)


# - FUNCTIONS - #

# Get matches from Acuris search API
# TODO: Add input query string to the output to simplify next function
def post_acuris_search(payload: dict[str,Any]) -> ApiResponse:
    response  = requests.post(url=acuris_url,headers={"X-Api-Key": acuris_key},json=payload)
    response.raise_for_status()
    response_data = response.json()
    acuris_response = ApiResponse(**response_data)
    # acurisResults = AcurisResults(**acurisResponseData.results.model_dump())
    return acuris_response

# Loop over all individual owners and get matches
# TODO: Refactor to a simpler approach using list comprehension
def get_acuris_matches(individual_owners: BeneficialOwners) -> MatchedOwners:
    owner_names: list[str] = [beneficialOwner.name for beneficialOwner in individual_owners.beneficialOwners]

    matched_owners = MatchedOwners(ownerMatches=[])
    for owner_name in owner_names:
        payload = Payload(name=owner_name)
        acuris_response = post_acuris_search(payload.model_dump())
        matches = [match for match in acuris_response.results.matches if len(acuris_response.results.matches) > 0]
        ownerMatch = OwnerMatch(owner_name=owner_name,owner_matches=matches)
        matched_owners.add_owner_matches(ownerMatch)

    return matched_owners


# Testing wit Jfrog ID
def main():
    craft_id: int = 60903

    owners_raw  = get_beneficial_owners(craft_id) # Get all UBO data
    individual_owners  = get_individual_owners(owners_raw) # Filter to individuals with > 0% ownership
    output = get_acuris_matches(individual_owners) # Get acuris matches and join to individual owners
    print(output.model_dump()) # Export to dictionary

if __name__ == "__main__":
    main()
