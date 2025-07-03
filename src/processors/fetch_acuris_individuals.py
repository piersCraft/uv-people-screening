import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel


# Load environment variables
load_dotenv()
craft_key  = os.getenv("KEY_ACURIS_TEST")
acuris_url  = os.getenv("URL_ACURIS_INDIVIDUAL")

class AcurisPayload(BaseModel):
    name: str
    threshold: int
    countries: list[str]
    datasets: list[str]

class BeneficialOwner(BaseModel):
    name: str
    beneficiaryType: dict[str,str]
    address: dict[str,str]
    beneficialOwnershipPercentage: float
    degreeOfSeparation: int

class BeneficialOwners(BaseModel):
    beneficialOwners: list[BeneficialOwner]


def read_owner_names():
    with open("owners.json","r") as file:
        owners = json.load(file)

    return owners

example_search_string = """
{
    "name": "Yuqun Zeng",
    "threshold": 80,
    "countries": [
       "HK",
       "CN",
       "TW"
    ],
    "datasets": [
        "PEP-LINKED",
        "SAN-FORMER",
        "SAN-CURRENT",
        "REL",
        "RRE",
        "POI",
        "INS"
    ]
}
"""

# Testing with Jfrog ID
def main():
    print(read_owner_names())

if __name__ == "__main__":
    main()
