from connectors.unpaywall import UnpaywallConnector


class PDFResolver:
    """
    AROS PDF Resolver.

    Attempts legal PDF discovery:

    1. Existing KnowledgeObject pdf_link
    2. Unpaywall DOI lookup

    Future:
    - CORE
    - OpenAlex OA metadata
    - arXiv PDF conversion
    """

    def __init__(self):
        self.unpaywall = UnpaywallConnector()

    def resolve(self, knowledge_object):
        if knowledge_object.pdf_link:
            return knowledge_object.pdf_link

        if knowledge_object.doi:
            return self.unpaywall.resolve_pdf(
                knowledge_object.doi
            )

        return None
