import json
import re
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

DB_FILE = Path("data/aros_knowledge.db")
DB_FILE.parent.mkdir(exist_ok=True)

STATUS_RANK = {
    "discovered": 10,
    "ingested": 20,
    "downloaded": 20,
    "enriched": 30,
    "evaluated": 40,
    "verified": 50,
}


def connect() -> sqlite3.Connection:
    return sqlite3.connect(DB_FILE)


def normalize_doi(doi: Optional[str]) -> str:
    """Return a consistent DOI value for comparison and storage."""
    value = str(doi or "").strip().lower()

    prefixes = (
        "https://doi.org/",
        "http://doi.org/",
        "http://dx.doi.org/",
        "doi:",
    )

    for prefix in prefixes:
        if value.startswith(prefix):
            value = value[len(prefix):]
            break

    return value.strip()


def normalize_title(title: Optional[str]) -> str:
    """Normalize a title for exact duplicate comparison."""
    value = str(title or "").strip().lower()
    value = re.sub(r"\s+", " ", value)
    return value


def initialize_database() -> None:
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS knowledge_objects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        source TEXT,
        source_type TEXT,
        document_type TEXT,
        research_domain TEXT,
        authors TEXT,
        publication_year TEXT,
        doi TEXT,
        abstract TEXT,
        keywords TEXT,
        pdf_link TEXT,
        open_access INTEGER,
        local_file TEXT,
        ai_summary TEXT,
        status TEXT,
        confidence REAL,
        date_added TEXT,
        raw_json TEXT
    )
    """)

    conn.commit()
    conn.close()


def find_by_doi(doi: Optional[str]):
    normalized = normalize_doi(doi)

    if not normalized:
        return None

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, title, doi, source, status
    FROM knowledge_objects
    WHERE LOWER(
        TRIM(
            REPLACE(
                REPLACE(
                    REPLACE(
                        REPLACE(doi, 'https://doi.org/', ''),
                        'http://doi.org/',
                        ''
                    ),
                    'http://dx.doi.org/',
                    ''
                ),
                'doi:',
                ''
            )
        )
    ) = ?
    ORDER BY id ASC
    LIMIT 1
    """, (normalized,))

    row = cursor.fetchone()
    conn.close()

    return row


def find_by_title(title: Optional[str]):
    normalized = normalize_title(title)

    if not normalized:
        return None

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, title, doi, source, status
    FROM knowledge_objects
    ORDER BY id ASC
    """)

    row = None

    for candidate in cursor.fetchall():
        if normalize_title(candidate[1]) == normalized:
            row = candidate
            break

    conn.close()

    return row


def get_knowledge_object_record(record_id: int) -> Optional[Dict[str, Any]]:
    conn = connect()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM knowledge_objects
    WHERE id = ?
    """, (record_id,))

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    record = dict(row)

    for field in ("authors", "keywords"):
        try:
            record[field] = json.loads(record.get(field) or "[]")
        except (json.JSONDecodeError, TypeError):
            record[field] = []

    record["open_access"] = bool(record.get("open_access"))

    return record


def knowledge_object_exists(obj) -> bool:
    normalized_doi = normalize_doi(getattr(obj, "doi", ""))

    if normalized_doi:
        return find_by_doi(normalized_doi) is not None

    return find_by_title(getattr(obj, "title", "")) is not None


def merge_unique(existing: Any, incoming: Any) -> List[str]:
    merged: List[str] = []

    for value in list(existing or []) + list(incoming or []):
        text = str(value or "").strip()

        if text and text not in merged:
            merged.append(text)

    return merged


def choose_longer(existing: Any, incoming: Any) -> str:
    existing_text = str(existing or "").strip()
    incoming_text = str(incoming or "").strip()

    if len(incoming_text) > len(existing_text):
        return incoming_text

    return existing_text


def choose_non_empty(existing: Any, incoming: Any) -> str:
    existing_text = str(existing or "").strip()
    incoming_text = str(incoming or "").strip()

    return existing_text or incoming_text


def advance_status(existing: Any, incoming: Any) -> str:
    existing_status = str(existing or "").strip().lower()
    incoming_status = str(incoming or "").strip().lower()

    if not existing_status:
        return incoming_status

    if not incoming_status:
        return existing_status

    existing_rank = STATUS_RANK.get(existing_status)
    incoming_rank = STATUS_RANK.get(incoming_status)

    if existing_rank is None and incoming_rank is None:
        return existing_status

    if existing_rank is None:
        return incoming_status

    if incoming_rank is None:
        return existing_status

    if incoming_rank > existing_rank:
        return incoming_status

    return existing_status


def merge_knowledge_object_data(
    existing: Dict[str, Any],
    incoming: Dict[str, Any],
) -> Dict[str, Any]:
    merged = {
        "title": choose_non_empty(existing.get("title"), incoming.get("title")),
        "source": choose_non_empty(existing.get("source"), incoming.get("source")),
        "source_type": choose_non_empty(
            existing.get("source_type"),
            incoming.get("source_type"),
        ),
        "document_type": choose_non_empty(
            existing.get("document_type"),
            incoming.get("document_type"),
        ),
        "research_domain": choose_non_empty(
            existing.get("research_domain"),
            incoming.get("research_domain"),
        ),
        "authors": merge_unique(
            existing.get("authors"),
            incoming.get("authors"),
        ),
        "publication_year": choose_non_empty(
            existing.get("publication_year"),
            incoming.get("publication_year"),
        ),
        "doi": normalize_doi(
            existing.get("doi") or incoming.get("doi")
        ),
        "abstract": choose_longer(
            existing.get("abstract"),
            incoming.get("abstract"),
        ),
        "keywords": merge_unique(
            existing.get("keywords"),
            incoming.get("keywords"),
        ),
        "pdf_link": choose_non_empty(
            existing.get("pdf_link"),
            incoming.get("pdf_link"),
        ),
        "open_access": bool(
            existing.get("open_access") or incoming.get("open_access")
        ),
        "local_file": choose_non_empty(
            existing.get("local_file"),
            incoming.get("local_file"),
        ),
        "ai_summary": choose_longer(
            existing.get("ai_summary"),
            incoming.get("ai_summary"),
        ),
        "status": advance_status(
            existing.get("status"),
            incoming.get("status"),
        ),
        "confidence": max(
            float(existing.get("confidence") or 0.0),
            float(incoming.get("confidence") or 0.0),
        ),
        "date_added": choose_non_empty(
            existing.get("date_added"),
            incoming.get("date_added"),
        ),
    }

    return merged


def records_differ(
    existing: Dict[str, Any],
    merged: Dict[str, Any],
) -> bool:
    comparable_fields = (
        "title",
        "source",
        "source_type",
        "document_type",
        "research_domain",
        "authors",
        "publication_year",
        "doi",
        "abstract",
        "keywords",
        "pdf_link",
        "open_access",
        "local_file",
        "ai_summary",
        "status",
        "confidence",
        "date_added",
    )

    for field in comparable_fields:
        existing_value = existing.get(field)
        merged_value = merged.get(field)

        if field == "doi":
            existing_value = normalize_doi(existing_value)

        if existing_value != merged_value:
            return True

    return False


def update_knowledge_object(
    record_id: int,
    merged: Dict[str, Any],
) -> None:
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE knowledge_objects
    SET
        title = ?,
        source = ?,
        source_type = ?,
        document_type = ?,
        research_domain = ?,
        authors = ?,
        publication_year = ?,
        doi = ?,
        abstract = ?,
        keywords = ?,
        pdf_link = ?,
        open_access = ?,
        local_file = ?,
        ai_summary = ?,
        status = ?,
        confidence = ?,
        date_added = ?,
        raw_json = ?
    WHERE id = ?
    """, (
        merged["title"],
        merged["source"],
        merged["source_type"],
        merged["document_type"],
        merged["research_domain"],
        json.dumps(merged["authors"], ensure_ascii=False),
        merged["publication_year"],
        merged["doi"],
        merged["abstract"],
        json.dumps(merged["keywords"], ensure_ascii=False),
        merged["pdf_link"],
        1 if merged["open_access"] else 0,
        merged["local_file"],
        merged["ai_summary"],
        merged["status"],
        merged["confidence"],
        merged["date_added"],
        json.dumps(merged, ensure_ascii=False),
        record_id,
    ))

    conn.commit()
    conn.close()


def save_knowledge_object(obj, return_status: bool = False):
    """
    Insert or update one canonical Knowledge Object.

    Identity priority:
    1. Normalized DOI
    2. Exact normalized title when DOI is unavailable

    Lifecycle behavior:
    - Insert a new canonical record when no match exists.
    - Merge improved metadata into an existing canonical record.
    - Advance lifecycle status without regression.
    - Preserve the existing record ID.

    Return status:
    - inserted: a new row was created
    - updated: an existing row received improved data
    - existing: an identical or non-improving duplicate was received
    """
    data = obj.to_dict()
    normalized_doi = normalize_doi(data.get("doi"))
    data["doi"] = normalized_doi

    if normalized_doi:
        existing_match = find_by_doi(normalized_doi)
    else:
        existing_match = find_by_title(data.get("title"))

    if existing_match:
        existing_id = int(existing_match[0])
        existing_record = get_knowledge_object_record(existing_id)

        if existing_record is None:
            raise RuntimeError(
                f"Existing repository record {existing_id} could not be read."
            )

        merged = merge_knowledge_object_data(existing_record, data)

        if records_differ(existing_record, merged):
            update_knowledge_object(existing_id, merged)
            repository_status = "updated"
        else:
            repository_status = "existing"

        if return_status:
            return {
                "record_id": existing_id,
                "status": repository_status,
            }

        return existing_id

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO knowledge_objects (
        title, source, source_type, document_type, research_domain,
        authors, publication_year, doi, abstract, keywords,
        pdf_link, open_access, local_file, ai_summary, status,
        confidence, date_added, raw_json
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["title"],
        data["source"],
        data["source_type"],
        data["document_type"],
        data["research_domain"],
        json.dumps(data["authors"], ensure_ascii=False),
        data["publication_year"],
        data["doi"],
        data["abstract"],
        json.dumps(data["keywords"], ensure_ascii=False),
        data["pdf_link"],
        1 if data["open_access"] else 0,
        data["local_file"],
        data["ai_summary"],
        data["status"],
        data["confidence"],
        data["date_added"],
        json.dumps(data, ensure_ascii=False),
    ))

    conn.commit()
    inserted_id = int(cursor.lastrowid)
    conn.close()

    if return_status:
        return {
            "record_id": inserted_id,
            "status": "inserted",
        }

    return inserted_id


def add_knowledge_object(obj) -> int:
    """
    Backward-compatible wrapper.

    Existing pipelines may continue calling add_knowledge_object().
    """
    return save_knowledge_object(obj)


def list_knowledge_objects():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, title, source, research_domain, status, date_added
    FROM knowledge_objects
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


def count_knowledge_objects() -> int:
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM knowledge_objects")
    count = int(cursor.fetchone()[0])

    conn.close()

    return count
