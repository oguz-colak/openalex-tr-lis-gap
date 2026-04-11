---
trigger: always_on
---

Automated Progress Logging

## Objective
To maintain a chronological and detailed audit trail of all research activities, data processing steps, and document modifications performed within this project.

## Instructions
After completing any significant task (e.g., running a script, fetching literature, updating a draft, or processing data), you MUST immediately append a log entry to the file named `progress_log.md` in the root directory.

## Logging Format
Each entry must follow this exact structure:
- **Timestamp:** [YYYY-MM-DD HH:MM]
- **Action:** A short, active-voice sentence describing what was done.
- **Changes:** A bulleted list of specific files created, modified, or deleted.
- **Outcome:** A brief note on the result (e.g., "10 papers fetched," "CSV generated").

## Constraints
1. **Consistency:** Do not skip logging even for small tasks.
2. **Persistence:** If `progress_log.md` does not exist, create it immediately.
3. **Clarity:** Use professional, technical language consistent with the LIS (Library and Information Science) domain.

## Example Entry
> [2026-04-08 11:45] - **Action:** Executed OpenAlex metadata extraction.
> - **Changes:** Created `data/raw/openalex_bby_works.json`.
> - **Outcome:** Retrieved metadata for 45 articles from 'Türk Kütüphaneciliği'.