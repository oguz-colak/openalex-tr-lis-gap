You are a senior data engineer tasked with refactoring a research data pipeline repository for a metadata quality study.

Your objective is to **restructure the project into a clean, layered architecture** and **remove all redundant, legacy, and analysis-polluting artifacts** WITHOUT breaking reproducibility.

This project contains BOTH:

* a **data pipeline (metadata extraction & analysis)**
* a **research layer (documents, PDFs, reports)**

These MUST be strictly separated.

---

# 🎯 GOAL

Transform the project into a **multi-layer architecture**:

## DATA PIPELINE

1. `raw/` → immutable source data (no parsing, no transformation)
2. `parsed/` → structured, schema-validated data (no enrichment)
3. `analysis/` → datasets used for evaluation (completeness, comparison)
4. `enriched/` → optional improved/inferred metadata (NOT used for evaluation)

## RESEARCH LAYER

1. `docs/` → methodology, reports, notes (no execution dependency)
2. `corpus/` → PDF papers and literature (read-only, not part of pipeline)

---

# ⚠️ CRITICAL RULES

* NEVER delete data before verifying it is reproducible
* NEVER mix pipeline data with research documents
* NEVER allow scripts to write into `docs/` or `corpus/`
* NEVER modify raw data
* ALL destructive actions must be logged

---

# 📁 TARGET DIRECTORY STRUCTURE

Reorganize the project into:

data/
├── raw/
│   ├── dergipark_xml/
│   └── openalex_json/
│
├── parsed/
│   ├── dergipark/
│   └── openalex/
│
├── analysis/
│   └── completeness_matrix/
│
├── enriched/
│   ├── dergipark/
│   └── openalex/

corpus/
├── papers/
│   ├── arxiv/
│   ├── symposium/

docs/
├── methodology/
├── reports/
├── literature/
├── notes/

logs/
├── harvest/
├── pipeline/

scripts/
├── harvest/
├── parse/
├── analysis/
├── enrichment/
├── writing_tools/

archive/
├── legacy_scripts/
├── legacy_data/

---

# 🧹 CLEANUP TASKS

## 1. RAW DATA NORMALIZATION

* Move ALL original:

  * XML files → `data/raw/dergipark_xml/`
  * OpenAlex JSON → `data/raw/openalex_json/`

* If raw data is missing:
  → STOP and log error

---

## 2. RESEARCH MATERIAL SEPARATION

### Move ALL PDF files

* `PDFler/` → `corpus/papers/arxiv/`
* `Sempozyum_26 PDFs/` → `corpus/papers/symposium/`

### Move and reorganize documentation

* Methodology files → `docs/methodology/`
* Analysis reports → `docs/reports/`
* Literature reviews → `docs/literature/`
* Drafts and notes → `docs/notes/`

---

## 3. DELETE / ARCHIVE THESE FILE TYPES

### ❌ DELETE (if reproducible)

* tmp/
* **pycache**/
* *.pyc
* scratch/
* intermediate CSVs not used in final analysis

### 📦 MOVE TO archive/

* old scripts no longer in pipeline
* experimental notebooks
* duplicate datasets
* legacy XML test files (e.g. tracer bullet samples)

---

## 4. SCRIPT REFACTOR

Reorganize scripts into:

scripts/
├── harvest/
│   ├── fetch_dergipark.py
│   └── fetch_openalex.py
│
├── parse/
│   └── parse_metadata.py
│
├── analysis/
│   └── build_completeness_matrix.py
│
├── enrichment/
│   └── enrich_metadata.py
│
├── writing_tools/
│   └── update_abstract.py

### Rules

* One responsibility per script
* No script should both parse AND analyze
* No script should modify raw data
* No script should interact with `corpus/`

---

## 5. DATA PURITY ENFORCEMENT

Validate:

* raw/ → ONLY source dumps
* parsed/ → schema-compliant only
* analysis/ → NO inferred values
* enriched/ → inferred values must be explicitly marked

If violations are found:
→ isolate and move to correct layer

---

## 6. LOGGING

Create:

logs/pipeline/refactor_log.md

Log:

* all deleted files
* all moved files
* all renamed scripts
* any uncertainty or skipped action

---

## 7. SAFETY CHECKS

Before deletion:

* confirm data can be regenerated via scripts
* confirm no unique data loss

If unsure:
→ MOVE to archive instead of deleting

---

# ✅ FINAL OUTPUT

At the end, produce:

1. Clean directory tree
2. List of removed files
3. List of archived files
4. List of refactored scripts
5. Risk report

---

# 🚫 DO NOT

* Do NOT change research data content
* Do NOT modify CSV values
* Do NOT perform enrichment
* Do NOT merge datasets
* Do NOT treat `docs/` or `corpus/` as pipeline inputs

---

# 🧠 MINDSET

This is NOT a coding task.

This is a **data architecture refactor for scientific validity**, where:

* pipeline data
* research documents
* and literature corpus

are strictly separated.

Act conservatively, transparently, and reproducibly.
