from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Any
from enum import Enum


# - CRAFT API - #
class GraphQlQuery(BaseModel):
    query: str
    variables: str | None

class GraphQlFragment(BaseModel):
    name: str
    on_type: str
    fields: str

class GraphQlVariables(BaseModel):
    id: int

# - CRAFT COMPANY - #
class CraftPayload(BaseModel):
    query: str
    variables: GraphQlVariables

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

class CraftCompanyUbo(BaseModel):
    id: int
    displayName: str
    shortDescription: str
    dnb: CraftDnb

class CraftCompanyDetails(BaseModel):
    id: int
    slug: str
    displayName: str
    shortDescription: str
    craftUrl: str
    logo: dict[str,str]
    companyType: str

class CraftCompany(BaseModel):
    company: dict[str,CraftCompanyDetails]

class CraftResponse(BaseModel):
    data: dict[str, CraftCompany]

# - ACURIS - #
class AcurisPayload(BaseModel):
    name: str | None
    threshold: int = 95
    countries: list[str] = ['IL','US']
    datasets: list[str] = ['PEP-CURRENT','PEP-FORMER','PEP-LINKED','SAN-CURRENT','SAN-FORMER','RRE','POI','REL']

class AcurisPayloads(BaseModel):
    payloads: list[AcurisPayload]

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

class MatchAddress(BaseModel):
    geography: str = Field(default='Unknown')
    city: str = Field(default='Unknown')

class AcurisMatch(BaseModel):
    qrCode: str = Field(exclude=True)
    resourceId: str = Field(exclude=True)
    score: int
    match: str = Field(exclude=True)
    name: str
    countries: list[str]
    addresses: list[MatchAddress] = Field(exclude=True)
    datesOfBirth: list[str] = Field(default=['Unknown'])
    gender: str = Field(default='Unknown')
    profileImage: str = Field(default='Not available')
    datasets: list[str]
    resourceUri: str = Field(exclude=True)
    version: int = Field(exclude=True)
    currentSanBodyIds: list[int] = Field(exclude=True)
    formerSanBodyIds: list[int] = Field(exclude=True)

class AcurisMatchResult(BaseModel):
    matchCount: int
    matches: list[AcurisMatch] = []

class AcurisMatchResults(BaseModel):
    results: AcurisMatchResult

class MatchedOwner(CraftBeneficialOwner):
    acurisMatchResults: AcurisMatchResults

    @classmethod
    def add_matches(cls, beneficial_owner: CraftBeneficialOwner, acurisMatchResults: AcurisMatchResults) -> 'MatchedOwner':
        return cls.model_validate({
            **beneficial_owner.model_dump(),
            "acurisMatchResult": acurisMatchResults
        })

class MatchedOwners(BaseModel):
    matchedOwners: list[MatchedOwner]


# - PREP FOR STREAMLIT - #
class OwnerSummary(BaseModel):
    owner_name: str = Field(validation_alias='name')
    ownership_percentage: float = Field(validation_alias='beneficialOwnershipPercentage')
    degree_of_separation: int = Field(validation_alias='degreeOfSeparation')

    model_config = ConfigDict(populate_by_name=False,extra='ignore')

class OwnerSummaries(BaseModel):
    ownerSummaries: list[OwnerSummary] = Field(validation_alias='matchedOwners')

    model_config = ConfigDict(populate_by_name=False,extra='ignore')



