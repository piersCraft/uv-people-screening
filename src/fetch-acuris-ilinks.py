import os
from dotenv import load_dotenv
from pydantic import BaseModel


# Load environment variables
load_dotenv()
craft_key  = os.getenv("KEY_ACURIS_TEST")
acuris_url  = os.getenv("URL_ACURIS_INDIVIDUAL")

class SearchPayload(BaseModel):
    name: str
    threshold: int
    countries: list[str]
    datasets: list[str]



print(acuris_url)

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

