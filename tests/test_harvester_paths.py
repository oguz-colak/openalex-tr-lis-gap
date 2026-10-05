from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
HARVESTER_DIR = PROJECT_ROOT / "bby-metadata-project" / "logs"


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_harvesters_write_under_project_raw_data(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Import-time setup must not create outputs relative to the script's log directory."""
    monkeypatch.chdir(tmp_path)

    openalex = load_module("openalex_harvester_test", HARVESTER_DIR / "openalex_harvester.py")
    dergipark = load_module("dergipark_harvester_test", HARVESTER_DIR / "dergipark_oaipmh_harvester.py")
    bilgi_dunyasi = load_module("bilgi_dunyasi_harvester_test", HARVESTER_DIR / "bilgi_dunyasi_harvester.py")

    expected = PROJECT_ROOT / "bby-metadata-project" / "02_data_collection" / "raw_data"
    assert openalex.OUTPUT_DIR == expected / "openalex"
    assert dergipark.OUTPUT_DIR == expected / "dergipark"
    assert bilgi_dunyasi.BASE_DIR == expected / "bilgi_dunyasi"


def test_openalex_mailto_is_optional_and_not_hardcoded(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    openalex_path = HARVESTER_DIR / "openalex_harvester.py"
    source = openalex_path.read_text(encoding="utf-8")
    assert "@" not in source

    openalex = load_module("openalex_harvester_mailto_test", openalex_path)
    openalex.EMAIL = None
    captured: dict = {}

    class FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict:
            return {"results": []}

    def fake_get(url: str, *, params: dict, timeout: int) -> FakeResponse:
        captured.update(params)
        return FakeResponse()

    monkeypatch.setattr(openalex.requests, "get", fake_get)
    assert openalex.resolve_source_id(["2147-9682"], "Türk Kütüphaneciliği") is None
    assert "mailto" not in captured
