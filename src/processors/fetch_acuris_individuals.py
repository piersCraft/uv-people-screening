import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Any
import requests
from requests import Response
from fetch_ubo import BeneficialOwners, get_beneficial_owners, get_individual_owners


# Load environment variables
load_dotenv()
acuris_key  = os.getenv("KEY_ACURIS_TEST")
acuris_url  = os.getenv('URL_ACURIS_INDIVIDUAL')

class AcurisSearchPayload(BaseModel):
    name: str = 'Unknown'
    threshold: int = 95
    countries: list[str] = ['IL','US','GB']
    datasets: list[str] = ['PEP-LINKED','POI','SAN-FORMER','SAN-CURRENT','RRE','REL']

class AcurisMatchAddress(BaseModel):
    geography: str | None
    city: str | None

class AcurisIndividualMatch(BaseModel):
    qrCode: str
    resourceId: str
    score: int
    match: str
    name: str
    addresses: list[AcurisMatchAddress]
    datesOfBirth: list[str | None]
    gender: str | None
    profileImage: str | None
    datasets: list[str]

class UboAcurisResult(BaseModel):
    owner_name: str | None = None
    matches: list[AcurisIndividualMatch] | None

class UboAcurisResults(BaseModel):
    match_results: list[UboAcurisResult] | None

    def add_results(self,uboAcurisResult: UboAcurisResult):
        """
        Method to add a single search response from Acuris
        """
        self.match_results.append(uboAcurisResult)

def search_acuris(payload) -> UboAcurisResult:
    response: Response = requests.post(
        url=acuris_url,
        headers={"X-Api-Key": acuris_key},
        json=payload
    )
    response_body: dict[str, Any ] = response.json()
    matches = UboAcurisResult(
        matches=response_body["results"]["matches"]
    )

    return matches


def get_individual_matches(individual_owners: BeneficialOwners) -> UboAcurisResults:
    
    individual_matches = UboAcurisResults(match_results=[])

    owner_names: list[str] = [beneficialOwner.name for beneficialOwner in individual_owners.beneficialOwners]
    for owner_name in owner_names:
        payload = AcurisSearchPayload(
            name=owner_name
        )
        owner_matches = search_acuris(payload.model_dump())
        individual_matches.add_results(owner_matches)
        

    return individual_matches

# Testing with Jfrog ID
def main():
    craft_id: int = 60903

    owners_raw  = get_beneficial_owners(craft_id) # Get all ubo
    individual_owners  = get_individual_owners(owners_raw) # Individuals only
    individual_matches = get_individual_matches(individual_owners).model_dump()

    print(individual_matches)

if __name__ == "__main__":
    main()
