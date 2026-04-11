# Data Dictionary: OpenAlex Metadata Analysis

Bu doküman, projede kullanılan veri setlerinin yapısını ve sütun tanımlarını içermektedir.

## Veri Seti: openalex_tr_lis_works.csv
**Konum:** `data/processed/`
**Açıklama:** Türk BBY dergilerinin OpenAlex API üzerinden çekilen veri setinin tüm alanlarını içeren işlenmiş CSV dosyası. Karmaşık JSON nesneleri (yazarlar, kurumlar vb.) hücre bazında JSON string olarak korunmuştur.

| Sütun Adı | Veri Tipi | Tanım | FAIR Notu |
| :--- | :--- | :--- | :--- |
| `id` | URI | OpenAlex üzerindeki kalıcı tanımlayıcı. | **Findable** (PID) |
| `doi` | URL | Yayının dijital nesne tanımlayıcısı. | **Findable** (PID) |
| `display_name` | String | Makalenin tam başlığı. | Human-readable |
| `publication_year` | Integer | Yayının yılı. | Temporal metadata |
| `authorships` | JSON String | Yazarlar ve kurumları içeren tam liste. | **Interoperable** (ORCID/ROR) |
| `primary_location` | JSON String | Kaynak ve erişim detaylarını içeren veri. | **Interoperable** |
| `cited_by_count` | Integer | Alınan toplam atıf sayısı. | Impact metric |
| `concepts` | JSON String | Konu etiketleri. | **Interoperable** |

## Veri Seti: openalex_bby_works_full.json
**Konum:** `data/raw/`  
**Açıklama:** OpenAlex API'den çekilen işlenmemiş (raw) üstveri verileri. Tüm üstveri alanlarını içeren ana depo.

| Alan (JSON Path) | Tip | Tanım | FAIR Notu |
| :--- | :--- | :--- | :--- |
| `results[].id` | URI | OpenAlex Work PID. | **Findable** (Globally Unique) |
| `results[].doi` | URL | Yayının DOI adresi. | **Findable** (PID) |
| `results[].display_name` | String | Makale başlığı. | Human-readable |
| `results[].publication_year`| Int | Yayın yılı. | Temporal Metadata |
| `results[].authorships[]` | List | Yazarlar ve kurumları. | **Interoperable** (ORCID/ROR) |
| `results[].locations[]` | List | Yayının bulunduğu kaynaklar. | **Accessible** (Open Access) |
| `results[].primary_location.source.id` | URI | Dergi (Source) PID. | **Interoperable** (Internal ID) |
| `results[].cited_by_count` | Int | Atıf sayısı. | Reusable Metric |
| `results[].concepts[]` | List | AI tabanlı konu etiketleri. | **Interoperable** (Vocabularies) |

## Veri Seti: openalex_state.json
**Konum:** `data/raw/`
**Açıklama:** API sorgu durumlarını (cursor) ve son tarama tarihlerini tutan sistem dosyası.