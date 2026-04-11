# Data Dictionary: OpenAlex Metadata Analysis

Bu doküman, projede kullanılan veri setlerinin yapısını ve sütun tanımlarını içermektedir.

## Veri Seti: openalex_bby_works_full.csv
**Konum:** `data/processed/`
**Açıklama:** Türk BBY dergilerinin OpenAlex API üzerinden çekilen ve analiz için temizlenen tam veri seti.

| Sütun Adı | Veri Tipi | Tanım | FAIR Notu |
| :--- | :--- | :--- | :--- |
| `id` | URI | OpenAlex üzerindeki kalıcı tanımlayıcı. | **Findable** (PID) |
| `doi` | URL | Yayının dijital nesne tanımlayıcısı. | **Findable** (PID) |
| `title` | String | Makalenin başlığı. | Human-readable |
| `publication_year` | Integer | Yayının yılı. | Temporal metadata |
| `abstract` | Text | Makalenin özeti (Varlığı kalite metriğidir). | **Reusable** (Content) |
| `affiliations` | JSON/String | Yazar kurum bilgileri (ROR ID içerir). | **Interoperable** |
| `host_venue` | String | Yayının çıktığı dergi adı (Türk Kütüphaneciliği vb.). | Contextual metadata |
| `cited_by_count` | Integer | Alınan toplam atıf sayısı. | Impact metric |

## Veri Seti: openalex_state.json
**Konum:** `data/raw/`
**Açıklama:** API sorgu durumlarını ve son tarama tarihlerini tutan sistem dosyası.