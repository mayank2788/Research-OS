import json
import urllib.parse
import urllib.request


class OpenAccessResolver:
    """
    AROS Open Access Resolver v1.

    Uses legal open-access discovery only.
    Primary resolver:
    - Unpaywall API

    Requires:
    - DOI
    """

    def __init__(self):
        self.email = "research@example.com"

    def resolve_unpaywall(self, doi):
        if not doi:
            return None

        encoded = urllib.parse.quote(doi)

        url = (
            "https://api.unpaywall.org/v2/"
            + encoded
            + "?email="
            + self.email
        )

        try:
            with urllib.request.urlopen(url, timeout=15) as response:
                data = json.loads(response.read().decode())

            best = data.get("best_oa_location") or {}

            pdf_url = best.get("url_for_pdf")

            if pdf_url:
                return pdf_url

        except Exception:
            return None

        return None

    def resolve(self, paper):
        doi = paper.get("doi")
        return self.resolve_unpaywall(doi)


if __name__ == "__main__":
    resolver = OpenAccessResolver()

    print(
        resolver.resolve(
            {
                "doi": "10.1038/s41599-020-00600-4"
            }
        )
    )
