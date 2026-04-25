# DergiPark MODS Metadata Öznitelikleri (oai_mods)

Bu dosya, DergiPark OAI-PMH servisi üzerinden `metadataPrefix=oai_mods` parametresiyle çekilebilecek tüm hiyerarşik alanları ve açıklamalarını içerir.

## MODS Tablo Yapısı ve Açıklamalar

| Grup | Alan (JSON Yolu) | Açıklama |
| :--- | :--- | :--- |
| **Başlık Bilgisi** | `mods.titleInfo.title` | Yayının ana başlığı. |
| | `mods.titleInfo.subTitle` | Varsa alt başlık bilgisi. |
| **Yazar Bilgisi** | `mods.name.namePart.givenName` | Yazarın adı (genellikle MODS'ta ayrıştırılmış gelir). |
| | `mods.name.namePart.familyName` | Yazarın soyadı. |
| | `mods.name.affiliation` | Yazarın kurumsal bağı (Affiliation). *Not: DergiPark çıktısında genellikle boştur.* |
| | `mods.name.orcid` | Yazarın ORCID numarası. |
| **Yayın Bilgisi** | `mods.originInfo.publisher` | Yayını yayımlayan kurum/kuruluş veya dergi birimi. |
| | `mods.originInfo.dateIssued` | Yayının resmî yayınlanma tarihi. |
| **Tanımlayıcılar** | `mods.identifier.doi` | Dijital Nesne Tanımlayıcı (DOI). |
| | `mods.identifier.uri` | Yayının kalıcı web bağlantısı. |
| | `mods.identifier.issn / eissn` | Derginin basılı veya elektronik ISSN numarası. |
| **İçerik** | `mods.abstract` | Yayının özeti (Genellikle dilli/multilingual destekler). |
| | `mods.subject.topic` | Anahtar kelimeler ve konu başlıkları. |
| **Ev Sahibi Kaynak** | `mods.relatedItem.titleInfo.title` | Makalenin yayımlandığı derginin adı. |
| | `mods.relatedItem.part.volume` | Derginin cilt numarası. |
| | `mods.relatedItem.part.issue` | Derginin sayı numarası. |
| | `mods.relatedItem.part.extent.pageRange` | Makalenin ilgili sayıdaki sayfa aralığı (örn. 619-626). |
| **Teknik & Erişim** | `mods.accessCondition` | Erişim durumu (genellikle "open access"). |
| | `mods.language.languageTerm` | Yayının dili (ISO 639-2 veya RFC 3066 kodları). |

---

## Örnek MODS-JSON Yapısı

```json
{
  "mods": {
    "name": [
      {
        "namePart": { "givenName": null, "familyName": null },
        "affiliation": null,
        "role": "author"
      }
    ],
    "originInfo": { "publisher": null, "dateIssued": null },
    "abstract": null,
    "identifier": { "doi": null, "uri": null },
    "relatedItem": {
      "type": "host",
      "titleInfo": { "title": null },
      "part": { "volume": null, "issue": null, "extent": { "pageRange": null } }
    }
  }
}
```

---

# DergiPark Dublin Core Metadata Öznitelikleri (oai_dc)

Bu bölüm, DergiPark OAI-PMH servisi üzerinden `metadataPrefix=oai_dc` parametresiyle çekilen standart 15 Dublin Core alanını ve DergiPark/OJS eşleşmelerini kapsar.

## Dublin Core Tablo Yapısı ve Açıklamalar

| Alan (Tag) | DergiPark/OJS Karşılığı | Açıklama |
| :--- | :--- | :--- |
| `dc:title` | Makale Başlığı | Birincil makale başlığı. |
| `dc:creator` | Yazarlar | Yayını hazırlayan yazar/yazarlar listesi. |
| `dc:subject` | Anahtar Kelimeler | Makale anahtar kelimeleri (keywords). |
| `dc:description` | Özet (Abstract) | Makalenin kısa özeti. |
| `dc:publisher` | Dergi Adı / Yayıncı | Yayını basan dergi veya bağlı olduğu kurum. |
| `dc:date` | Yayın Tarihi | Makalenin resmî yayınlanma tarihi. |
| `dc:type` | Yayın Türü | Genellikle 'article' (makale) değeri döndürülür. |
| `dc:format` | Dosya Formatı | Çoğunlukla 'application/pdf' olarak belirtilir. |
| `dc:identifier` | DOI / URL | Makaleye ait kalıcı DOI numarası ve web adresi. |
| `dc:source` | Bibliyografik Kaynak | Dergi adı, cilt, sayı ve sayfa bilgileri (metin olarak). |
| `dc:language` | Dil Kodu | Yayının dili (örn. 'tr', 'en'). |
| `dc:rights` | Telif Hakları | Lisans ve kullanım hakları bilgisi. |
| `dc:contributor` | null | OJS OAI-PMH çıktısında genellikle boş döndürülür. |
| `dc:relation` | null | İlişkili kaynak bilgisi genellikle harmanlanmaz. |
| `dc:coverage` | null | Kapsam bilgisi genellikle standart OJS çıktısında yer almaz. |

---

## Örnek DC-JSON Yapısı

```json
{
    "dc:title": "Article Title",
    "dc:creator": ["Author Name 1", "Author Name 2"],
    "dc:subject": ["Keyword1", "Keyword2"],
    "dc:description": "Abstract content...",
    "dc:publisher": "Journal Name",
    "dc:date": "YYYY-MM-DD",
    "dc:type": "article",
    "dc:identifier": {
        "doi": "10.XXXX/XXXX",
        "url": "https://dergipark.org.tr/..."
    },
    "dc:source": "Journal Name, Vol. X No. Y",
    "dc:language": "tr",
    "dc:rights": "Copyright/License info"
}
```
