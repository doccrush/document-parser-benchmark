# Benchmark documents

The five PDFs used in v0.1, with the parsing challenge each one targets. All are publicly available documents, included here for reproducible evaluation.

| Document | Type | Size | Parsing challenge |
|---|---|---:|---|
| `NIPS-2017-attention-is-all-you-need-Paper.pdf` | Multi-column academic paper | 0.6 MB | Two-column layout, inline math/equations, citations |
| `FY25_Q2_Consolidated_Financial_Statements.pdf` | Financial report | 3.1 MB | Dense numerical tables, structured data |
| `NVIDIA.pdf` | Technical / corporate report | 17.4 MB | Large multi-page file, mixed text and graphics |
| `the-state-of-enterprise-ai_2025-report.pdf` | Image-heavy industry report | 10.2 MB | Charts and full-page graphics, low text density |
| `CREC-2026-07-21-dailydigest.pdf` | Congressional Record | 0.4 MB | Dense formal English text, heading hierarchy |

## Notes

- **`CREC-2026-07-21-dailydigest`** is the U.S. **Congressional Record** (English), not a non-English daily digest. It is a work of the U.S. federal government and in the public domain.
- The **NIPS paper** ("Attention Is All You Need", Vaswani et al., 2017) is the canonical two-column academic test case.
- The **FY25 financial statements** and **NVIDIA** / **State of Enterprise AI** reports are publicly released corporate documents used here solely for parsing evaluation.

## Evaluation focus

Each document is scored per-parser on:

- Reading order
- Heading structure
- Table extraction
- OCR / text accuracy
- Markdown cleanliness & RAG readiness

See [`../../results/scoring-v0.1.md`](../../results/scoring-v0.1.md) for the scores.
