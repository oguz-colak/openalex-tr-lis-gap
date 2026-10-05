# Ortak Üstveri Alanları

Analizde üç kaynaktan çıkarılan kayıtlar aşağıdaki 11 çekirdek alan üzerinden
ortak şemaya aktarılır. Anahtar kelime alanı şema farkları nedeniyle ölçüm
kapsamında değildir.

| Ortak alan | DergiPark MODS | Bilgi Dünyası MARC21 | OpenAlex |
|---|---|---|---|
| Başlık | `titleInfo/title` | `245$a` | `title` |
| Yazarlar | `name` (`given` + `family`) | `100$a` + `720$a` | `authorships[].raw_author_name` |
| Yıl | `originInfo/dateIssued` | `008` veya `786$n` | `publication_year` |
| Tarih | `originInfo/dateIssued` | yalnız yıl | `publication_date` |
| DOI | `identifier[@type=doi]` | `024$a`, `$2=doi` | `doi` |
| Dil | `language/languageTerm` | `546$a` | `language` |
| Tür | `genre[@authority=marcgt]` | OAI `setSpec` | `type` |
| Cilt | `detail[@type=volume]/number` | `786$n` içinden | `biblio.volume` |
| Sayı | `detail[@type=issue]/number` | `786$n` içinden | `biblio.issue` |
| Sayfa | `extent/start`, `extent/end` | bulunmuyor | `biblio.first_page`, `last_page` |
| Özet | `abstract` | `520$a` | `abstract_inverted_index` |

## Normalizasyon ilkeleri

- Unicode NFC uygulanır; Türkçe karakterler korunur.
- Başlık ve DOI karşılaştırmaları boşluk, noktalama ve URL önekleri
  normalize edilerek yapılır.
- DOI eşleştirme anahtarı değildir; ayrı bir alan olarak ölçülür.
- Yazarlar ortak ad-soyad biçimine getirilir; Bilgi Dünyası'nda `100$a` ve
  `720$a` birleştirilir.
- OpenAlex özetleri inverted index konumlarına göre yeniden kurulur.
- Eşleştirme anahtarı normalize başlık + yıldır; belirsiz eşleşmeler ayrı
  inceleme tablosunda tutulmalıdır.
