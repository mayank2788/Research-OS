# Reader Module Audit

## Module

reader/pdf_reader.py

## Purpose

Reads PDF documents from the Research Library.

## Current Capabilities

- Read PDF files
- Extract text
- Count pages
- Count words
- Estimate reading time
- Generate text preview
- Save report to extracted_text

## Input

Research-Papers directory

## Output

Text report in extracted_text/

## Dependencies

- Python 3.12
- pypdf 6.14.2

## Validation Performed

**Date:** 01 July 2026

**Test PDF:**
AN_APPROACH_TO_PERFORMANCE_OF_MFI_USING.pdf

**Result:**

- Pages: 5
- Words: 2027
- Estimated Reading Time: 10.1 minutes
- Status: Success

## Safety

- Original PDFs are never modified.
- Original PDFs are never renamed.
- Original PDFs are never deleted.

## Current Limitations

- Reads only text-based PDFs
- No OCR for scanned PDFs
- No PDF metadata extraction (Author, Title, Keywords)
- No image extraction
- Text preview limited to the first 1000 characters

## Verification Status

✅ Verified

## Next Planned Enhancements

- OCR support for scanned PDFs
- Metadata extraction
- Full text storage
- Language detection
- Better error reporting