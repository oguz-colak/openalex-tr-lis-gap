"""Build deterministic provenance metadata for raw XML/JSON snapshots."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


def _format_for(path: Path) -> str | None:
    suffix = path.suffix.lower()
    if suffix in {".json", ".xml"}:
        return suffix[1:]
    return None


def build_manifest(root: Path, files: Iterable[Path]) -> dict:
    """Return deterministic file metadata relative to ``root``."""
    root = Path(root).resolve()
    entries = []

    for file in sorted((Path(item) for item in files), key=lambda item: item.as_posix()):
        resolved = file.resolve()
        if not resolved.is_file():
            raise FileNotFoundError(resolved)
        try:
            relative = resolved.relative_to(root)
        except ValueError as exc:
            raise ValueError(f"File is outside manifest root: {resolved}") from exc

        content = resolved.read_bytes()
        entry = {
            "path": relative.as_posix(),
            "bytes": len(content),
            "sha256": hashlib.sha256(content).hexdigest(),
        }
        file_format = _format_for(resolved)
        if file_format is not None:
            entry["format"] = file_format
        entries.append(entry)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files": entries,
    }


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    raw_data = root / "bby-metadata-project" / "02_data_collection" / "raw_data"
    files = sorted(
        path
        for path in raw_data.rglob("*")
        if path.is_file() and path.suffix.lower() in {".json", ".xml"}
    )
    output = root / "docs" / "data-provenance.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(build_manifest(root, files), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(files)} file entries to {output}")


if __name__ == "__main__":
    main()
