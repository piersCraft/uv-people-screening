from src.ppl_screen_package.models import CraftBeneficialOwner, AcurisMatchResults, CraftBeneficialOwners
from pydantic import BaseModel

response_string = """
{
  "results": {
    "matchCount": 3,
    "matches": [
      {
        "qrCode": "811221",
        "resourceId": "fae660daa7c8528a577d16429bfa58d17efd50dad22430413af13aa28eba3cc5",
        "score": 100,
        "match": "Shlomi Ben Haim",
        "name": "Shlomi Ben Haim",
        "countries": ["IL"],
        "addresses": [
          {
            "geography": "IL",
            "city": "Kiryat Yam"
          }
        ],
        "datasets": ["RRE"],
        "currentSanBodyIds": [],
        "formerSanBodyIds": [],
        "version": 1625738255586,
        "resourceUri": "/individuals/fae660daa7c8528a577d16429bfa58d17efd50dad22430413af13aa28eba3cc5",
        "datesOfBirth": ["1975"],
        "gender": "Male",
        "profileImage": "https://www.acurisriskintelligence.com/cdn/content/0005645000/0005644482.jpg"
      },
      {
        "qrCode": "10329771",
        "resourceId": "38e5fcf2e9025acd64ed62b7fc8e2787dfea6be2b9af6125c1e398b16c6c4be9",
        "score": 97,
        "match": "Shlome Ben Haim",
        "name": "Shlomo Ben-Haim",
        "countries": ["IL"],
        "addresses": [
          {
            "geography": "IL",
            "city": "Givat Shmuel"
          }
        ],
        "datasets": ["REL", "RRE"],
        "currentSanBodyIds": [],
        "formerSanBodyIds": [],
        "version": 1652860502423,
        "resourceUri": "/individuals/38e5fcf2e9025acd64ed62b7fc8e2787dfea6be2b9af6125c1e398b16c6c4be9",
        "datesOfBirth": [],
        "gender": "Male"
      },
      {
        "qrCode": "4199076",
        "resourceId": "3792c859dd3296a528afabf073aaa5f509c2ca29a296a971b76d03cabc814749",
        "score": 95,
        "match": "Shlomo A Ben-Haim",
        "name": "Shlomo A Ben-Haim",
        "countries": ["IL", "GB"],
        "addresses": [
          {
            "geography": "IL",
            "city": "Haifa"
          },
          {
            "geography": "IL",
            "city": "Caesarea"
          },
          {
            "geography": "GB",
            "city": "London"
          }
        ],
        "datasets": ["PEP-LINKED", "REL", "RRE"],
        "currentSanBodyIds": [],
        "formerSanBodyIds": [],
        "version": 1699253884807,
        "resourceUri": "/individuals/3792c859dd3296a528afabf073aaa5f509c2ca29a296a971b76d03cabc814749",
        "datesOfBirth": ["1958"],
        "gender": "Male",
        "profileImage": "https://www.acurisriskintelligence.com/cdn/content/0020485000/0020484173.jpg"
      }
    ]
  }
}
"""
owners_string = """
{
  "beneficialOwners": [
    {
      "name": "Yaochu Yang",
      "beneficiaryType": { "description": "Individual" },
      "address": { "city": "Unknown", "country": "Unknown" },
      "beneficialOwnershipPercentage": 0.35,
      "degreeOfSeparation": 1
    },
    {
      "name": "Shaoteng Duan",
      "beneficiaryType": { "description": "Individual" },
      "address": { "city": "Unknown", "country": "Unknown" },
      "beneficialOwnershipPercentage": 0.3,
      "degreeOfSeparation": 1
    },
    {
      "name": "Zhong Wang",
      "beneficiaryType": { "description": "Individual" },
      "address": { "city": "Unknown", "country": "Unknown" },
      "beneficialOwnershipPercentage": 0.24,
      "degreeOfSeparation": 1
    },
    {
      "name": "Simo He",
      "beneficiaryType": { "description": "Individual" },
      "address": { "city": "Unknown", "country": "Unknown" },
      "beneficialOwnershipPercentage": 0.17,
      "degreeOfSeparation": 1
    },
    {
      "name": "Furong Mai",
      "beneficiaryType": { "description": "Individual" },
      "address": { "city": "Unknown", "country": "Unknown" },
      "beneficialOwnershipPercentage": 0.23,
      "degreeOfSeparation": 1
    }
  ]
}
"""
acuris_results = AcurisMatchResults.model_validate_json(response_string)
individual_owners = CraftBeneficialOwners.model_validate_json(owners_string)

class BaseObject(BaseModel):
    name: str
    age: int

class ExtendedObject(BaseObject):
    country: str

base_object = BaseObject(name='joe',age=21)
extended_object = ExtendedObject(**base_object.model_dump(),country='GB')

class ExtendedOwner(CraftBeneficialOwner):
    matches: list[str]

class ExtendedOwners(BaseModel):
    extendedOwners: list[ExtendedOwner]

def extend_owner(owner: CraftBeneficialOwner):
    extended_owner = ExtendedOwner(**owner.model_dump(),matches=['matchone','matchtwo'])
    return extended_owner

extended_owners = ExtendedOwners(extendedOwners=[extend_owner(owner) for owner in individual_owners.beneficialOwners]) 


print(extended_owners.model_dump())

