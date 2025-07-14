import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Any
from enum import Enum
import requests
from app_modules.fetch_ubo import BeneficialOwner, BeneficialOwners


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
    datasets: list[str]

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
    addresses: list[dict[str,Any] | None]
    datesOfBirth: list[str | None]
    gender: str = 'Unknown'
    profileImage: str = 'Not Available'
    datasets: list[str]
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
    matchedOwners: list[MatchedOwner]

class Payload(BaseModel):
    name: str | None
    threshold: int = 95
    countries: list[str] = ['CN','US','TW','HK']
    datasets: list[str] = ['PEP-CURRENT','PEP-FORMER','PEP-LINKED','SAN-CURRENT','SAN-FORMER','RRE','POI','REL']

class Payloads(BaseModel):
    payloads: list[Payload]

class MatchedOwnerSummary(BaseModel):
    beneficial_owner_name: str
    ownership_percentage: float | None
    degree_of_separation: int | None
    matched_name: str | None = None
    resource_id: str | None = Field(exclude=True, default=None)
    match_confidence: int | None = None
    datasets: list[Dataset] | list[str] = []  # Default empty list

    @classmethod
    def from_matchedOwner(cls, matchedOwner: MatchedOwner) -> 'MatchedOwnerSummary':
        # Check if matches exist
        matches = matchedOwner.acurisMatchResults.results.matches
        first_match = matches[0] if matches else None
        
        return cls(
            beneficial_owner_name=matchedOwner.name,
            ownership_percentage=matchedOwner.ownershipPercentage,
            degree_of_separation=matchedOwner.degreeOfSeparation,
            matched_name=first_match.name if first_match else None,
            resource_id=first_match.resourceId if first_match else None,
            match_confidence=first_match.score if first_match else None,
            datasets=first_match.datasets if first_match else []
        )

class MatchedOwnerSummaries(BaseModel):
    owner_summaries: list[MatchedOwnerSummary]

# - GET ACURIS MATCHES - #

# Get matches from Acuris search API
def post_acuris_search(owner_name: str) -> AcurisMatchResults:
    payload = Payload(name=owner_name) # Build payload from owner name
    response  = requests.post(url=acuris_url,headers={"X-Api-Key": acuris_key},json=payload.model_dump()) # post to Acuris search endpoint
    response.raise_for_status() # handle errors in response
    # acuris_response = AcurisMatchResults(results=response.json()["results"]) # Serialise response body to results object in API response
    acurisResult = AcurisMatchResults(results=response.json()["results"])

    return acurisResult

# Function to add matches to ubo record
def acuris_match_owner(beneficial_owner: BeneficialOwner) -> MatchedOwner:
    matchedOwner = MatchedOwner.add_matches(
        beneficial_owner=beneficial_owner,
        acurisMatchResults=post_acuris_search(f"{beneficial_owner.name}").model_dump()
    )
    return matchedOwner

# Loop over owners and add matches to each ubo record
def acuris_match_owners(beneficial_owners: BeneficialOwners) -> MatchedOwners:
    matched_owners = MatchedOwners(matchedOwners=[acuris_match_owner(beneficial_owner) for beneficial_owner in beneficial_owners.beneficialOwners])
    return matched_owners

# Function to summarise data for ubo record
def make_owner_summary(matched_owner: MatchedOwner) -> MatchedOwnerSummary:
    owner_summary = MatchedOwnerSummary.from_matchedOwner(matchedOwner=matched_owner)
    return owner_summary

# Produce owner summary dataframe
def make_owner_summaries(matched_owners: MatchedOwners) -> MatchedOwnerSummaries:
    matched_owner_summaries = MatchedOwnerSummaries(
        owner_summaries=[make_owner_summary(matched_owner) for matched_owner in matched_owners.matchedOwners]
    )
    return matched_owner_summaries

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
