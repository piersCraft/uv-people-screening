import os
from dotenv import load_dotenv
from pydantic import BaseModel
from enum import Enum
import requests
from app_modules.fetch_ubo import BeneficialOwner, BeneficialOwners, get_beneficial_owners, get_individual_owners


# - VARIABLES - #
_ = load_dotenv()
acuris_key: str | bytes = os.getenv("KEY_ACURIS_TEST")
acuris_url: str | bytes = os.getenv('URL_ACURIS_INDIVIDUAL')

# - CLASSES - #
class Dataset(str,Enum):
    PEP_CURRENT = 'PEP-CURRENT'
    PEP_FORMER = 'PEP-FORMER'
    PEP_LINKED = 'PEP-LINKED'
    SAN_CURRENT = 'SAN-CURRENT'
    SAN_FORMER = 'SAN-FORMER'
    RRE = 'RRE'
    POI = 'POI'
    REL = 'REL'
    NONE = 'NONE'

class Datasets(BaseModel):
    datasets: list[Dataset]

class DatesOfBirth(BaseModel):
    datesOfBirth: list[str | None]

class Address(BaseModel):
    geography: str | None
    city: str | None

class IndividualMatch(BaseModel):
    qrCode: str
    resourceId: str
    score: int
    match: str
    name: str
    countries: list[str | None]
    addresses: list[Address]
    datesOfBirth: list[str | None]
    gender: str = 'Unknown'
    profileImage: str = 'Not Available'
    datasets: list[Dataset]
    resourceUri: str
    version: int
    currentSanBodyIds: list[int]
    formerSanBodyIds: list[int]

class AcurisMatchResult(BaseModel):
    matchCount: int
    matches: list[IndividualMatch | None]

class AcurisMatchResults(BaseModel):
    results: AcurisMatchResult

class MatchedOwner(BeneficialOwner):
    acurisMatchResults: AcurisMatchResults

    @classmethod
    def add_matches(cls, beneficial_owner: BeneficialOwner, acurisMatchResults: AcurisMatchResults) -> 'MatchedOwner':
        return cls.model_validate({
            **beneficial_owner.model_dump(),
            "acurisMatchResults": acurisMatchResults
        })

class MatchedOwners(BaseModel):
    matchedOwner: list[MatchedOwner] | None

class Payload(BaseModel):
    name: str | None
    threshold: int = 95
    countries: list[str] = ['IL','US','GB']
    datasets: list[str] = ['PEP-CURRENT','PEP-FORMER','PEP-LINKED','SAN-CURRENT','SAN-FORMER','RRE','POI','REL']

class Payloads(BaseModel):
    payloads: list[Payload]


# - FUNCTIONS - #

# Get matches from Acuris search API
def post_acuris_search(owner_name: str) -> AcurisMatchResults:
    payload = Payload(name=owner_name) # Build payload from owner name
    response  = requests.post(url=acuris_url,headers={"X-Api-Key": acuris_key},json=payload.model_dump()) # post to Acuris search endpoint
    response.raise_for_status() # handle errors in response
    # acuris_response = AcurisMatchResults(results=response.json()["results"]) # Serialise response body to results object in API response
    acurisResult = AcurisMatchResults(results=response.json()["results"])

    return acurisResult

def acuris_match_owner(beneficial_owner: BeneficialOwner):
    matchedOwner = MatchedOwner.add_matches(
        beneficial_owner=beneficial_owner,
        acurisMatchResults=post_acuris_search(f"{beneficial_owner.name}").model_dump()
    )

    return matchedOwner

def acuris_match_owners(beneficial_owners: BeneficialOwners) -> MatchedOwners:
    matched_owners = MatchedOwners(matchedOwner=[acuris_match_owner(beneficial_owner) for beneficial_owner in beneficial_owners.beneficialOwners])

    return matched_owners

# Loop over all individual owners and get matches
# def get_acuris_matches(individual_owners: BeneficialOwners) -> MatchedOwners:
    # owner_names: list[str] = [beneficialOwner.name for beneficialOwner in individual_owners.beneficialOwners] # extract names from individual beneficial owners to create payload
    # matched_owners = MatchedOwners(
    #     acuris_data=[
    #         post_acuris_search(owner_name) for owner_name in owner_names
    #     ], 
    #     ubo_data=individual_owners
    # ) # write ubo data and acuris data to matched_owners object for each owner in the owner_names list

    # return matched_owners


# Testing wit Jfrog ID
def main():
    craft_id: int = 60903
    owners_raw  = get_beneficial_owners(craft_id) # Get all UBO data
    individual_owners  = get_individual_owners(owners_raw) # Filter to individuals with > 0% ownership
    # output = get_acuris_matches(individual_owners) # Get acuris matches and join to individual owners
    print(output.model_dump()) # Export to dictionary

if __name__ == "__main__":
    main()
