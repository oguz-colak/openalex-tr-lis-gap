from __future__ import annotations

import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator


class ArticleMetadata(BaseModel):
    # --- ZORUNLU ALANLAR (AGENTS.md Kural 3) ---
    title_tr: str
    language: str
    publication_year: int
    identifier_doi: str
    source_journal: str

    # --- PROVENANCE FIELDS (FIX 5) ---
    source_system: str
    metadata_format: str
    is_inferred: bool = False

    # --- OPSIYONEL ALANLAR ---
    title_en: Optional[str] = None
    abstract_tr: Optional[str] = None
    abstract_en: Optional[str] = None
    authors: list[str] = Field(default_factory=list)
    date_issued: Optional[str] = None
    publisher: Optional[str] = None
    funders: list[str] = Field(default_factory=list)
    ror_ids: list[str] = Field(default_factory=list)

    @field_validator("language")
    @classmethod
    def validate_language(cls, v: str) -> str:
        # BCP-47 temel format: iki veya üç harfli dil kodu
        if not re.match(r"^[a-zA-Z]{2,3}(-[a-zA-Z0-9]{2,8})*$", v):
            raise ValueError(f"Geçersiz BCP-47 dil etiketi: '{v}'")
        return v.lower()

    @field_validator("publication_year")
    @classmethod
    def validate_year(cls, v: int) -> int:
        if not (1900 <= v <= 2100):
            raise ValueError(f"Yayın yılı 1900-2100 aralığında olmalı, alınan: {v}")
        return v

    @field_validator("identifier_doi")
    @classmethod
    def validate_doi(cls, v: str) -> str:
        # Tam URL veya düz DOI kabul et, normalize et
        v = v.strip()
        if v.startswith("https://doi.org/"):
            v = v[len("https://doi.org/"):]
        elif v.startswith("http://doi.org/"):
            v = v[len("http://doi.org/"):]
        if not v.startswith("10."):
            raise ValueError(f"Geçersiz DOI formatı: '{v}'")
        return v

    @field_validator("title_tr")
    @classmethod
    def validate_title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("title_tr boş olamaz")
        return v.strip()

    @model_validator(mode="after")
    def validate_date_year_consistency(self) -> ArticleMetadata:
        if self.date_issued:
            match = re.match(r"^(\d{4})", self.date_issued)
            if match:
                year_from_date = int(match.group(1))
                if year_from_date != self.publication_year:
                    raise ValueError(
                        f"publication_year ({self.publication_year}) ile "
                        f"date_issued yılı ({year_from_date}) uyuşmuyor"
                    )
        return self
