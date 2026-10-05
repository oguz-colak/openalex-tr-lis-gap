# Yeniden Üretilebilirlik Notları

## Snapshot kapsamı

Bu commit'te bulunan snapshot'lar dosya içeriklerinden yeniden sayıldığında
2.235 ulusal XML ve 2.828 OpenAlex JSON kaydı içerir:

| Dergi | Ulusal kayıt | OpenAlex kayıt |
|---|---:|---:|
| Türk Kütüphaneciliği | 1.037 | 1.918 |
| Arşiv Dünyası | 207 | 32 |
| Bilgi Yönetimi | 195 | 155 |
| Bilgi ve Belge Araştırmaları | 89 | 58 |
| LAM Research Journal | 74 | 55 |
| Bilgi Dünyası | 633 | 610 |
| **Toplam** | **2.235** | **2.828** |

OpenAlex snapshot'ının hasat özeti `harvest_log.json` içinde `2026-05-07`
tarih bilgisiyle bulunur. DergiPark ve Bilgi Dünyası XML dosyaları, kaynak
endpoint'lerinden alınan ham snapshot'lardır. Dosya boyutları ve SHA-256
özetleri [`data-provenance.json`](data-provenance.json) içinde tutulur.

## Kaynak endpoint'leri

- OpenAlex Works API: `https://api.openalex.org/works`
- DergiPark OAI-PMH: `https://dergipark.org.tr/api/public/oai/`
- Bilgi Dünyası OAI-PMH: `https://bd.org.tr/tr/oai`
- Bilgi Dünyası ISSN: `2148-354X`

API sonuçları zaman içinde değişebilir. Aynı sonuçları yeniden üretmek için
snapshot tarihi, source filtreleri, ISSN'ler ve `harvest_log.json` birlikte
değerlendirilmelidir.

## Ortam kurulumu

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

OpenAlex polite-pool iletişim adresi gerekiyorsa kod içine yazmak yerine:

```powershell
$env:OPENALEX_MAILTO = "kendi-adresiniz@example.org"
```

## Kontroller

```powershell
python -m pytest -q
python -m compileall -q bby-metadata-project tests scripts
python scripts/provenance/build_manifest.py
```

Manifest üreticisi yalnızca `bby-metadata-project/02_data_collection/raw_data/`
altındaki JSON/XML dosyalarını listeler. PDF, `.pyc`, `__pycache__`, geçici log
ve ortam dosyaları kasıtlı olarak repo kapsamına alınmaz.

## Analiz sınırları

Tutarlılık ölçümü yayınların version of record sürümüne karşı doğruluk değil,
ulusal platform kayıtları ile OpenAlex arasındaki kaynaklar arası uyumdur.
Bilgi Dünyası'nda sayfa alanı bulunmaz ve tarih yalnızca yıl düzeyinde
karşılaştırılır. Tam analiz kuralları ve sınırlılıklar için analiz planına
bakılmalıdır.
