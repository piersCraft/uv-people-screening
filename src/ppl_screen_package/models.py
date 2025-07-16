from pydantic import BaseModel, Field, field_validator
from typing import Any
from enum import Enum


# - API CONFIG - #
class ApiClient(BaseModel):
    url: str
    method: str
    headers: dict[str, str]
    payload: dict[str, Any]

class GraphQlQuery(BaseModel):
    query: str
    variables: str | None

class GraphQlFragment(BaseModel):
    name: str
    on_type: str
    fields: str

class Variables(BaseModel):
    id: int

# - CRAFT - #
class CraftPayload(BaseModel):
    query: str
    variables: Variables

class CraftBeneficiaryType(BaseModel):
    description: str = 'Unknown'

class CraftBeneficialOwnerAddress(BaseModel):
    city: str = Field(default='Unknown')
    country: str = Field(default='Unknown') 

class CraftBeneficialOwner(BaseModel):
    name: str
    beneficiaryType: CraftBeneficiaryType = Field(default_factory=CraftBeneficiaryType)
    address: CraftBeneficialOwnerAddress = Field(default_factory=CraftBeneficialOwnerAddress)
    beneficialOwnershipPercentage: float = Field(default=0)
    degreeOfSeparation: int = Field(default=0)

    @field_validator("address","beneficiaryType", mode="before")
    @classmethod
    def fill_missing_dicts(cls, v: Any) -> Any:
        if v is None:
            return {}
        return v

    @field_validator("beneficialOwnershipPercentage","degreeOfSeparation", mode="before")
    @classmethod
    def fill_missing_values(cls, v: Any) -> Any:
        if v is None:
            return 0
        return v

class CraftBeneficialOwners(BaseModel):
    beneficialOwners: list[CraftBeneficialOwner]

class CraftDnb(BaseModel):
    beneficialOwnershipStructure: CraftBeneficialOwners

class SubjectCompanyUbo(BaseModel):
    id: int
    displayName: str
    shortDescription: str
    dnb: CraftDnb

class SubjectCompany(BaseModel):
    id: int
    slug: str
    displayName: str
    shortDescription: str
    craftUrl: str
    logo: dict[str,str]
    companyType: str

class CraftCompany(BaseModel):
    company: dict[str,SubjectCompany]

class BeneficialOwner(BaseModel):
    name: str
    beneficiaryType: str | None
    country: str | None
    ownershipPercentage: float | None
    degreeOfSeparation: int | None

class BeneficialOwners(BaseModel):
    beneficialOwners: list[BeneficialOwner]

class CraftResponse(BaseModel):
    data: dict[str, CraftCompany]

# - ACURIS - #
class Payload(BaseModel):
    name: str | None
    threshold: int = 95
    countries: list[str] = ['CN','US','TW','HK']
    datasets: list[str] = ['PEP-CURRENT','PEP-FORMER','PEP-LINKED','SAN-CURRENT','SAN-FORMER','RRE','POI','REL']

class Payloads(BaseModel):
    payloads: list[Payload]

class Dataset(str, Enum):
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

class AcurisMatch(BaseModel):
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
    matches: list[AcurisMatch | None]

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
