# AROS AI Handoff

Date: 13 July 2026

This file allows ChatGPT, Claude, Gemini, Cursor or any future AI assistant to resume AROS development consistently.

## Project

AROS — AI Research Operating System

AROS is an AI-native research platform supporting academic research, finance, accounting, taxation, economics, management, corporate governance, public policy and knowledge management.

## Authoritative Context

The Research-OS repository and its docs folder are the authoritative project record.

Do not rely only on conversation memory from ChatGPT, Clher AI system.

## Architecture Rule

Do not redesign the architecture unless explicitly instructed.

Preserve:

Source
↓
Connector
↓
Knowledge Object
↓
Repository
↓
Future AI Layer

## Current Committed Baseline

8ca535a — Migrate OpenAlex connector to shared framework

## Pending Verified Milestone

A Baseline 0.3 candidate is prepared locally and verified but not yet committed.

It includes:

- Academic connector abstraction.
- Core connector.
- OpenAlex connector using the shared framework.
- Connector registry integration.
- Credential manager integration.
- Execution manager integration.
- Rate limiting and retry support.
- Open Access Resolver.
- Repository Ingestion Engine.
- Automated connector tests.
- AROS inspection script.
- Updated Git ignore rules for generated research outputs.

## Verification Completed

- Shell syntax passed.
- Inspection script execution passed.
- Python compilation passed.
- Four automated connectorsed.
- OpenAlex health check returned HTTP 200.
- OpenAlex search returned live results.

## Verified Existing Modules

- Reader.
- Knowledge Object.
- Repository.
- Connector Framework.
- Profile.
- Scout.
- app.py.
- Local Live Research Pipeline.
- OpenAlex Academic Connector.

## Local Generated Assets

Generated journal datasets and literature Knowledge Objects are retained locally and excluded from Git.

They must not be added automatically to commits.

## Immediate Next Action

Review the staged file list, commit the verified Baseline 0.3 milestone and push to origin/main.

## Development Rules

- One objective at a time.
- Audit before change.
- Do not rewrite verified modules unnecessarily.
- Test before calling implementation complete.
- Update documentation alongside meaningful milestones.
- Distinguish achieved implementation from proposed work.
- Keep connectors, Knowledge Objects, repositories and future AI modules loosely coupled.

## Latest Repository Milestone

Repository v1.1 adds duplicate-safe persistence without changing existing connector or pipeline interfaces.

Current duplite rules:

1. Normalized DOI match.
2. Exact normalized-title match only when DOI is unavailable.

`add_knowledge_object()` remains available for backward compatibility and now delegates to `save_knowledge_object()`.

Historical duplicates have not yet been modified or removed.

## Citation Import

AROS now supports BibTeX citation-file imports.

Primary workflow:

Google Scholar, Zotero, Scopus, Web of Science or another citation tool
→ BibTeX export
→ BibTeX importer
→ Knowledge Object
→ duplicate-safe repository

Google Scholar is not scraped automatically. Its records enter through user-authorised exports.

## OpenAlex Metadata Mapper

OpenAlex records are now converted into Knowledge Objects through a dedicated mapper.

The mapper preserves:

- reconstructed abstract, when available;
- OpenAlex and DOI identifiers;
- authors;
- keywords and topics;
- journal and publisher metadata;
- ISSN;
- PDF and landing-page links;
- open-access metadata;
- citation and reference counts;
- language and retraction status;
- raw OpenAlex record.

The connector remains responsible for API communication. The mapper is responsible for metadata transformation.

## Canonical Repository Lifecycle Milestone

The repository now acts as the canonical lifecycle store for Knowledge Objects.

Identity order:

1. Normalized DOI.
2. Exact normalized title only when DOI is unavailable.

Persistence outcomes:

- `inserted` — a new canonical row was created.
- `updated` — an existing canonical row received improved metadata or advanced lifecycle state.
- `existing` — the incoming object did not improve the canonical record.

Lifecycle progression currently recognises:

discovered → ingested/downloaded → enriched → evaluated → verified

Merge behaviour includes:

- union of authors and keywords;
- preservation of the longer abstract and AI summary;
- preservation of existing non-empty source metadata;
- retention of PDF and local-file paths;
- logical promotion of open-access status;
- retention of the highest confidence;
- prevention of lifecycle regression;
- preservation of the existing repository record ID.

`add_knowledge_object()` remains available for backward compatibility.

Historical duplicate migration and database uniqueness constraints remain proposed and must be completed only after a verified backup and migration procedure.
