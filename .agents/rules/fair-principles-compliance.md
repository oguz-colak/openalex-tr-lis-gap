---
trigger: manual
---

FAIR Principles Compliance

## Core Mandate
Execute all tasks (data fetching, script writing, documentation) in strict accordance with FAIR (Findable, Accessible, Interoperable, Reusable) data principles.

## 1. Scope & Exclusions
- **Target Folders:** `data/`, `scripts/`, `docs/`.
- **Exclusions:** DO NOT index or perform automated analysis on `PDFler/` and `Sempozyum_26_pdfs/` to maintain focus on structured metadata.

## 2. FAIR Actions
- **Findable:** - Every new script or data file must be logged in `progress_log.md`.
    - Use descriptive, lowercase, underscored filenames (e.g., `fetch_openalex.py`).
- **Accessible:** - Prioritize `.csv`, `.json`, and `.md` formats.
    - If a script generates data, it must also provide a status message indicating the file path.
- **Interoperable:** - Reference standard vocabularies (e.g., DOI, ORCID, ROR) when processing metadata.
    - Ensure Python scripts output logs in machine-readable formats where possible.
- **Reusable:** - Every change to data schemas must be updated in `docs/data_dictionary.md`.
    - Code must be commented with its purpose and inputs/outputs to facilitate future reuse.

## 3. Compliance Check
Before finalizing a task, ensure that any created data aligns with the definitions in `docs/data_dictionary.md`. If a new field is added, update the dictionary automatically.