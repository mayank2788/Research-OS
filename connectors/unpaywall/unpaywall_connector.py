import os
import requests
from dotenv import load_dotenv

load_dotenv()


class UnpaywallConnector:
    """
    AROS Unpaywall Connector.

    Purpose:
    DOI → legal open access PDF resolver.
    """

    def __init__(self):
        self.name = "Unpaywall"

    def clean_doi(self, doi):
        doi = doi or ""
        doi = doi.replace("https://doi.org/", "")
        doi = doi.replace("http://doi.org/", "")
        return doi.strip()

    def resolve_pdf(self, doi, email=None):
        doi = self.clean_doi(doi)

        if not doi:
            return None

        email = email or os.getenv("UNPAYWALL_EMAIL", "research@example.com")

        url = f"https://api.unpaywall.org/v2/{doi}"

        try:
            response = requests.get(
                url,
                params={"email": email},
                timeout=20,
            )
            response.raise_for_status()
            data = response.json()

        except requests.exceptions.RequestException as error:
            print(f"Unpaywall request failed: {error}")
            return None

        location = data.get("best_oa_location") or {}

        return (
            location.get("url_for_pdf")
            or location.get("url")
            or None
        )
