You are a senior data engineer performing a **targeted correction pass** on an already refactored research data pipeline.

Your task is to **fix critical architectural violations** WITHOUT restructuring the whole project again.

---

# 🎯 OBJECTIVE

Apply the following 5 FIXES:

1. Correct RAW vs PARSED separation for DergiPark
2. Restore true RAW XML data into raw layer
3. Separate parsing logic from transformation logic
4. Ensure analysis dataset is built ONLY from parsed data
5. Add provenance metadata fields to parsed records

---

# ⚠️ GLOBAL RULES

* DO NOT redesign the entire project
* DO NOT delete any data unless explicitly safe
* DO NOT modify research documents (docs/ or corpus/)
* ALL actions must be logged in: `logs/pipeline/fix_log.md`
* If uncertain → MOVE to archive instead of deleting

---

# 🔧 FIX 1 — CORRECT DERGIPARK RAW LAYER

## Problem

DergiPark JSONL files are incorrectly placed in raw/

## Action

* Ensure:

  * ONLY XML files exist in `data/raw/dergipark_xml/`
* Move all parsed JSON/JSONL files to:

  * `data/parsed/dergipark/`

## Validation

* raw/dergipark_xml → only `.xml`
* parsed/dergipark → only structured records

---

# 🔧 FIX 2 — RESTORE TRUE RAW XML

## Problem

XML files were moved to archive but are actually raw data

## Action

* Identify XML files in:

  * `archive/legacy_data/`

* Move ONLY real OAI-PMH responses to:

  * `data/raw/dergipark_xml/`

* Leave test/tracer XMLs in archive

## Heuristic

* Keep files with:

  * `<OAI-PMH>` root
* Ignore small test files or malformed XML

---

# 🔧 FIX 3 — SPLIT PARSE VS TRANSFORM

## Problem

Parsing and transformation are mixed in `parse_metadata.py`

## Action

### Create

scripts/parse/
├── parse_dergipark.py
├── parse_openalex.py

### Rules

* parse scripts:

  * ONLY map raw → structured schema
  * NO flattening
  * NO inference
  * NO regex fixes

### Move logic

* If code does:

  * flattening
  * CSV conversion
  * normalization
    → move that logic OUT of parse layer

---

# 🔧 FIX 4 — ENFORCE ANALYSIS PURITY

## Problem

Analysis may be using enriched or transformed data

## Action

* Ensure:

scripts/analysis/build_completeness_matrix.py

ONLY reads from:

* `data/parsed/dergipark/`
* `data/parsed/openalex/`

### Strict rules

* NO inferred values
* NO regex recovery
* NO enrichment fields

If violations found:

→ isolate them into enrichment layer

---

# 🔧 FIX 5 — ADD PROVENANCE FIELDS

## Problem

Records lack source traceability

## Action

Update parsed data schema to include:

* `source_system`: "dergipark" | "openalex"
* `metadata_format`: "mods" | "dc"
* `is_inferred`: boolean (default = False)

### Apply to

* ALL parsed records
* Do NOT backfill inferred values

---

# 🧪 VALIDATION CHECKLIST

After applying fixes, verify:

* raw/ contains ONLY untouched source data
* parsed/ contains structured but NOT enriched data
* analysis/ uses ONLY parsed data
* enriched/ contains ALL inferred values
* no script mixes responsibilities

---

# 📝 LOGGING

Write all actions to:

logs/pipeline/fix_log.md

Include:

* files moved
* scripts modified
* logic extracted
* any uncertainty

---

# 🚫 DO NOT

* Do NOT rewrite entire pipeline
* Do NOT delete XML unless confirmed duplicate
* Do NOT merge parsed and enriched data
* Do NOT modify CSV values

---

# ✅ FINAL OUTPUT

Return:

1. List of changes applied
2. Updated directory tree
3. Scripts created/modified
4. Any unresolved risks

---

# 🧠 MINDSET

This is a **surgical correction pass** to ensure:

* epistemic validity
* reproducibility
* separation of concerns

Act precisely and conservatively.
