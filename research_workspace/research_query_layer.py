import sqlite3
from pathlib import Path


DB_FILE = Path("data/aros_knowledge.db")


class AROSResearchWorkspace:
    """
    Research workspace layer.

    Provides researcher-focused queries.

    Version 1:
    - Highest relevance papers
    - Domain collections
    - Minimum score filtering
    - Recent literature
    - Literature review seed
    """

    def connect(self):
        return sqlite3.connect(DB_FILE)


    def remove_duplicates(self, rows):
        """
        Remove duplicate research outputs.

        Uses title as primary uniqueness key.
        Keeps first/highest ranked occurrence.
        """

        unique = {}
        
        for row in rows:
            title = row[0].lower().strip()

            if title not in unique:
                unique[title] = row

        return list(unique.values())


    def highest_relevance_papers(self, limit=10):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT title, source, research_domain, confidence
        FROM knowledge_objects
        ORDER BY confidence DESC
        LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()
        conn.close()

        return self.remove_duplicates(rows)


    def search_domain(self, keyword):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT title, source, research_domain, confidence
        FROM knowledge_objects
        WHERE 
            title LIKE ?
            OR research_domain LIKE ?
            OR ai_summary LIKE ?
        ORDER BY confidence DESC
        """, (
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
        ))

        rows = cursor.fetchall()
        conn.close()

        return self.remove_duplicates(rows)


    def papers_above_score(self, score):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT title, source, confidence
        FROM knowledge_objects
        WHERE confidence >= ?
        ORDER BY confidence DESC
        """, (score,))

        rows = cursor.fetchall()
        conn.close()

        return rows


    def literature_review_seed(self, topic, limit=20):

        results = self.search_domain(topic)

        return self.remove_duplicates(results)[:limit]
