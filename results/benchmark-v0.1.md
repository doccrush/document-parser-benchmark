# Document Parser Benchmark v0.1


## Overview

Initial comparison of open-source document parsing tools.

Tested:

- Microsoft MarkItDown
- Marker
- Docling
- MinerU


## Test Cases

| Category | Description |
|-|-|
| Simple PDF | Text document |
| Multi-column | Academic paper |
| Tables | Financial report |
| OCR | Scanned document |


## Evaluation

### Reading Order

| Tool | Score |
|-|-|
| Marker | ⭐⭐⭐⭐⭐ |
| Docling | ⭐⭐⭐⭐ |
| MinerU | ⭐⭐⭐⭐ |
| MarkItDown | ⭐⭐⭐ |


### Table Extraction

| Tool | Score |
|-|-|
| Marker | ⭐⭐⭐⭐ |
| Docling | ⭐⭐⭐⭐ |
| MinerU | ⭐⭐⭐⭐ |


## Notes

Document structure preservation is critical for RAG pipelines.

Incorrect hierarchy often leads to:

- bad chunks
- incomplete retrieval
- incorrect answers
