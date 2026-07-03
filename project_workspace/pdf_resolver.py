from connectors.unpaywall import UnpaywallConnector


class PDFResolver:
    """
    AROS PDF Resolver.

    Attempts legal PDF discovery:

    1. Direct PDF link
    2. arXiv PDF conversion
    3. Unpaywall DOI lookup
    4. Fallback landing page only if no better option exists
    """

    def __init__(self):
        self.unpaywall = UnpaywallConnector()

    def is_pdf_url(self, url):
        if not url:
            return False

        text = url.lower()

        return (
            text.endswith(".pdf")
            or "/pdf/" in text
            or "pdf" in text
        )

    def convert_arxiv_url(self, url):
        if not url:
            return None

        if "arxiv.org/abs/" in url:
            return url.replace(
                "arxiv.org/abs/",
                "arxiv.org/pdf/"
            ) + ".pdf"

        return None

    def resolve(self, knowledge_object):
        existing = knowledge_object.pdf_link or ""

        if self.is_pdf_url(existing):
            return existing

        arxiv_pdf = self.convert_arxiv_url(existing)
        if arxiv_pdf:
            return arxiv_pdf

        if knowledge_object.doi:
            unpaywall_pdf = self.unpaywall.resolve_pdf(
                knowledge_object.doi
            )

            if unpaywall_pdf:
                return unpaywall_pdf

        return existing or None
