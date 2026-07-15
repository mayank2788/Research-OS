# AROS Current Architecture

Date: 13 July 2026

## Architectural Principle

AROS uses a modular research pipeline:

Source
↓
Connector
↓
Knowledge Object
↓
Repository
↓
Future AI Layer

External research sources must enter AROS through an appropriate connector.

## Existing Core Modules

- reader/
- knowledge/
- repository/
- connectors/
- connector_framework/
- literature_acquisition/
- profile/
- scout/
- journal_intelligence/
- tools/
- app.py

## Local Document Pipeline

Local PDF
↓
Reader
↓
Knowledge Object
↓
SQLite Repository

Status: Verified.

## Academic Connector Pipeline

Academic Source
↓
Academic Connector
↓
Connector Execution Manager
↓
Knowledge Object / Acquisition Processor
↓
Repository

Status: Foundation and OpenAlex c Shared Connector Framework

The shared framework currently includes:

- Connector registry.
- Credential manager.
- Execution manager.
- Rate limiter.
- Retry support.
- Academic connector abstraction.
- Core connector.
- OpenAlex connector.

## Literature Acquisition Components

Current components include:

- DOAJ Article Connector.
- OpenAlex Open Access Resolver.
- Open Access Resolver.
- Corpus Audit.
- Knowledge Enrichment Engine.
- Knowledge Object Bridge.
- Repository Ingestion Engine.

Some components pre-date the current milestone; the new resolver and repository ingestion modules have passed import and compilation verification.

## Journal Intelligence

Journal intelligence contains:

- Raw-source datasets.
- Normalized datasets.
- Merged journal database.
- Domain-filtered journal data.

These datasets are local research assets and are excluded from Git because of their generated or externally acquired nature.

## Verified Modules

- Reader.
- Knowledge Object.
- Repository.
- Connector Framework.
- Profile.
- Scout.
- app.py.
- Local Live Research Pipeline.
- OpenAlex Academic Connector.
- AROS Inspection Script.

## Proposed Future Layer

- AI-assisted synthesis.
- Research relevance scoring.
- Domain-specific intelligence.
- Cross-source deduplication and provenance enhancement.
- Research user interfaces.

These are proposed and must not be described as implemented.

## Canonical Repository Lifecycle

The repository layer now supports canonical lifecycle persistence:

Source
↓
Connector
↓
Knowledge Object
↓
Identity Resolution
↓
Canonical Repository Record
↓
Metadata Merge and Lifecycle Progression
↓
Future AI Layer

Repository identity priority:

1. Normalized DOI.
2. Exact normalized title when DOI is unavailable.

For an existing canonical record, AROS retains the existing record ID and merges improved metadata rather than creating a new row.

Recognised lifecycle progression:

discovered → ingested/downloaded → enriched → evaluated → verified

Repository outcomes are explicitly reported as:

- inserted;
- updated;
- existing.

Historical duplicate cleanup and database uniqueness enforcement reon work and are not yet part of the verified architecture.

## Repository Integrity Enforcement

The canonical repository is now protected by database-level integrity controls.

Implemented:

- canonical duplicate migration;
- lifecycle-aware metadata consolidation;
- deletion of redundant historical rows;
- unique normalized DOI enforcement;
- normalized title indexing;
- pre- and post-migration SQLite integrity verification.

The repository currently contains 1,137 canonical Knowledge Object records after migration.
