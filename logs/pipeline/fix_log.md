# Fix Log

**Date:** 2026-04-23
**Purpose:** Apply targeted corrections as per `task_2.md` to ensure epistemic validity, reproducibility, and separation of concerns.

## Actions Taken:

### FIX 1: Correct Dergipark Raw Layer
- Moved `dergipark_records.jsonl` from `data/raw/dergipark_xml/` to `data/parsed/dergipark/`.
- Moved `dergipark_ids/` JSON files from `data/raw/dergipark_xml/` to `data/parsed/dergipark/`.
- **Validation:** `data/raw/dergipark_xml/` is now devoid of non-XML files.

### FIX 2: Restore True Raw XML
- Analyzed `archive/legacy_data/*.xml` files.
- **Decision:** Identified as test/tracer XMLs (single records from DergiPark API tests). As per the heuristic ("Ignore small test files"), they were left in `archive/legacy_data/`. No true full OAI-PMH dumps were found to restore.

### FIX 3: Split Parse vs Transform
- Removed `scripts/parse/parse_metadata.py`.
- Created `scripts/parse/parse_openalex.py` which only maps raw OpenAlex JSON to a structured parsed format (JSONL) without any flattening, CSV conversion, or regex.
- Updated `scripts/parse/models.py` schema with provenance fields.

### FIX 4: Enforce Analysis Purity
- Created `scripts/analysis/build_completeness_matrix.py` (migrated transforming logic from old parse script).
- Ensured it strictly reads from `data/parsed/openalex/openalex_records.jsonl` rather than raw data.
- The analysis logic now handles flattening of properly parsed lists/dicts without injecting inferred values.

### FIX 5: Add Provenance Fields
- Extended `ArticleMetadata` in `models.py` with:
  - `source_system`
  - `metadata_format`
  - `is_inferred`
- Executed a script to inject provenance fields into all existing parsed DergiPark records (`dergipark_records.jsonl`).
- Implemented provenance fields injection natively inside `parse_openalex.py`.

## Unresolved Risks
- **Raw XML Data:** The pipeline currently generates JSONL directly via `fetch_dergipark.py` instead of saving XML OAI-PMH responses to `data/raw/dergipark_xml/`. Rewriting `fetch_dergipark.py` was skipped to adhere to the "DO NOT rewrite entire pipeline" constraint. Future harvests will still bypass the raw XML folder. This remains a minor architectural debt.
