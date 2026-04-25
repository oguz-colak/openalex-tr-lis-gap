# AGENTS.md — Symposium Proceeding Pipeline Kuralları

Bu dosya, DergiPark OAI-PMH veri pipeline'ı üzerinde çalışan tüm agent'lar için bağlayıcı kurallardır.
Kuralları geçersiz kılmak veya kolaylık gerekçesiyle atlamak yasaktır.

---

## Kural 1 — Yalnızca `oai_mods` Formatı Kullanılır

`dergipark_harvester.py` içindeki `METADATA_PREFIXES` listesinde `oai_dc` ve `oai_marc` bulunmaktadır.
Bu formatları **asla** veri çekme hedefi olarak kullanma. Yalnızca `oai_mods` kullan.

```python
# YANLIŞ
METADATA_PREFIXES = ["oai_dc", "oai_mods", "oai_marc"]

# DOĞRU
METADATA_PREFIXES = ["oai_mods"]
```

**Neden:** `oai_dc` çok daha basit olduğu için agent'lar kendiliğinden oraya kayar.
`oai_mods` olmadan dil etiketi (AS2) ve funder (ROR) verileri kaybolur.

---

## Kural 2 — OAI-PMH XML `<error>` Etiketi Her Zaman Ayrıştırılır

OAI-PMH, hataları HTTP 200 ile döner. `response.status_code == 200` kontrolü yeterli değildir.
`check_oai_errors()` fonksiyonu her XML yanıtına uygulanmalıdır — bu `dergipark_harvester.py`'de
zaten mevcuttur, ancak hiçbir zaman atlanmamalıdır.

```python
# YANLIŞ — hata kontrolü atlandı
if response.status_code == 200:
    save_to_file(response.text, filename)

# DOĞRU
if response.status_code == 200:
    error = check_oai_errors(response.text)
    if error:
        raise ValueError(f"OAI-PMH Error: {error}")
    save_to_file(response.text, filename)
```

---

## Kural 3 — Pydantic Modeli Olmadan Veri Kaydedilmez

Herhangi bir XML parse veya metadata işleme kodu yazarken, önce Pydantic şeması tanımlanmalıdır.
Aşağıdaki alanlar **zorunludur, `Optional` yapılamaz:**

| Alan | Açıklama |
| ------ | ---------- |
| `title` | Makale başlığı |
| `language` | BCP-47 dil etiketi (örn. `tr`, `en`) |
| `publication_year` | 4 haneli tam sayı (1900–2100 aralığında) |
| `identifier_doi` | DOI string'i |
| `source_journal` | DergiPark dergi adı |

Diğer alanlar (`abstract`, `authors`, `funders`, `ror_ids`) `Optional` olabilir ama
şemada **açıkça belirtilmeli**, sessizce atlanmamalıdır.

---

## Kural 4 — Kayıt Sayısı Doğrulaması Zorunludur

`ListRecords` yanıtındaki `resumptionToken@completeListSize` değeri ile diske kaydedilen
kayıt sayısı karşılaştırılmalıdır. Pipeline kapanmadan önce bu kontrolü çalıştır:

```python
assert saved <= complete_list_size, (
    f"Count mismatch: saved={saved} > completeListSize={complete_list_size}"
)
if complete_list_size - saved > 0:
    log.warning("⚠ %d kayıt eksik", complete_list_size - saved)
```

`completeListSize` mevcut değilse (bazı sunucular göndermez) kayıt sayısını logla ve devam et.
Eksik kayıtları `"Tüm kayıtlar indirildi"` gibi sahte başarı mesajlarıyla örtme.
Hataları olduğu gibi raporla.

---

## Kural 5 — State File Her 100 Kayıtta Yazılır

Uzun çalışan harvest işlemlerinde her 100 kayıtta bir durum dosyasına yaz.
Format referansı: `data/raw/openalex_state.json` (mevcut örnek).

```python
if i % 100 == 0:
    write_state({"last_processed_index": i, "harvested_count": len(saved_files)})
```

Bu olmadan pipeline ortada kesilirse baştan başlamak gerekir.

---

## Genel Yasaklar

- `oai_dc` veya `oai_marc` formatlarına düşme — fark etsen bile
- Zorunlu Pydantic alanlarını `Optional` yapma
- HTTP 200'ü başarı sayma, XML `<error>` kontrolünü atlama
- Eksik kayıtları rapor etmeden geçme
- `try-except` bloklarını 3 seviyeden fazla iç içe yazma
