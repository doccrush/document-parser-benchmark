# From PDF to RAG: where parsing quality decides everything

The document parser is the first link in a RAG pipeline, and it's the one that's hardest to undo. Everything downstream — chunking, embedding, retrieval, generation — inherits the parser's mistakes. A retrieval model can't find a table that the parser shattered; an LLM can't reason over numbers that were concatenated without spaces.

## The pipeline

```
 ┌──────┐    ┌────────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌────────┐    ┌─────┐
 │ PDF  │───▶│   Parser   │───▶│ Markdown │───▶│ Chunking │───▶│ Embedding│───▶│ Vector │───▶│ LLM │
 └──────┘    └────────────┘    └──────────┘    └──────────┘    └──────────┘    │   DB   │    └─────┘
                                   │                                              └────────┘
                                   └─── headings, lists, tables, reading order ───┘
                                        (the structure retrieval depends on)
```

Structured Markdown survives chunking and embedding far better than flat text, because headings, lists, and tables give the chunker semantic boundaries to cut on.

## Where parser quality actually bites RAG

This benchmark's failure modes map directly onto RAG failure modes:

| Parser failure (observed in this benchmark) | What it does to your RAG pipeline |
|---|---|
| Tables shattered / numbers polluted (MarkItDown on the FY25 financial report) | Numeric questions retrieve garbage; the LLM answers with wrong figures |
| Reading order scrambled in two-column layout | Chunks mix left- and right-column text; retrieval returns incoherent passages |
| Heading hierarchy flattened (MarkItDown) | No structure to chunk on; oversized, unfocused chunks; worse recall |
| Images embedded as 126 MB of base64 (Docling, default) | Chunks become walls of encoded text; embedding cost explodes, signal vanishes |
| Math/equations concatenated without spaces (`Thedominantsequencetransductionmodels…`) | Keyword and semantic search both miss the term; the passage is unretrievable |
| Tables emitted as raw HTML `<table>` (MinerU) | A Markdown-only chunker may not recognize rows as a table at all |

## Why this benchmark exists

Most RAG tutorials hand you a clean Markdown file and skip the parser entirely. In production, the PDF is messy, and the parser's output is the foundation everything stands on. Picking a parser that preserves structure — tables, reading order, headings — is the highest-leverage decision in the pipeline. That's what we measure here.

## Practical takeaways

- **Structure beats raw text.** Prefer a parser that preserves headings and tables over one that's merely fast. The chunker and embedder can't recover structure that was lost upstream.
- **Watch the output, not just the success flag.** Several parsers here "succeeded" while producing output useless for RAG (base64 walls, empty pages, garbled text). Inspect the Markdown before indexing it.
- **Match the parser to the document.** No single parser won every category — see the [selection table](../README.md#how-to-pick-a-parser).

See [`results/caveats.md`](../results/caveats.md) for the full failure-mode analysis and [`README.md`](../README.md) for the ranked results.
