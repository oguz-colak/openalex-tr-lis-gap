# Güncel Proje Repo Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the old contents of `openalex-tr-lis-gap` with the current `5th_GGBBYS` project while preserving Git history and making the private repository reproducible.

**Architecture:** Keep the current `bby-metadata-project` directory as the project boundary so existing paths remain recognizable. Add only repository-level documentation, dependency, provenance, and ignore files needed to run and audit the current snapshot. Remove legacy repository files with a normal commit; do not rewrite history.

**Tech Stack:** Python 3.10+, `requests`, `pandas`, `matplotlib`, JSON/XML, Git, PowerShell on Windows.

**Spec:** `docs/superpowers/specs/2026-10-05-current-project-migration-design.md`

## Global Constraints

- Migration öncesi `main` commit'i `legacy-before-current-project` etiketiyle saklanacaktır.
- History rewrite veya orphan branch kullanılmayacaktır.
- Ham bibliyografik XML/JSON kayıtları korunacaktır.
- PDF tam metinleri, `.pyc`, `__pycache__`, geçici loglar ve credential dosyaları taşınmayacaktır.
- Türkçe karakterler korunacak; dosyalar UTF-8 olarak tutulacaktır.
- Taşıma sırasında bilimsel analiz algoritmaları değiştirilmeyecektir.
- OpenAlex iletişim e-postası kod içine sabitlenmeyecek; `OPENALEX_MAILTO` ortam değişkeni kullanılacaktır.
- `origin/main` ancak yerel doğrulamalar tamamlandıktan sonra güncellenecektir.

## Review Focus

- Eski repo dosyalarının `main` çalışma ağacında kalması — Task 2'nin takip edilen dosya listesi kontrolü.
- PDF, `.pyc`, geçici log veya credential dosyasının yanlışlıkla stage edilmesi — Task 2 ve Task 6 artifact taraması.
- `bby-metadata-project` altındaki mevcut çıktı yollarının script konumlarıyla uyuşmaması — Task 3 path smoke test'i.
- Türkçe karakterlerin veya XML/JSON Unicode içeriğinin bozulması — Task 2 UTF-8 ve örnek içerik doğrulaması.
- Kişisel e-posta/API anahtarının kod veya commit içine gömülmesi — Task 3 secret-pattern testi.

---

### Task 1: Migration branch ve legacy geri dönüş noktası

**Files:**
- Git metadata only: branch/tag creation; no product files modified.

**Interfaces:**
- Consumes: the isolated migration clone used for this plan.
- Produces: local branch `migration/current-project-2026-10-05` and tag `legacy-before-current-project` pointing to the pre-migration remote `main` commit.

- [ ] **Step 1: Verify the starting point**

Run:

```powershell
git status --short --branch
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

Expected: clean local branch, local migration base known, and the remote main hash is `2ce01c30841f9fa15986340cabd4056f2292f12f`.

- [ ] **Step 2: Create the local safety tag and migration branch**

Create `legacy-before-current-project` at the remote main hash and branch from the current local `main` so the already-reviewed design commit remains available locally.

- [ ] **Step 3: Verify branch isolation**

Run `git status --short --branch` and `git tag --list legacy-before-current-project`. Expected: active branch is `migration/current-project-2026-10-05`; the tag resolves to `2ce01c3`.

- [ ] **Step 4: Commit the migration plan**

```powershell
git add docs/superpowers/plans/2026-10-05-current-project-migration.md
git commit -m "docs: add current project migration plan"
```

Expected: one plan commit and no unstaged changes.

---

### Task 2: Replace the legacy working tree with the current project snapshot

**Files:**
- Delete: all legacy tracked files outside `docs/superpowers/specs/` and `docs/superpowers/plans/`.
- Create: `bby-metadata-project/02_data_collection/raw_data/openalex/*.json` (six files).
- Create: `bby-metadata-project/02_data_collection/raw_data/dergipark/*.xml` (five files).
- Create: `bby-metadata-project/02_data_collection/raw_data/bilgi_dunyasi/oai_bd.xml`.
- Create: `bby-metadata-project/02_data_collection/raw_data/harvest_log.json`.
- Create: `bby-metadata-project/logs/*.py` (three harvester scripts).
- Create: `bby-metadata-project/logs/normalization.md`.
- Do not create: PDFs, `.log`, `.pyc`, `__pycache__`.

**Interfaces:**
- Consumes: source files from the current project's `bby-metadata-project` directory.
- Produces: current raw data and harvester snapshot under the repository's `bby-metadata-project` boundary.

- [ ] **Step 1: Remove legacy tracked product files**

Remove the old root `README.md`, `AGENTS.md`, `.agents/`, `.vscode/`, `scripts/`, `data/`, `archive/`, `corpus/`, `logs/`, `docs/methodology/`, `docs/notes/`, `docs/reports/`, and other legacy files while preserving the reviewed `docs/superpowers/` documents.

- [ ] **Step 2: Copy the allowlisted current files**

Copy only the exact source groups listed above. Do not copy the complete source directory recursively, because it contains ten PDFs, three `.pyc` files, and three temporary `.log` files.

- [ ] **Step 3: Verify raw snapshot counts and UTF-8 content**

Check that the six OpenAlex JSON files, five DergiPark XML files, one Bilgi Dünyası XML file, and `harvest_log.json` exist; parse representative JSON/XML files; and confirm Turkish strings such as `Türk Kütüphaneciliği`, `Bilgi Dünyası`, and `Şerefoğlu` remain intact.

- [ ] **Step 4: Verify artifact exclusion before staging**

Run a recursive search for `*.pdf`, `*.pyc`, `__pycache__`, `*.log`, `.env`, and credential-like filenames. Expected: no matches in the migration tree.

- [ ] **Step 5: Stage and inspect the snapshot replacement without committing**

Run `git add -A` followed by `git status --short`. Expected: the diff removes legacy files and adds only the allowlisted current project files. Leave the staged migration changes for the single migration commit after documentation and verification are complete.

---

### Task 3: Make harvest scripts portable and credential-safe

**Files:**
- Modify: `bby-metadata-project/logs/openalex_harvester.py`.
- Modify: `bby-metadata-project/logs/dergipark_oaipmh_harvester.py`.
- Modify: `bby-metadata-project/logs/bilgi_dunyasi_harvester.py`.
- Create: `tests/test_harvester_paths.py`.

**Interfaces:**
- Consumes: `OPENALEX_MAILTO` optionally from the process environment.
- Produces: output paths rooted at `bby-metadata-project/02_data_collection/raw_data/`; no hard-coded personal contact or secret.

- [ ] **Step 1: Write failing path and configuration tests**

Add tests that import the three scripts by file path and assert:

```python
assert openalex.OUTPUT_DIR == project_root / "02_data_collection/raw_data/openalex"
assert dergipark.OUTPUT_DIR == project_root / "02_data_collection/raw_data/dergipark"
assert bilgi_dunyasi.BASE_DIR == project_root / "02_data_collection/raw_data/bilgi_dunyasi"
```

Also assert the OpenAlex module does not expose a literal personal email and that `OPENALEX_MAILTO` is optional when constructing request parameters.

- [ ] **Step 2: Run the focused tests and verify failure**

Run:

```powershell
python -m pytest tests/test_harvester_paths.py -q
```

Expected: FAIL against the current script-relative output paths and hard-coded email.

- [ ] **Step 3: Implement the minimal portability changes**

In each harvester, define the project root from `Path(__file__).resolve().parents[1]` and derive raw-data paths from it. In the OpenAlex harvester, read `os.getenv("OPENALEX_MAILTO")` and include the `mailto` query parameter only when it is non-empty. Keep the source URLs, journal definitions, parsing rules, retry behavior, and output schemas unchanged.

- [ ] **Step 4: Run focused tests and syntax checks**

Run:

```powershell
python -m pytest tests/test_harvester_paths.py -q
python -m py_compile bby-metadata-project/logs/openalex_harvester.py bby-metadata-project/logs/dergipark_oaipmh_harvester.py bby-metadata-project/logs/bilgi_dunyasi_harvester.py
```

Expected: all focused tests pass and `py_compile` exits with code 0.

- [ ] **Step 5: Stage and inspect the script portability changes without committing**

Run `git add bby-metadata-project/logs tests/test_harvester_paths.py` and inspect the staged diff. Leave these changes staged for the single migration commit after documentation and verification are complete.

---

### Task 4: Add repository documentation, dependencies, and provenance

**Files:**
- Create: `README.md`.
- Create: `docs/methodology/analysis-plan.md`.
- Create: `docs/methodology/data-dictionary.md`.
- Create: `docs/reproducibility.md`.
- Create: `docs/data-provenance.json`.
- Create: `requirements.txt`.
- Replace: `.gitignore`.
- Create: `scripts/provenance/build_manifest.py`.
- Create: `tests/test_provenance_manifest.py`.

**Interfaces:**
- `scripts/provenance/build_manifest.py`: `build_manifest(root: Path, files: Iterable[Path]) -> dict`.
- Manifest entries contain `path`, `bytes`, `sha256`, and, for JSON/XML snapshots, `format`.
- `docs/reproducibility.md` documents `python scripts/provenance/build_manifest.py` and the exact source endpoints.

- [ ] **Step 1: Write failing manifest tests**

Test that a temporary UTF-8 file produces a deterministic SHA-256 entry and that a missing file raises `FileNotFoundError`. Test that generated paths are repository-relative POSIX paths.

- [ ] **Step 2: Run manifest tests and verify failure**

Run `python -m pytest tests/test_provenance_manifest.py -q`. Expected: FAIL because the manifest builder does not yet exist.

- [ ] **Step 3: Implement the manifest builder**

Implement deterministic sorted traversal, binary hashing, repository-relative POSIX paths, and JSON output with a UTC `generated_at` field. The script must not include excluded artifacts.

- [ ] **Step 4: Add documentation and dependency files**

Document the six-journal scope and counts from the approved analysis plan: 2,235 national records and 2,828 OpenAlex records. Include the 11 fields, source mappings, limitations, harvest commands, optional `OPENALEX_MAILTO`, and snapshot provenance. Set `requirements.txt` to the packages actually used by harvest and planned analysis: `requests`, `pandas`, and `matplotlib` with compatible lower bounds.

- [ ] **Step 5: Generate and verify the manifest**

Run the builder against the allowlisted raw XML/JSON files and verify that all listed paths exist, hashes are 64-character lowercase SHA-256 values, and no PDF/cache/log path is present.

- [ ] **Step 6: Run documentation and manifest tests**

Run:

```powershell
python -m pytest tests/test_provenance_manifest.py -q
```

Expected: all tests pass.

- [ ] **Step 7: Stage and inspect repository support files without committing**

Run `git add README.md .gitignore requirements.txt docs scripts/provenance tests` and inspect the staged diff. All migration files will be committed together after the full verification task.

---

### Task 5: Full local verification and migration review

**Files:**
- No intended product-file changes; verification of all migration outputs.

**Interfaces:**
- Consumes: all files on `migration/current-project-2026-10-05`.
- Produces: verified migration commit set ready for remote push.

- [ ] **Step 1: Run the complete Python test and syntax suite**

Run:

```powershell
python -m pytest -q
python -m compileall -q bby-metadata-project tests scripts
```

Expected: zero test failures and zero compile errors.

- [ ] **Step 2: Verify tracked-file policy**

Run a tracked-file scan and assert there are no `.pdf`, `.pyc`, `.log`, `__pycache__`, `.env`, private-key, token, password, or credential paths.

- [ ] **Step 3: Verify repository layout and data scope**

Confirm README paths exist, the six OpenAlex JSON snapshots and six national XML snapshots are present, the manifest matches their hashes, and the approved 2,235/2,828 scope is documented.

- [ ] **Step 4: Review the complete diff and history**

Run:

```powershell
git diff --check legacy-before-current-project..HEAD
git diff --cached --check
git diff --cached --stat
git log --oneline --decorate --max-count=8
git status --short --branch
```

Expected: no whitespace errors in committed or staged changes, a deliberate replacement diff, legacy tag present, and the staged migration set ready for the single commit in Task 6.

---

### Task 6: Commit and publish the verified migration

**Files:**
- Git remote refs only: `origin/main` and `origin/legacy-before-current-project`.

**Interfaces:**
- Consumes: verified local migration branch and tag.
- Produces: remote `main` containing only the current project plus the migration history, and a remote legacy tag.

- [ ] **Step 1: Create the single migration commit**

```powershell
git add -A
git commit -m "chore: migrate to current reproducible project"
```

Expected: one migration commit contains the legacy-tree deletion, current snapshot, portability changes, documentation, provenance, tests, and ignore rules.

- [ ] **Step 2: Push the legacy tag**

```powershell
git push origin legacy-before-current-project
```

Expected: the tag is created remotely and resolves to the pre-migration commit.

- [ ] **Step 3: Fast-forward remote main**

```powershell
git push origin migration/current-project-2026-10-05:main
```

Expected: push succeeds without force; no remote history is rewritten.

- [ ] **Step 4: Verify remote refs and clean state**

Run:

```powershell
git ls-remote --heads --tags origin
git fetch origin --prune
git status --short --branch
```

Expected: remote `main` points to the migration tip, the legacy tag points to `2ce01c3`, and the local working tree is clean.

- [ ] **Step 5: Record the final commit and repository URL**

Add the final commit hash and repository URL to the completion report; do not claim publication until the remote verification output confirms both refs.
