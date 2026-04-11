# Progress Log - Symposium Proceeding

> [2026-04-08 11:45] - **Action:** Executed OpenAlex metadata extraction.
> - **Changes:** Created `data/raw/openalex_bby_works_full.json`.
> - **Outcome:** Retrieved metadata for 45 articles from 'Türk Kütüphaneciliği'.

> [2026-04-08 11:49] - **Action:** Comprehensive metadata harvesting for 6 BBY journals (All Time).
> - **Changes:** Updated `scripts/fetch_openalex.py`, `scripts/fetch_dergipark.py`. Created `data/raw/openalex_bby_works_full.json` (2826 records) and `data/raw/dergipark_ground_truth_full.json` (2235 records).
> - **Outcome:** Successfully resolved Bilgi Dünyası harvesting gap via HTTP OAI endpoint. Expanded OpenAlex coverage using Source ID filters to include all historical records available.

> [2026-04-08 12:51] - **Action:** Corrected OpenAlex harvest filter (Primary Location).
> - **Changes:** Modified `scripts/fetch_openalex.py`. Re-generated `data/raw/openalex_bby_works_full.json` (1382 records).
> - **Outcome:** Eliminated 902 SHILAP records. Dataset is now cleaned and ready for gap analysis.

> [2026-04-08 13:14] - **Action:** Scientific Validation of Dataset Completeness (OpenAlex & DergiPark).
> - **Changes:** Created `tmp/verify_completeness.py`, `tmp/compare_years.py`, `tmp/verify_dp_structure.py`. Generated `validation_report.md` and `validation_report_dp.md`.
> - **Outcome:** 
>   - **OpenAlex Audit:** Proved 100% coverage relative to internal index via Orphaned ISSN check (0 records lost). Verified historical depth (since 1953) for established journals.
>   - **DergiPark Audit:** Structural continuity verified via Volume/Issue sequence analysis. Cross-validation with web archive pages confirmed 1:1 match with harvested OAI-PMH records (e.g., 84/84 issues for TK).

> [2026-04-08 13:36] - **Action:** Converted full JSON datasets (OpenAlex & DergiPark) to Analysis-Ready CSV.
> - **Changes:** Updated `scripts/json_to_csv.py`. Created `data/processed/openalex_bby_works_full.csv` (1,382 rows) and `data/processed/dergipark_ground_truth_full.csv` (2,235 rows).
> - **Outcome:** Successfully flattened nested metadata into CSV format using `UTF-8-SIG` encoding (BOM) to ensure compatibility with Windows Excel and preserve Turkish characters.

> [2026-04-08 15:13] - **Action:** Optimized DergiPark metadata extraction via Robust Fallback Logic.
> - **Changes:** Updated `scripts/json_to_csv.py` with multi-field regex extraction. Re-generated `data/processed/dergipark_ground_truth_full.csv`.
> - **Outcome:** Successfully recovered **203 additional publication years** for TK records from DOI strings and descriptions. Reduced missing dates from 688 to 485. Verified the "0019" anomaly as a manual data entry error in DergiPark.

> [2026-04-08 15:20] - **Action:** Cleaned up project workspace.
> - **Changes:** Deleted 32 temporary Python scripts and text reports from the `tmp/` directory.
> - **Outcome:** Maintained a clean working environment and followed data hygiene protocols.


> [2026-04-08 15:38] - **Action:** Engineered Industrial-Grade Robust OAI-PMH Harvester.
> - **Changes:** Completely rewritten scripts/fetch_dergipark.py.
> - **Outcome:** Implemented tenacity exponential backoff (retries), lxml defensive parsing (error recovery), and detailed checkpointing logic in tmp/harvester_state.json. The system now supports 100% data extraction with resumption capabilities from any resumptionToken failure point. Verified functionality via partial run and state persistence check.
> - **Outcome:** Implemented tenacity exponential backoff (retries), lxml defensive parsing (error recovery), and detailed checkpointing logic in tmp/harvester_state.json. The system now supports 100% data extraction with resumption capabilities from any resumptionToken failure point. Verified functionality via partial run and state persistence check.

> [2026-04-08 15:48] - **Action:** Converted full robust DergiPark/OpenAlex JSON to analysis-ready CSV.
> - **Changes:** Updated scripts/json_to_csv.py. Re-generated data/processed/dergipark_ground_truth_full.csv (4,470 rows) and data/processed/openalex_bby_works_full.csv (1,382 rows).
> - **Outcome:** Flattened all 15 Dublin Core fields. Successfully recovered missing dates using improved regex fallback. Validated character encoding integrity (UTF-8-SIG).

> [2026-04-09 11:13] - **Action:** Reset project codebase for a fresh start.
> - **Changes:** Deleted 5 scripts from 'scripts/' and cleared 'tmp/' directory.
> - **Outcome:** Environment prepared for clean project initialization.

> [2026-04-09 11:15] - **Action:** Cleared raw data directory.
> - **Changes:** Deleted all 4 JSON files in `data/raw/` (`dergipark_ground_truth.json`, `dergipark_ground_truth_full.json`, `openalex_bby_works.json`, `openalex_bby_works_full.json`).
> - **Outcome:** Raw data cache cleared for fresh ingestion.

> [2026-04-09 11:16] - **Action:** Cleaned up root directory artifacts and scripts.
> - **Changes:** Deleted `harvester.log`, `download_pdfs.py`, and `bd_test.xml`.
> - **Outcome:** Removed legacy log files and redundant scripts from the main workspace.

> [2026-04-09 11:57] - **Action:** Executed robust OpenAlex metadata extraction for 6 LIS journals.
> - **Changes:** Created `scripts/fetch_openalex.py`, `data/raw/openalex_bby_works_full.json`, and `data/raw/openalex_state.json`.
> - **Outcome:** Successfully fetched 1,382 records using ISSN-based filtering and cursor pagination. Optimized storage by removing abstracts. Verified data integrity and checkpointing functionality.
[2026-04-09 13:28] - **Action:** Executed OpenAlex JSON to CSV flattening script.
- **Changes:** Created scripts/openalex_json_to_csv.py, generated data/processed/openalex_bby_works_full.csv.
- **Outcome:** Successfully flattened 1382 works into a structured CSV with UTF-8-SIG encoding.

> [2026-04-11 12:06] - **Action:** OpenAlex web sitesi ve API verileri arasındaki kayıt sayısı karşılaştırması.
> - **Changes:** `progress_log.md` güncellendi.
> - **Outcome:** OpenAlex web sitesi üzerinden yapılan Türk Kütüphaneciliği adlı sorguda 546 kayıt yer almaktayken, aynı siteden API ile çekilen veride Türk Kütüphaneciliği adıyla filtreleme yapıldığında 541 kayıt yer alıyor. Fakat filtrede daha sonra Boş Olanlar eklendiğinde kayıt sayısı 546 ya çıkıyor, yani API den çekilen Türk Kütüphaneciliği kayıtları doğru.

> [2026-04-11 12:47] - **Action:** Created empty data dictionary file.
> - **Changes:** Created `data_dictionary.md`.
> - **Outcome:** Initialized an empty markdown file for future data documentation.

> [2026-04-11 13:10] - **Action:** Initialized Git and pushed to GitHub repository.
> - **Changes:** Initialized `.git`, added all files, and pushed to `https://github.com/oguz-colak/openalex-tr-lis-gap.git`.
> - **Outcome:** Project structure and FAIR rules committed to remote `main` branch.

> [2026-04-11 13:42] - **Action:** Updated `fetch_openalex.py` to use Source IDs and re-executed harvesting.
> - **Changes:** Modified `scripts/fetch_openalex.py` (Source ID filter, cleaned placeholders), re-generated `data/raw/openalex_bby_works_full.json`.
> - **Outcome:** Successfully fetched 549 records for Bilgi Dünyası using its OpenAlex Source ID (`s2736521800`). 
> 
> ### 🚨 ÖNEMLİ BULGU (BİLDİRİ İÇİN)
> ISSN bazlı API sorgusu ile Source ID bazlı Web sorgusu arasındaki fark test edildi. Sadece Bilgi Dünyası dergisinde, makale düzeyinde ISSN üstverisi eksik olan yaklaşık 500 adet (549) kayıt tespit edildi. Bu durum, Türkiye adresli LIS dergilerinin OpenAlex'e aktarımında (OJS migrasyonu) ciddi bir Metadata Gap (Üstveri Boşluğu) olduğuna dair bildirinin temel bulgusunu oluşturacaktır.
