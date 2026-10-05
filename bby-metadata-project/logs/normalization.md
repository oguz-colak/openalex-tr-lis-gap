You are acting as a senior data engineer, metadata architect, and pragmatic vibe coder working on a bibliographic metadata reconciliation pipeline.

Your task is NOT just cleaning strings.

You are building a production-grade:

* metadata normalization engine
* cross-platform schema harmonization layer
* bibliographic entity resolution pipeline
* data quality validation framework
* anomaly detection system

The project ingests metadata from:

* OpenAlex
* DergiPark MODS
* TR-Dizin JSON
* bd.org.tr MARCXML

The current implementation is too simplistic and mixes:

* normalization
* validation
* reconciliation
* anomaly detection
* schema mapping

into the same layer.

Refactor the system into a rule-driven architecture.

Critical requirement:
Normalization rules must be:

* idempotent
* explainable
* auditable
* source-aware
* reversible when possible

The current plan and findings are below.

---

# EXISTING VERIFIED RULES

## DOI normalization

Observed formats:

* OpenAlex:
  "https://doi.org/10.14293/s2199-1006.1"

* DergiPark MODS:
  "https://doi.org/10.24146/tk.1002393"

* bd.org.tr MARCXML:
  "10.15612/BD.2019.741"

Rules:

* lowercase DOI
* strip:

  * https://doi.org/
  * http://dx.doi.org/
* normalization must be idempotent
* validate DOI regex
* detect duplicate DOI assignments
* support preprint DOI detection:

  * 10.48550 → arXiv
  * 10.5281 → Zenodo
  * 10.20944 → Preprints.org

---

## Year extraction normalization

Observed formats:

* OpenAlex:
  2016

* MODS:
  2021-09-01

* MARCXML:
  2019-12-30 00:00:00

Rules:

* extract only year
* convert to int
* valid range:
  1900 <= year <= current_year + 1
* invalid years become None
* never coerce invalid years to 0

---

## Unicode normalization

Critical for Turkish metadata.

Observed names:

* Açık
* Çelik
* Şerefoğlu
* MAHİROĞLU

Rules:

* use Unicode NFC normalization
* preserve Turkish characters
* never ASCII-fold

---

# CURRENT PROBLEMS

## Language code normalization

Current mapping incomplete.

Observed values:

* OpenAlex:
  "tr"

* DergiPark:
  "tr"

* TR-Dizin:
  "TUR"

* bd.org.tr:
  "tur"

Required fixes:

* support lowercase ISO639-2 variants
* add:
  "tur" -> "tr"
  "eng" -> "en"

Need:

* canonical ISO639-1 output
* configurable mapping table

---

## Title normalization issues

### Smart quotes

Observed:

* Türkiye'de
* Yazar(lar)

Need:

* normalize curly quotes/apostrophes
* normalize Unicode punctuation variants

### Multilingual titles in MODS

Observed:

* xml:lang="tr-TR"
* xml:lang="en-US"

Need explicit reconciliation logic:

* Turkish title becomes primary canonical title
* English title stored separately as:
  title_en

Do NOT collapse multilingual titles into one field.

---

## Author normalization issues

### ALL CAPS author names

Observed:

* "Halise ŞEREFOĞLU HENKOĞLU"

Need:

* detect ALL CAPS patterns
* apply title-case normalization carefully
* preserve Turkish casing rules

---

### Garbage author detection

Observed garbage entries:

* "Bu ARAŞTIRMA"
* "Ahmet MAHİROĞLU DANIŞMANLIĞINDA"

Need:

* anomaly detection layer
* stopword/keyword filtering
* confidence scoring
* explainability

These are NOT normal normalization rules.
They belong to anomaly detection.

---

### Incorrect entity extraction

Observed:

* "Dünyası, Bilgi"

This is actually journal title:

* "Bilgi Dünyası"

Need:

* journal-title leakage detection
* source-aware heuristics
* MARC field-aware parsing

---

### Name order normalization

Observed:

* "Şerefoğlu Henkoğlu, Halise"

Need:

* normalize:
  Last, First
  →
  First Last

But:

* retain original raw value
* preserve provenance

---

# CRITICAL MISSING COMPONENT

## bd.org.tr MARCXML schema mapping

Current metric_definitions_v2.json lacks MARCXML mapping.

Need full mapping layer.

Required mappings:

* 022$a → ISSN
* 024$a when code=doi → DOI
* 245$a → title
* 100$a → primary author
* 700$a → added personal name
* 720$a → uncontrolled name
* 546$a → language
* 260$c or 264$c → publication date

Need explicit distinction between:

* controlled author fields
* uncontrolled entries

MARC semantics matter.

---

# DergiPark MODS schema correction

Current assumptions wrong.

Correct mappings:

Journal title:
relatedItem[@type='host']/titleInfo/title

Page information:
relatedItem/part/extent[@unit='pages']/start|end

Do NOT use publisher field as journal title.

---

# REQUIRED ARCHITECTURE REFACTOR

The current architecture mixes unrelated concerns.

Refactor into:

{
"schema_mapping": {},
"normalization_rules": {},
"validation_rules": {},
"anomaly_rules": {},
"reconciliation_rules": {},
"source_priority_rules": {}
}

---

# EXAMPLES

## Normalization rules

Pure deterministic transforms:

* DOI lowercase
* Unicode NFC
* ISSN formatting
* whitespace cleanup
* smart quote replacement

---

## Validation rules

* DOI regex
* year range validation
* ISO639 conformity
* ISSN checksum validation

---

## Anomaly rules

* garbage author detection
* journal parsed as author
* impossible year values
* suspicious ALL CAPS patterns

---

## Reconciliation rules

* TR title primary
* EN title secondary
* ORCID precedence
* structured MODS author preferred
* mixed-case preferred over ALL CAPS

---

## Source priority rules

Examples:

* TR-Dizin name > inPublicationName
* MODS structured name > raw string
* OpenAlex DOI authoritative

---

# ADD RULE PROVENANCE

Every rule must include metadata.

Example:

{
"rule_id": "author_all_caps_normalization",
"type": "normalization",
"applies_to": ["trdizin"],
"confidence": 0.82,
"reversible": true,
"source": "empirical_observation"
}

Need:

* explainability
* auditability
* traceability

---

# ADD CONFIDENCE SCORING

Need field-level and record-level confidence scores.

Example:

{
"author_match_confidence": 0.91,
"title_match_confidence": 0.87,
"doi_match_confidence": 1.0,
"overall_record_confidence": 0.93
}

---

# MISSINGNESS CLASSIFICATION

Implement:

* CMI
* PMI
* NMI
* FI

per field.

Do NOT treat missing and conflicting data as the same thing.

---

# IMPLEMENTATION REQUIREMENTS

Use only:

* pandas
* numpy
* re
* unicodedata
* pathlib
* json
* logging

Optional:

* rapidfuzz

No heavyweight frameworks.

---

# OUTPUT REQUIREMENTS

1. Refactor metric_definitions_v2.json
2. Create modular rule structure
3. Add MARCXML schema mapping
4. Add reconciliation layer
5. Add anomaly detection layer
6. Add provenance metadata
7. Add confidence scoring
8. Preserve raw/original values
9. Keep transforms idempotent
10. Produce explainable outputs

---

# DESIGN PHILOSOPHY

This is NOT a generic ETL cleaner.

This is a:

* metadata quality engine
* bibliographic reconciliation pipeline
* scholarly metadata harmonization system

Design accordingly.

Prefer:

* deterministic transforms
* composable rules
* source-aware heuristics
* transparent audit logs
* explicit provenance
* reversible normalization

Avoid:

* hidden heuristics
* destructive transforms
* silent coercion
* lossy normalization

Think like:

* a metadata engineer
* a digital librarian
* a scholarly infrastructure architect
* a production data engineer
* an entity resolution specialist

Now:

* propose the refactored architecture
* define the JSON schema
* redesign the normalization layer
* identify hidden edge cases
* implement the rule structure
* improve the agent prompts
* suggest pipeline modules
* generate production-quality code where needed
* optimize for maintainability and explainability
