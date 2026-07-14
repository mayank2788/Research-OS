# AROS Module Registry

Date: 13 July 2026

| Module | Status | Notes |
|---|---|---|
| Reader | Verified | Reads PDF files and generates extracted-text reports |
| Knowledge Object | Verified | Creates structured Knowledge Objects |
| Repository | Verified | Stores Knowledge Objects in SQLite |
| Original Connector Framework | Verified | Base and mock connector flow operational |
| Profile | Verified | Research profile loads successfully |
| Scout | Verified | Discovery plan generation verified |
| app.py | Verified | Research library scanning and reporting verified |
| Local Live Research Pipeline | Verified | Local PDF → Reader → Knowledge Object → Repository |
| Connector Registry | Verified | Registers and lists supported connectors |
| Credential Manager | Verified | Supplies connector authentication configuration |
| Execution Manager | Verified | Executes connector requests with shared controls |
| Rate Limiter | Verified | Shared connector rate-limit foundation operational |
| Academic Connector Abstraction | Verified | Shared interface compiles successfully |
| Core Connector | Verified | Shared core connector compiles successfully |
| OpenAlex Connector | Verified | Health HTTP 200 and live search results verified |
| OpenAlex Automated Tests | Verified | Four connector tests executed and passed |
| Open Access Resolver | Verified | Import and compilation verified |
| Repository Ingestion Engine | Verified | Import and compilation verified |
| AROS Inspection Script | Verified | Shell syntax and complete execution passed |
| Journal Intelligence Data | Local Asset | Generated or externally acquired datasets retained locally and excluded from Git |
| Literature Knowledge Objects | Local Asset | 1,118 generated JSON objects present at verification and excluded from Git |
| AI Synthesis Layer | Proposed | Future research synthesis and reasoning layer |
| Research UI | Proposed | Future user-facing interaction layer |
| Repository Duplicate Detection | Verified | DOI and normalized-title duplicate detection; 5 automated tests passed |
