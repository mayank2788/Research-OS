import re
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from knowledge.knowledge_object import KnowledgeObject
from repository.knowledge_repository import save_knowledge_object


def _clean_value(value: str) -> str:
    value = value.strip()

    if (
        len(value) >= 2
        and (
            (value[0] == "{" and value[-1] == "}")
            or (value[0] == '"' and value[-1] == '"')
        )
    ):
        value = value[1:-1]

    value = value.replace("\\&", "&")
    value = value.replace("\\_", "_")
    value = re.sub(r"[{}]", "", value)
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def _split_entries(text: str) -> Iterable[str]:
    index = 0
    length = len(text)

    while index < length:
        start = text.find("@", index)

        if start == -1:
            break

        opening = text.find("{", start)

        if opening == -1:
            break

        depth = 0
        in_quotes = False
        escaped = False
        end = opening

        while end < length:
            char = text[end]

            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_quotes = not in_quotes
            elif not in_quotes:
                if char == "{":
                    depth += 1
                elif char == "}":
                    depth -= 1

                    if depth == 0:
                        yield text[start:end + 1]
                        index = end + 1
                        break

            end += 1
        else:
            break


def _parse_fields(body: str) -> Dict[str, str]:
    fields: Dict[str, str] = {}
    index = 0
    length = len(body)

    while index < length:
        while index < length and body[index] in " \t\r\n,":
            index += 1

        if index >= length:
            break

        key_start = index

        while index < length and (
            body[index].isalnum()
            or body[index] in "_-"
        ):
            index += 1

        key = body[key_start:index].strip().lower()

        while index < length and body[index].isspace():
            index += 1

        if not key or index >= length or body[index] != "=":
            while index < length and body[index] != ",":
                index += 1
            continue

        index += 1

        while index < length and body[index].isspace():
            index += 1

        if index >= length:
            fields[key] = ""
            break

        if body[index] == "{":
            start = index
            depth = 0

            while index < length:
                if body[index] == "{":
                    depth += 1
                elif body[index] == "}":
                    depth -= 1

                    if depth == 0:
                        index += 1
                        break

                index += 1

            value = body[start:index]

        elif body[index] == '"':
            start = index
            index += 1
            escaped = False

            while index < length:
                char = body[index]

                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    index += 1
                    break

                index += 1

            value = body[start:index]

        else:
            start = index

            while index < length and body[index] != ",":
                index += 1

            value = body[start:index]

        fields[key] = _clean_value(value)

    return fields


def parse_bibtex_text(text: str) -> List[Dict[str, str]]:
    records: List[Dict[str, str]] = []

    for entry in _split_entries(text):
        header = re.match(
            r"@(?P<type>[A-Za-z]+)\s*\{\s*(?P<key>[^,]+),",
            entry,
            flags=re.DOTALL,
        )

        if not header:
            continue

        entry_type = header.group("type").strip().lower()
        citation_key = header.group("key").strip()

        body = entry[header.end():]
        body = body.rsplit("}", 1)[0]

        fields = _parse_fields(body)
        fields["entry_type"] = entry_type
        fields["citation_key"] = citation_key

        records.append(fields)

    return records


def parse_bibtex_file(path: str | Path) -> List[Dict[str, str]]:
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"BibTeX file not found: {file_path}"
        )

    return parse_bibtex_text(
        file_path.read_text(encoding="utf-8-sig")
    )


def _split_authors(author_text: str) -> List[str]:
    if not author_text:
        return []

    return [
        author.strip()
        for author in re.split(
            r"\s+and\s+",
            author_text,
            flags=re.IGNORECASE,
        )
        if author.strip()
    ]


def _split_keywords(keyword_text: str) -> List[str]:
    if not keyword_text:
        return []

    return [
        keyword.strip()
        for keyword in re.split(r"[;,]", keyword_text)
        if keyword.strip()
    ]


def record_to_knowledge_object(
    record: Dict[str, str],
    research_domain: str = "",
    source: str = "BibTeX Import",
) -> KnowledgeObject:
    title = record.get("title", "").strip()

    if not title:
        raise ValueError(
            "BibTeX record does not contain a title."
        )

    entry_type = record.get(
        "entry_type",
        "article",
    )

    return KnowledgeObject(
        title=title,
        source=source,
        source_type="Citation File Import",
        document_type=entry_type,
        research_domain=research_domain,
        authors=_split_authors(
            record.get("author", "")
        ),
        publication_year=record.get("year", ""),
        doi=record.get("doi", ""),
        abstract=record.get("abstract", ""),
        keywords=_split_keywords(
            record.get("keywords", "")
        ),
        pdf_link=(
            record.get("url", "")
            or record.get("eprint", "")
        ),
        open_access=False,
        status="imported",
        confidence=0.75,
        metadata={
            "citation_key": record.get(
                "citation_key",
                "",
            ),
            "entry_type": entry_type,
            "journal": record.get("journal", ""),
            "booktitle": record.get("booktitle", ""),
            "publisher": record.get("publisher", ""),
            "volume": record.get("volume", ""),
            "number": record.get("number", ""),
            "pages": record.get("pages", ""),
            "issn": record.get("issn", ""),
            "isbn": record.get("isbn", ""),
            "raw_record": dict(record),
        },
    )


def import_bibtex(
    path: str | Path,
    research_domain: str = "",
    source: str = "Google Scholar",
) -> Dict[str, object]:
    records = parse_bibtex_file(path)

    inserted_or_existing: List[int] = []
    failed: List[Tuple[str, str]] = []

    for record in records:
        try:
            obj = record_to_knowledge_object(
                record=record,
                research_domain=research_domain,
                source=source,
            )

            record_id = save_knowledge_object(obj)
            inserted_or_existing.append(record_id)

        except (TypeError, ValueError) as error:
            failed.append(
                (
                    record.get("citation_key", ""),
                    str(error),
                )
            )

    return {
        "source": source,
        "file": str(Path(path)),
        "records_found": len(records),
        "records_processed": len(
            inserted_or_existing
        ),
        "record_ids": inserted_or_existing,
        "failed": failed,
    }
