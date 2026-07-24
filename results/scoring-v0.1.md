# PDF Parser Benchmark — Scoring Sheet v0.1

> **AI-assisted preliminary scoring** based on the actual Markdown outputs in `results/`, **pending human review**.
> Weights: Reading Order 30% / Heading Structure 20% / Table Extraction 25% / OCR Quality 15% / Markdown Quality 10%. Each dimension scored 0–5.

## 1. Detail scores (0–5)

RO = Reading Order · HS = Heading Structure · TE = Table Extraction · OCR = OCR Quality · MD = Markdown Quality

| PDF | Tool | RO | HS | TE | OCR | MD |
|---|---|:---:|:---:|:---:|:---:|:---:|
| NIPS (two-column paper) | markitdown | 2 | 1 | 2 | 2 | 1 |
| | docling | 5 | 4 | 5 | 4 | 4 |
| | marker | 5 | 3 | 3 | 3 | 3 |
| | mineru | 5 | 5 | 2 | 5 | 4 |
| NVIDIA (technical report) | markitdown | 3 | 1 | 2 | 4 | 2 |
| | docling | 4 | 4 | 1 | 4 | 1 |
| | marker | N/A | N/A | N/A | N/A | N/A |
| | mineru | 4 | 3 | 1 | 3 | 4 |
| FY25 (financial statements) | markitdown | 2 | 1 | 1 | 2 | 2 |
| | docling | 5 | 5 | 4 | 5 | 5 |
| | marker | 4 | 4 | 2 | 5 | 3 |
| | mineru | 3 | 4 | 1 | 2 | 2 |
| state-of-enterprise-ai | markitdown | 2 | 1 | 2 | 4 | 2 |
| | docling | 0 | 0 | 0 | 0 | 0 |
| | marker | 4 | 4 | 4 | 4 | 4 |
| | mineru | 4 | 3 | 3 | 2 | 3 |
| CREC (Congressional Record) | markitdown | 1 | 1 | 1 | 2 | 1 |
| | docling | 4 | 2 | 4 | 4 | 3 |
| | marker | 5 | 5 | 3 | 5 | 5 |
| | mineru | 5 | 3 | 2 | 5 | 4 |

## 2. Weighted total (out of 5)

| PDF | markitdown | docling | marker | mineru |
|---|:---:|:---:|:---:|:---:|
| NIPS | 1.70 | 4.55 | 3.60 | 4.15 |
| NVIDIA | 2.40 | 2.95 | N/A | 2.90 |
| FY25 | 1.55 | 4.75 | 3.55 | 2.45 |
| state-of-enterprise-ai | 2.10 | 0.00 | 4.00 | 3.15 |
| CREC | 1.15 | 3.50 | 4.50 | 3.75 |
| **Weighted average** | **1.78** | **3.15** | **3.91\*** | **3.28** |
| # documents scored | 5 | 5 | 4 | 5 |

**Ranking: marker 3.91\* > mineru 3.28 > docling 3.15 > markitdown 1.78**

\* Marker was scored on only 4 PDFs (NVIDIA timed out with no output). **The sample is biased and not directly comparable** — it conveniently skipped the largest file.

## 3. Strengths / weaknesses per tool

### markitdown — weighted 1.78 (weakest)
- **Strengths:** Fastest by far (avg 1.7s); clean plain text with no base64 bloat.
- **Weaknesses:** Almost no Markdown structure (zero heading hierarchy); tables shattered and numbers polluted; severe missing-space concatenation in formulas and text (NIPS: `Thedominantsequencetransductionmodels...`, CREC: reversed/garbled text). **Not suitable as a primary RAG parser.**

### docling — weighted 3.15 (high ceiling, unstable)
- **Strengths:** **Best tables** (the only clean Markdown pipe table on the FY25 financial report, with correct values); best reading order and formula handling on the two-column paper (NIPS 4.55).
- **Weaknesses:** **Embeds images as base64 by default**, which turned the image-heavy `state-of-enterprise-ai` into an all-image, no-text output (0.00) and produced a 126 MB Markdown file for NVIDIA (MD=1). Image-heavy documents fail outright.

### marker — weighted 3.91* (best structure/layout, but slow and chokes on big files)
- **Strengths:** Most complete heading hierarchy and layout restoration (best on `state-of-enterprise-ai` and CREC); clear case/section semantics.
- **Weaknesses:** **NVIDIA (17 MB) exceeded the 1200s timeout with no output**; systematic table-row errors (header merged with the first row, section labels concatenated — FY25 TE=2); VLM inference is slow (avg 346s).

### mineru — weighted 3.28 (most balanced and stable)
- **Strengths:** **All 5 PDFs ran successfully**, with no catastrophic failure; best formula quality (NIPS math equations complete); strong reading order and CJK handling; **images referenced as standalone files (no base64 bloat — RAG-friendly)**.
- **Weaknesses:** **Tables are almost all HTML `<table>` instead of Markdown pipe tables** (unfriendly to pure-Markdown pipelines); financial-table values occasionally shift (FY25 TE=1); OCR occasionally misreads "AI" as "Al".

## 4. Data-quality notes (affect the scores — reported honestly)

1. **Docling base64 images:** The `state-of-enterprise-ai` (0.00) and NVIDIA (MD=1) results are caused by default base64 image embedding, not raw parsing ability. Rerunning with `--image-export-mode placeholder` should lift Docling's ranking noticeably.
2. **Marker NVIDIA timeout:** CPU VLM inference on a 17 MB multi-page file exceeded 1200s. Use `--mode fast` to avoid it (small accuracy trade-off).
3. **CREC is actually English:** `CREC-2026-07-21-dailydigest` is the U.S. Congressional Record (English), not a non-English daily digest. It was scored on its actual English content.

## 5. RAG selection guidance (for Phase 2)

- Want stability / general purpose → **mineru** (passes everything, balanced, no bloat)
- Want tables / financial docs → **docling** (after disabling base64)
- Want layout / structure → **marker** (accept slow + big-file timeout risk)
- Want speed / rough draft → **markitdown** (high quality cost)
