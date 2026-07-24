# Data-quality caveats — what actually broke

> The honest part of the benchmark. Most parser comparisons publish a tidy green table and hide the failures. We don't — these are the four findings that most change how you should read the v0.1 scores, and they're the reason "highest score" ≠ "best parser for you."

## 1. Docling embeds images as base64 by default — and it silently destroys two documents

Docling inlines every extracted image as a base64 string directly in the Markdown. On image-heavy documents this has two catastrophic effects:

- **`the-state-of-enterprise-ai_2025-report` scored 0.00.** So much of the page became embedded-image base64 that there was effectively no extractable text left — the parser "succeeded" but produced an output useless for RAG.
- **The NVIDIA report became a 126 MB Markdown file** (126,173,302 characters). That single file accounts for essentially all of Docling's bloated output total and drags up its average runtime.

This is a **default-settings problem, not a parsing-ability problem.** Rerunning with `--image-export-mode placeholder` (Docling references images as files instead of inlining them) should lift Docling's ranking substantially. We flag this rather than bury it, because a naive user following a "Docling scored well" recommendation would hit the same wall.

**Impact on scores:** `state-of-enterprise-ai` Docling = 0.00 across all dimensions; NVIDIA Docling MD (Markdown Quality) = 1.

## 2. Marker hangs for 20 minutes on a 17 MB file — and that biases its ranking

Marker uses a VLM (vision-language model) for layout understanding. On CPU, inference on the 17 MB, multi-page NVIDIA report exceeded the **1200-second timeout** and produced no output at all.

This biases Marker's headline score **upward**: it was scored on 4/5 documents while conveniently skipping the largest, hardest one. That's why its 3.91 average is marked with ⚠️ and is **not directly comparable** to the others. On a level playing field (all five documents), MinerU and Docling are the stronger overall choices.

`--mode fast` avoids the timeout at a small accuracy cost. A GPU run would also change this picture dramatically.

**Impact on scores:** Marker NVIDIA = N/A (excluded); Marker averages computed over 4 docs, not 5.

## 3. MinerU emits tables as HTML, not Markdown

MinerU was the most reliable parser — the only one besides MarkItDown to run all five documents with no disasters, and it references images as standalone files (no base64 bloat). But its tables come out as HTML `<table>` blocks rather than Markdown pipe tables.

If your RAG pipeline expects pure Markdown (many chunkers and embedders do), this means MinerU's tables may not be parsed as tables at all without a preprocessing step. For financial/data-heavy documents this cost it table-extraction scores (e.g. FY25 Table Extraction = 1).

This is a trade-off, not a defect — but it's the kind of thing you only discover after deployment, so we surface it here.

## 4. The "CREC daily digest" is actually the U.S. Congressional Record (in English)

`CREC-2026-07-21-dailydigest.pdf` is the **Congressional Record** — English-language proceedings of the U.S. Congress — not a non-English daily digest as the filename might suggest to some readers. It was scored on its actual English content (dense, formal text). We note this so anyone reproducing the test isn't confused about which language or content type they're evaluating.

---

## Why we report this

A benchmark that only shows the winners is an ad. The useful information — for anyone building a real RAG pipeline — is the failure mode of each tool, because that's what you'll hit in production. If you came here from a ranking table, treat the caveats above as the actual decision criteria:

| You care about… | Avoid | Prefer |
|---|---|---|
| Image-heavy PDFs | Docling (default settings) | Marker, MinerU |
| Large multi-page PDFs on CPU | Marker (timeout) | MinerU, Docling |
| Pure-Markdown table pipelines | MinerU (HTML tables) | Docling |
| Anything mission-critical | MarkItDown (low quality) | MinerU |

See [`scoring-v0.1.md`](./scoring-v0.1.md) for the full per-document scores and [`benchmark-v0.1.md`](./benchmark-v0.1.md) for the headline results.
