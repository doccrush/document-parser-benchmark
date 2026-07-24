---
name: "\U0001F4C4 Submit a challenging document"
about: Suggest a real-world PDF that stresses parsers in a way not yet covered
title: "[Document] <short description>"
labels: ["new-document"]
---

### Document

- **Name / source:**
- **Public URL or attached below?**
- **May it be redistributed in this repo for benchmarking?** (required for inclusion; note the license — e.g. CC, public domain, your own)

### What makes it hard for parsers?

Check all that apply:

- [ ] Multi-column layout
- [ ] Dense / complex tables
- [ ] Scanned / requires OCR
- [ ] Very large (many pages / high MB)
- [ ] Image-heavy pages
- [ ] Math / equations
- [ ] Mixed scripts / CJK
- [ ] Other:

### What went wrong?

If you've already run it through a parser, describe the failure (e.g. "tables collapsed", "reading order scrambled", "timed out"):

### Expected behavior

What should correct extraction look like for this document?
