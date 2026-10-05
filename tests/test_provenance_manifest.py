from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from scripts.provenance.build_manifest import build_manifest


def test_build_manifest_hashes_utf8_file_with_posix_relative_path(tmp_path: Path) -> None:
    target = tmp_path / "nested" / "Türkçe.json"
    target.parent.mkdir()
    content = "Bilgi Dünyası\n".encode("utf-8")
    target.write_bytes(content)

    manifest = build_manifest(tmp_path, [target])

    assert manifest["files"] == [
        {
            "path": "nested/Türkçe.json",
            "bytes": len(content),
            "sha256": hashlib.sha256(content).hexdigest(),
            "format": "json",
        }
    ]


def test_build_manifest_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        build_manifest(tmp_path, [tmp_path / "missing.xml"])
