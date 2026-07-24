# Benchmark documents

The six PDFs used in v0.2 (five real-world documents from v0.1, plus a synthesized scanned document added in v0.2), each targeting a distinct parsing challenge. All are publicly available or CC0-dedicated, included here for reproducible evaluation.

| Document | Type | Size | Parsing challenge |
|---|---|---:|---|
| `NIPS-2017-attention-is-all-you-need-Paper.pdf` | Multi-column academic paper | 0.6 MB | Two-column layout, inline math/equations, citations |
| `FY25_Q2_Consolidated_Financial_Statements.pdf` | Financial report | 3.1 MB | Dense numerical tables, structured data |
| `NVIDIA.pdf` | Technical / corporate report | 17.4 MB | Large multi-page file, mixed text and graphics |
| `the-state-of-enterprise-ai_2025-report.pdf` | Image-heavy industry report | 10.2 MB | Charts and full-page graphics, low text density |
| `CREC-2026-07-21-dailydigest.pdf` | Congressional Record | 0.4 MB | Dense formal English text, heading hierarchy |
| `scanned-report-cc0.pdf` | **Scanned / OCR (v0.2)** | 0.3 MB | Image-only, no text layer — forces OCR |

## Notes

- **`CREC-2026-07-21-dailydigest`** is the U.S. **Congressional Record** (English), not a non-English daily digest. It is a work of the U.S. federal government and in the public domain.
- **`scanned-report-cc0.pdf`** is **synthesized** (`scripts/make_scanned_pdf.py`): a short CC0-dedicated text rendered to a noisy, slightly rotated, **image-only PDF with no text layer**, so parsers must OCR. Its exact source text is in `scanned-ground-truth.txt`, enabling objective OCR-accuracy scoring (`scripts/ocr_accuracy.py`).
- The **NIPS paper** ("Attention Is All You Need", Vaswani et al., 2017) is the canonical two-column academic test case.
- The **FY25 financial statements** and **NVIDIA** / **State of Enterprise AI** reports are publicly released corporate documents used here solely for parsing evaluation.

## Evaluation focus

Each document is scored per-parser on:

- Reading order
- Heading structure
- Table extraction
- OCR / text accuracy
- Markdown cleanliness & RAG readiness

See [`../../results/scoring-v0.2.md`](../../results/scoring-v0.2.md) for the v0.2 scores (and [`scoring-v0.1.md`](../../results/scoring-v0.1.md) for the v0.1 archive).
