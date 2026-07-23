# Document Parser Benchmark

A benchmark comparing open-source document parsing tools for converting documents into clean Markdown for LLM and RAG applications.

## Why this project?

Document parsing is one of the biggest challenges in building reliable RAG pipelines.

Poor extraction quality can cause:

- broken document structure
- incorrect reading order
- lost tables
- bad chunk boundaries
- inaccurate retrieval results

This project evaluates different document parsing tools based on real-world documents.

## Tested Tools

| Tool | Description |
| --- | --- |
| Microsoft MarkItDown | Document to Markdown converter |
| Marker | PDF parser with strong layout understanding |
| Docling | Document intelligence toolkit |
| MinerU | PDF parsing and OCR framework |
| PaddleOCR | OCR engine |

## Evaluation Criteria

We compare:

- Reading order preservation
- Markdown quality
- Table extraction
- Heading detection
- OCR accuracy
- RAG usability

## Benchmark Documents

Test cases include:

- Multi-column academic papers
- Business reports
- Tables
- Scanned PDFs
- Complex layouts

## Results

Benchmark results will be updated as more tests are completed.

## Related Project

DocCrush provides an online document processing workflow:

https://doccrush.com

Convert documents into clean Markdown optimized for AI applications.

## Contributing

Suggestions and benchmark cases are welcome.

Open an issue or submit a pull request.
