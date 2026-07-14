import json
import re
import sqlite3
from pathlib import Path
from typing import Optional

DB_FILE = Path("data/aros_knowledge.db")
DB_FILE.parent.mkdir(exist_ok=True)


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


def knowledge_object_exists(obj) -> bool:
    normalized_doi = normalize_doi(getattr(obj, "doi", ""))

    if normalized_doi:
        return find_by_doi(normalized_doi) is not None

    return find_by_title(getattr(obj, "title", "")) is not None


def save_knowledge_object(obj) -> int:
    """
    Save a KnowledgeObject without creating an exact duplicate.

    Duplicate priority:
    1. Normalized DOI
    2. Exact normalized title when DOI is unavailable

    Returns the existing row ID for duplicates or the new row ID
    for newly inserted records.
    """
    data = obj.to_dict()

    normalized_doi = normalize_doi(data.get("doi"))

    if normalized_doi:
        existing = find_by_doi(normalized_doi)
    else:
        existing = find_by_title(data.get("title"))

    if existing:
        return int(existing[0])

    data["doi"] = normalized_doi

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
        json.dumps(data["authors"]),
        data["publication_year"],
        data["doi"],
        data["abstract"],
        json.dumps(data["keywords"]),
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
