import json
import urllib.parse
import urllib.request


class OpenAlexOAResolver:
    """
    AROS OpenAlex Open Access Resolver.
    Resolves DOI metadata into legal OA PDF/landing URLs.
    """

    def resolve_by_doi(self, doi):
        if not doi:
            return None

        doi = doi.replace("https://doi.org/", "")
        url = "https://api.openalex.org/works/doi:" + urllib.parse.quote(doi)

        try:
            with urllib.request.urlopen(url, timeout=20) as response:
                data = json.loads(response.read().decode())

            best = data.get("best_oa_location") or {}
            if best.get("pdf_url"):
                return best.get("pdf_url")

            primary = data.get("primary_location") or {}
            if primary.get("pdf_url"):
                return primary.get("pdf_url")

            oa = data.get("open_access") or {}
            if oa.get("oa_url"):
                return oa.get("oa_url")

        except Exception:
            return None

        return None

    def resolve(self, paper):
        return self.resolve_by_doi(paper.get("doi"))


if __name__ == "__main__":
    print(
        OpenAlexOAResolver().resolve(
            {"doi": "10.3390/ijfs14060155"}
        )
    )
