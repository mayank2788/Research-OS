import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_FILE = Path("data/aros_knowledge.db")
DB_FILE.parent.mkdir(exist_ok=True)

def connect():
    return sqlite3.connect(DB_FILE)

def initialize_database():
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

def add_knowledge_object(obj):
    data = obj.to_dict()

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
        json.dumps(data, ensure_ascii=False)
    ))

    conn.commit()
    inserted_id = cursor.lastrowid
    conn.close()

    return inserted_id

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

def count_knowledge_objects():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM knowledge_objects")
    count = cursor.fetchone()[0]

    conn.close()
    return count
