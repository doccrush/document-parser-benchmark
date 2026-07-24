# Reproducing the benchmark

This document explains how to install the four parsers, run the benchmark, and reproduce the v0.1 numbers.

## Prerequisites

- Python 3.11
- [`uv`](https://docs.astral.sh/uv/) (used to install each parser in its own isolated environment)
- macOS or Linux. The v0.1 timings were measured **on a CPU-only machine** — GPU acceleration (notably for Marker's VLM) would substantially change the speed column.

## Why isolated installs

The four parsers pull in conflicting versions of shared dependencies (`pillow`, `transformers`, `pdfminer.six`). Installing them all into one Python environment leads to version conflicts. The robust approach is one isolated environment per tool via `uv tool`, which gives each its own bin on `PATH`.

## Installing the parsers

```bash
uv tool install 'markitdown[pdf]'          # CLI: markitdown
uv tool install docling                     # CLI: docling
uv tool install marker-pdf                  # CLI: marker_single
uv tool install 'mineru[pipeline]'          # CLI: mineru  (the [pipeline] extra pulls torch)
```

### Gotchas (these cost real time — read first)

**Marker 2.0 needs `llama.cpp`.** Its `surya` model backend requires the `llama-server` binary, otherwise non-text-only PDFs fail with `SpawnError: llama-server binary not found`:

```bash
brew install llama.cpp
```

**MinerU is missing a transitive dependency.** Its dependency manifest omits `six`, so the first run dies with `No module named 'six'`. Install it into MinerU's isolated env manually:

```bash
uv pip install --python "$(uv tool dir)/mineru/bin/python" six
```

**Docling has no `--output-dir`.** The runner handles this by setting the working directory. If you call Docling manually, it's a subcommand: `docling convert <pdf> --to md`.

## Running the benchmark

From the repo root:

```bash
python scripts/run_benchmark.py --timeout 1200
```

Options:

| Flag | Default | Purpose |
|---|---|---|
| `--tools` | all | Comma-separated subset, e.g. `--tools mineru,docling` |
| `--timeout` | 600 | Per-PDF timeout in seconds. v0.1 used 1200 (Marker needs it for large files). |
| `--skip-existing` | off | Resume: skip PDFs that already have non-empty output |
| `--keep-raw` | off | Keep the nested raw output dirs (marker/mineru/docling) |

The runner writes `results/benchmark-report.md` and `results/benchmark-report.csv`.

### Pointing at custom binaries

If a parser's CLI isn't on `PATH`, the runner reads an env var for each tool and falls back to `PATH`:

```
MARKITDOWN_BIN, DOCLING_BIN, MARKER_BIN, MINERU_BIN
```

## Scoring

The runner only measures **speed and reliability** (success/failure, time, output size). The **quality scores** in [`results/scoring-v0.1.md`](results/scoring-v0.1.md) are an AI-assisted preliminary assessment of the Markdown outputs, weighted across five dimensions for RAG relevance. To re-score after a rerun, open the per-tool outputs under `results/<tool>/` and reapply the rubric.

## Reducing the v0.1 biases

The two biggest biases in v0.1 are documented in [`results/caveats.md`](results/caveats.md). To remove them on a rerun:

- **Docling base64 bloat** → pass `--image-export-mode placeholder` (Docling's CLI). This requires a small change in `run_docling()`; contributions welcome.
- **Marker large-file timeout** → pass `--mode fast` to `marker_single`.
