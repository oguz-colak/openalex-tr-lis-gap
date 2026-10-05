# Türkiye KBB Dergilerinde Üstveri Kalitesi

Bu repo, Türkiye'de yayımlanan altı Kütüphane ve Bilgi Bilimi (KBB)
dergisinin ulusal platformlardaki üstverilerini OpenAlex kayıtlarıyla
karşılaştıran yeniden üretilebilir araştırma çalışma alanıdır.

## Kapsam

- Ulusal kaynaklar: DergiPark MODS ve Bilgi Dünyası MARCXML.
- OpenAlex kaynağı: dergi bazında JSON çalışma kayıtları.
- Ulusal kayıt sayısı: **2.235**.
- OpenAlex kayıt sayısı: **2.828**.
- Karşılaştırma alanları: başlık, yazarlar, yıl, tarih, DOI, dil, tür, cilt,
  sayı, sayfa ve özet.
- Analiz boyutları: alan doluluğu/kayıt tamlığı ve kaynaklar arası tutarlılık.

Kesin kurallar ve metodolojik sınırlılıklar için
[`docs/methodology/analysis-plan.md`](docs/methodology/analysis-plan.md)
dosyasına bakın.

## Dizin yapısı

```text
bby-metadata-project/
├── 02_data_collection/raw_data/
│   ├── dergipark/       # Beş derginin MODS XML snapshot'ları
│   ├── bilgi_dunyasi/   # Bilgi Dünyası MARCXML snapshot'ı
│   └── openalex/        # Altı derginin OpenAlex JSON snapshot'ları
└── logs/
    ├── *_harvester.py   # Veri toplama betikleri
    └── normalization.md # Normalizasyon kararları ve bulgular
docs/
├── methodology/         # Analiz planı ve alan sözlüğü
├── data-provenance.json # Snapshot hash ve boyut manifesti
└── reproducibility.md   # Ortam ve çalıştırma talimatları
scripts/provenance/      # Manifest üretim aracı
tests/                   # Migration ve provenance testleri
```

## Hızlı başlangıç

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q
python scripts/provenance/build_manifest.py
```

Harvester betikleri ağ erişimi gerektirir ve mevcut raw snapshot'ların üzerine
yazabilir. OpenAlex polite-pool iletişim adresi gerekiyorsa çalışma öncesinde
ortam değişkeni olarak verin:

```powershell
$env:OPENALEX_MAILTO = "kendi-adresiniz@example.org"
```

PDF tam metinleri, geçici loglar, Python cache dosyaları ve credential dosyaları
repo kapsamı dışındadır. Ham bibliyografik XML/JSON kayıtları ise snapshot ve
provenance amacıyla korunur.

## Lisans ve kullanım notu

Bu repo araştırma yeniden üretilebilirliği içindir. Harici kaynakların kullanım
koşulları, telifleri ve API politikaları ayrıca geçerlidir.
