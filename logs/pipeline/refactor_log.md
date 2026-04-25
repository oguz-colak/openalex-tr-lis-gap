# Refactor Log

**Date:** 2026-04-22
**Purpose:** Restructure project into a clean, layered architecture according to `task.md`.

## Created Directories
- `data/raw/dergipark_xml`
- `data/raw/openalex_json`
- `data/parsed/dergipark`
- `data/parsed/openalex`
- `data/analysis/completeness_matrix`
- `data/enriched/dergipark`
- `data/enriched/openalex`
- `corpus/papers/arxiv`
- `corpus/papers/symposium`
- `docs/methodology`
- `docs/reports`
- `docs/literature`
- `docs/notes`
- `logs/harvest`
- `logs/pipeline`
- `scripts/harvest`
- `scripts/parse`
- `scripts/analysis`
- `scripts/enrichment`
- `scripts/writing_tools`
- `archive/legacy_scripts`
- `archive/legacy_data`

## Moved Files
- **Raw Data:** Moved OpenAlex JSON and DergiPark JSONL/IDs to `data/raw/*`.
- **Analysis Data:** Moved `openalex_completeness_matrix.csv` to `data/analysis/completeness_matrix/`.
- **Corpus:** Moved PDFs to `corpus/papers/arxiv/` and `corpus/papers/symposium/`.
- **Docs:** Grouped documentation into `methodology`, `reports`, `literature`, and `notes` subdirectories in `docs/`.
- **Logs:** Moved state JSONs and fetch logs to `logs/harvest/`.
- **Legacy:** Moved test XML files to `archive/legacy_data/`. Moved unused scripts (`mcp_openai_server.py`, `dergipark_harvester.py`) to `archive/legacy_scripts/`.
- **Scripts:** 
  - `fetch_dergipark.py`, `fetch_openalex.py` -> `scripts/harvest/`
  - `openalex_json_to_csv.py` -> `scripts/parse/parse_metadata.py`
  - `models.py` -> `scripts/parse/`
  - `update_abstract.py` -> `scripts/writing_tools/`

## Deleted Files & Directories
- `tmp/`
- `scratch/`
- `scripts/__pycache__/` and all `*.pyc` files
- `data/processed/openalex_tr_lis_works.csv`
- `data/processed/`

## Risk Report
- Data loss: No raw data was deleted. `openalex_tr_lis_works.csv` was deleted as it was deemed an intermediate artifact not used for final analysis and easily reproducible from raw JSON.
- Scripts: Script references to file paths will need to be updated to reflect the new directory structure.
