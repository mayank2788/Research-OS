from typing import Any, Dict, List, Optional

from knowledge.knowledge_object import KnowledgeObject


def reconstruct_abstract(
    inverted_index: Optional[Dict[str, List[int]]],
) -> str:
    """
    Reconstruct plain abstract text from an OpenAlex inverted index.
    """
    if not inverted_index:
        return ""

    positioned_words = []

    for word, positions in inverted_index.items():
        for position in positions:
            positioned_words.append((int(position), word))

    positioned_words.sort(key=lambda item: item[0])

    return " ".join(
        word for _, word in positioned_words
    ).strip()


def extract_authors(record: Dict[str, Any]) -> List[str]:
    authors = []

    for authorship in record.get("authorships") or []:
        author = authorship.get("author") or {}
        name = str(
            author.get("display_name") or ""
        ).strip()

        if name:
            authors.append(name)

    return list(dict.fromkeys(authors))


def extract_keywords(
    record: Dict[str, Any],
    query: str = "",
) -> List[str]:
    keywords = []

    if query.strip():
        keywords.append(query.strip())

    for item in record.get("keywords") or []:
        if isinstance(item, dict):
            value = (
                item.get("display_name")
                or item.get("keyword")
                or ""
            )
        else:
            value = str(item)

        value = str(value).strip()

        if value:
            keywords.append(value)

    for topic in record.get("topics") or []:
        value = str(
            (topic or {}).get("display_name") or ""
        ).strip()

        if value:
            keywords.append(value)

    return list(dict.fromkeys(keywords))


def extract_pdf_link(record: Dict[str, Any]) -> str:
    locations = [
        record.get("best_oa_location") or {},
        record.get("primary_location") or {},
    ]

    locations.extend(record.get("locations") or [])

    for location in locations:
        pdf_url = str(
            (location or {}).get("pdf_url") or ""
        ).strip()

        if pdf_url:
            return pdf_url

    for location in locations:
        landing_url = str(
            (location or {}).get(
                "landing_page_url"
            ) or ""
        ).strip()

        if landing_url:
            return landing_url

    return ""


def extract_journal(record: Dict[str, Any]) -> str:
    primary_location = (
        record.get("primary_location") or {}
    )
    source = primary_location.get("source") or {}

    return str(
        source.get("display_name") or ""
    ).strip()


def map_openalex_record(
    record: Dict[str, Any],
    research_domain: str = "",
    source: str = "OpenAlex",
) -> KnowledgeObject:
    """
    Convert one OpenAlex work record into a KnowledgeObject.
    """
    open_access = record.get("open_access") or {}
    ids = record.get("ids") or {}
    primary_location = (
        record.get("primary_location") or {}
    )
    primary_source = (
        primary_location.get("source") or {}
    )

    doi = (
        record.get("doi")
        or ids.get("doi")
        or ""
    )

    abstract = reconstruct_abstract(
        record.get("abstract_inverted_index")
    )

    metadata = {
        "openalex_id": record.get("id", ""),
        "ids": ids,
        "journal": extract_journal(record),
        "issn_l": primary_source.get("issn_l", ""),
        "issn": primary_source.get("issn", []),
        "publisher": primary_source.get(
            "host_organization_name",
            "",
        ),
        "publication_date": record.get(
            "publication_date",
            "",
        ),
        "language": record.get("language", ""),
        "cited_by_count": record.get(
            "cited_by_count",
            0,
        ),
        "referenced_works_count": record.get(
            "referenced_works_count",
            0,
        ),
        "is_retracted": bool(
            record.get("is_retracted", False)
        ),
        "has_fulltext": bool(
            record.get("has_fulltext", False)
        ),
        "open_access": open_access,
        "primary_location": primary_location,
        "best_oa_location": record.get(
            "best_oa_location"
        ),
        "raw_record": record,
    }

    return KnowledgeObject(
        title=str(
            record.get("title")
            or record.get("display_name")
            or ""
        ).strip(),
        source=source,
        source_type="Academic API",
        document_type=str(
            record.get("type")
            or "Journal Article"
        ),
        research_domain=research_domain,
        authors=extract_authors(record),
        publication_year=str(
            record.get("publication_year") or ""
        ),
        doi=str(doi).strip(),
        abstract=abstract,
        keywords=extract_keywords(
            record,
            research_domain,
        ),
        pdf_link=extract_pdf_link(record),
        open_access=bool(
            open_access.get("is_oa", False)
        ),
        status="discovered",
        confidence=0.85,
        metadata=metadata,
    )
