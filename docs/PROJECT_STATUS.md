# AROS Project Status

Date: 13 July 2026

## Current Git Baseline

8ca535a — Migrate OpenAlex connector to shared framework

A new verified connector-framework milestone is prepared locally but has not yet been committed.

## Current Stage

Baseline 0.3 Candidate — Shared academic connector framework and OpenAlex integration verified.

## Achieved

- Cursor, Git, GitHub and Python 3.12.8 environment verified.
- Reader module verified.
- Knowledge Object module verified.
- Repository module verified.
- Original Connector Framework verified.
- Profile module audited and verified.
- Scout module audited and verified.
- app.py audited and verified.
- Local PDF → Reader → Knowledge Object → SQLite Repository pipeline verified.
- Shared connector registry implemented.
- Credential manager implemented.
- Connector execution manager implemented.
- Rate limiter and retry foundation implemented.
- Cor connector abstraction implemented.
- OpenAlex connector migrated to the shared framework.
- OpenAlex health check verified with HTTP 200.
- OpenAlex search verified with live results.
- Open Access Resolver implemented.
- Repository Ingestion Engine implemented.
- Automated connector tests created and verified.
- AROS project inspection script implemented and verified.
- Generated datasets and literature Knowledge Objects excluded from Git.

## Verified Connector Tests

- Connector registry initialization.
- Connector foundation initialization.
- OpenAlex health check.
- OpenAlex search result retrieval.

Result:

- 4 tests executed.
- 4 tests passed.
- Python compilation passed.
- Shell inspection script syntax and execution passed.

## Preserved Architecture

Source
↓
Connector
↓
Knowledge Object
↓
Repository
↓
Future AI Layer

## Generated Local Research Assets

The following are retained locally but excluded from Git:

- Journal intelligence raw-source datasets.
- Journal intelligence processets.
- Domain-filtered journal datasets.
- Generated literature Knowledge Objects.

## Current Rule

One objective at a time.

Plan → Inspect → Understand → Document → Implement → Test → Verify → Update Docs → Commit → Push

## Next Objective

Complete the Baseline 0.3 commit and push.

After the baseline is frozen, select one connector-intelligence objective without redesigning verified architecture.

## Repository v1.1 — Duplicate-Safe Saving

Implemented and verified:

- DOI normalization.
- DOI-based duplicate detection.
- Exact normalized-title duplicate detection when DOI is unavailable.
- Duplicate-safe `save_knowledge_object()` behaviour.
- Backward-compatible `add_knowledge_object()` wrapper.
- Existing row ID returned when an exact duplicate is detected.
- Isolated automated repository tests using temporary SQLite databases.

Verification:

- Repository tests: 5 passed.
- Connector tests: 4 passed.
- Python compilation passed.
- Git diff validation passed.

Historical duplicate records remain unchanged. The new behaviour prevents additional exact duplicates through current repository call sites.

## BibTeX Citation Import

Implemented and verified:

- General BibTeX file parser using the Python standard library.
- Conversion of BibTeX records into Knowledge Objects.
- Import through the duplicate-safe repository.
- Support for Google Scholar BibTeX exports.
- Compatibility with BibTeX exports from Zotero, Scopus, Web of Science and other citation tools.
- Preservation of citation key, journal, publisher, volume, issue, pages, ISSN, ISBN and raw imported metadata.
- Knowledge Object metadata field added for extensible source metadata.

Verification:

- BibTeX importer tests: 3 passed.
- Repository tests: 5 passed.
- Connector tests: 4 passed.
- Python compilation passed.
- Git diff validation passed.

Google Scholar is integrated through user-authorised citation export and import. Automated Google Scholar scraping is not used.
