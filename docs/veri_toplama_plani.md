# 📋 Kapsamlı Veri Toplama Eylem Planı
## 6 BBY Dergisi | OpenAlex + DergiPark | Tüm Zamanlar

---

## SORUN RAPORU (Teşhis)

### A. OpenAlex (fetch_openalex.py) — Kritik Hatalar

| Sorun | Detay | Etki |
|---|---|---|
| Bilgi Dünyası ISSN eksik | 2148-354X var ama issn_l 1302-3217 eksik | 1.052 kayıt atlanmış |
| TK Print ISSN eksik | 2147-9682 var ama issn_l 1300-0039 eksik | Eksik kayıtlar |
| Yanıltıcı parametre | start_year/end_year API'ye uygulanmıyor | Şimdilik sorun yok |

### B. DergiPark (fetch_dergipark.py) — Orta Sorunlar

| Sorun | Detay | Etki |
|---|---|---|
| BD ayrı endpoint | bd.org.tr SSL 526 hatası | Güvenilirlik riski |
| TK yıl parse hatası | Bazı tarihlerde "19" çıkıyor | Analiz güvenilirliği |

---

## GERÇEK BEKLENEN KAYIT SAYILARI (Doğrulanmış)

### OpenAlex Source API
| Dergi | ISSN-L | Beklenen |
|---|---|---|
| Bilgi Dünyası | 1302-3217 | 1.052 |
| Türk Kütüphaneciliği | 1300-0039 | 546 |
| Bilgi Yönetimi | 2636-8544 | 147 |
| Bilgi ve Belge Araştırmaları | 2148-8975 | 55 |
| LAMRe | 2718-0832 | 55 |
| Arşiv Dünyası | 2147-2599 | 32 |
| TOPLAM | | ~1.887 |

Mevcut çekimde 1.382 kayıt var → 505 kayıt eksik (Bilgi Dünyası dahil).

---

## ADIM 1 — OpenAlex Betiğini Düzelt

Düzeltilecek ISSN listesi:

```python
bby_issns = [
    "1300-0039",  # TK print (EKLENDI)
    "2147-9682",  # TK e-ISSN
    "1302-3217",  # BD print (EKLENDI - kritik)
    "2148-354X",  # BD e-ISSN
    "2636-8544",  # Bilgi Yönetimi
    "2718-0832",  # LAMRe
    "2147-2599",  # Arşiv Dünyası (geçerli olan bu)
    "2148-8975",  # Bilgi ve Belge Araştırmaları
]
# per-page: 100 -> 200 yap
# start_year/end_year parametrelerini kaldır
```

Çıktı: data/raw/openalex_bby_works_full.json

---

## ADIM 2 — DergiPark Betiğini Düzelt

```python
# Bilgi Dünyası için bd.org.tr yerine DergiPark'ı kullan
{"name": "Bilgi Dünyası", "spec": "bd",
 "base_url": "https://dergipark.org.tr/api/public/oai/"}
# spec="bd" doğrulanmalı — ListSets ile kontrol et
```

Yıl parse düzeltmesi ekle:

```python
import re
def parse_year(date_val):
    m = re.search(r'\b(1[89]\d{2}|20[012]\d)\b', date_val or "")
    return int(m.group(1)) if m else None
```

Çıktı: data/raw/dergipark_ground_truth_full.json

---

## ADIM 3 — Doğrulama

- OpenAlex: her dergi için sayı == Source API beklentisi?
- DergiPark: TK 1952'ye kadar iniyor mu?
- BD için DergiPark çekimi > 633 kayıt mi?

---

## ADIM 4 — CSV ve Karşılaştırma

Hedef:
- data/processed/openalex_full.csv
- data/processed/dergipark_full.csv
- data/processed/comparison_matrix.csv

Analiz boyutları:
1. Kapsam farkı (DergiPark'ta olup OA'da olmayan)
2. Dil etiketi hatası (TR vs EN)
3. Kurum bilgisi kaybı (affiliation boşluğu)
4. Belge türü hatası

---

## UYGULAMA SIRASI

1. fetch_openalex.py düzelt + çalıştır (~30 dk)
2. fetch_dergipark.py düzelt + çalıştır (~60-90 dk)
3. Doğrulama kontrolleri (~15 dk)
4. CSV dönüşüm + analiz (~30 dk)
