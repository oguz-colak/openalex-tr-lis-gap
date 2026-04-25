# DergiPark OAI-PMH Üstveri Öznitelikleri

Bu belge, DergiPark OAI-PMH servisi üzerinden erişilen gerçek bir kayıt üzerinden (`article/1674520`) hem **Dublin Core (oai_dc)** hem de **MODS (oai_mods)** biçimlerindeki tüm üstveri alanlarını, gerçek değerleriyle ve açıklamalarıyla listeler.

- **Kayıt Kimliği:** `oai:dergipark.org.tr:record/1674520`
- **Son Değişiklik:** 2026-02-02
- **Yanıt Tarihi:** 2026-04-13T16:20:18Z

---

## 1. OAI-PMH Zarfı (Her İki Biçimde Ortak)

Her OAI-PMH yanıtında `<metadata>` bloğunun dışında yer alan çerçeve alanlarıdır.

| XPath | Değer (Örnek Kayıt) | Açıklama |
| :--- | :--- | :--- |
| `/OAI-PMH/responseDate` | `2026-04-13T16:20:18Z` | Sunucunun yanıtı ürettiği tarih ve saat (UTC, ISO 8601). |
| `/OAI-PMH/request/@verb` | `GetRecord` | Kullanılan OAI-PMH fiili. Tek kayıt çekmek için `GetRecord` kullanılır. |
| `/OAI-PMH/request/@metadataPrefix` | `oai_dc` / `oai_mods` | İstenen üstveri biçimi. |
| `/OAI-PMH/request/@identifier` | `oai:dergipark.org.tr:record/1674520` | Talep edilen kaydın OAI tanımlayıcısı. |
| `/OAI-PMH/GetRecord/record/header/identifier` | `oai:dergipark.org.tr:record/1674520` | Kaydın kalıcı OAI tanımlayıcısı. `oai:<kurum>:<kayıtNo>` biçimindedir. |
| `/OAI-PMH/GetRecord/record/header/datestamp` | `2026-02-02` | Kaydın havuzda son güncellendiği tarih (YYYY-MM-DD). |
| `/OAI-PMH/GetRecord/record/header/setSpec` | `tk` | Kaydın ait olduğu küme (set); genellikle derginin kısa adıdır. |

---

## 2. Dublin Core (oai_dc) Biçimi

Dublin Core, 15 temel alandan oluşan yalın ve geniş uyumlu bir üstveri standardıdır. DergiPark, `dc:` önekiyle sunulan alanları aşağıdaki şekilde doldurmaktadır.

### 2.1 Başlık — `dc:title`

Birden fazla dil için ayrı `<dc:title>` elemanı kullanılır; dil `xml:lang` niteliğiyle belirtilir.

| Nitelik | Değer |
| :--- | :--- |
| `xml:lang="tr-TR"` | `Bilgi ve Belge Yönetimi Bölümü Öğrencilerinin Yapay Zekâ Okuryazarlığı Düzeyleri Üzerine Bir Araştırma` |
| `xml:lang="en-US"` | `A Study on the Artificial Intelligence Literacy Levels of Information and Records Management Students` |

> Yayının birincil başlığı. DergiPark çok dilli başlık desteği sunar; bu sayede aynı alan, farklı dil etiketleriyle birden fazla kez tekrarlanabilir.

---

### 2.2 Yazar — `dc:creator`

Her yazar için ayrı bir `<dc:creator>` elemanı eklenir. Değer `Soyadı, Ad` biçimindedir.

| # | Değer |
| :--- | :--- |
| 1 | `Cengiz Mater, Emine` |
| 2 | `Yalçınkaya, Bahattin` |

> Dublin Core bu alanda yazar ile editör ayrımı yapmaz; tüm birincil katkıcılar bu alana yazılır. Sıralama, sistemdeki yazar sıralamasını yansıtır.

---

### 2.3 Konu / Anahtar Kelimeler — `dc:subject`

Her bir konu/anahtar kelime grubu ayrı bir `<dc:subject>` elemanında sunulur.

| # | Değer | Tür |
| :--- | :--- | :--- |
| 1 | `Library and Information Studies (Other)` | ASJC disiplin sınıflaması (İngilizce) |
| 2 | `Kütüphane ve Bilgi Çalışmaları (Diğer)` | ASJC disiplin sınıflaması (Türkçe) |
| 3 | `Yapay zekâ (YZ),Yapay zekâ (YZ) okuryazarlığı,Bilgi ve Belge Yönetimi Bölümü` | Yazar anahtar kelimeleri (Türkçe, virgülle ayrılmış) |
| 4 | `Artificial Intelligence (AI),Artificial Intelligence (AI) literacy,Information and Records Management Department` | Yazar anahtar kelimeleri (İngilizce, virgülle ayrılmış) |

> **Dikkat:** Anahtar kelimeler virgülle ayrılmış tek bir metin olarak gelir; ayrıştırmak için split gereklidir. Disiplin sınıflaması ile yazar anahtar kelimeleri aynı alanda birbirine karışır.

---

### 2.4 Açıklama / Özet — `dc:description`

Özet, dile göre ayrı `<dc:description>` elemanlarında sunulur.

| Nitelik | Değer |
| :--- | :--- |
| `xml:lang="tr-TR"` | *(Türkçe özet — ~400 kelime)* Amaç, Yöntem, Bulgular ve Sonuç bölümlerinden oluşan yapılandırılmış özet metni. |
| `xml:lang="en-US"` | *(İngilizce özet — ~350 kelime)* Purpose, Method, Findings ve Implications başlıklı yapılandırılmış özet metni. |

> Ham XML'de CDATA bloğu içinde sunulur. DergiPark, yapılandırılmış özetleri tek bir metin olarak birleştirir; bölüm başlıkları (Amaç:, Yöntem: vb.) metnin içinde yer alır.

---

### 2.5 Yayıncı — `dc:publisher`

| Değer |
| :--- |
| `Türk Kütüphaneciler Derneği` |

> Yayını yayımlayan dernek, kurum veya ticari yayıncı adı. DergiPark'ta genellikle derneğin adıdır.

---

### 2.6 Yayın Tarihi — `dc:date`

| Değer | Biçim |
| :--- | :--- |
| `2025-12-30` | ISO 8601 (YYYY-MM-DD) |

> Makalenin dergide resmi olarak yayımlandığı tarih. Çevrimiçi erken erişim tarihi değil, sayıdaki yayım tarihidir.

---

### 2.7 Yayın Türü — `dc:type`

| Değer |
| :--- |
| `info:eu-repo/semantics/article` |

> DRIVER/OpenAIRE sözdizimini kullanan URI tabanlı kaynak türü. `article` = hakemli dergi makalesi. Olası diğer değerler: `bookPart`, `conferenceObject`, `review`.

---

### 2.8 Dosya Biçimi — `dc:format`

| Değer |
| :--- |
| `application/pdf` |

> Yayının sunulduğu MIME türü. DergiPark'ta PDF varsayılan biçimdir.

---

### 2.9 Tanımlayıcı — `dc:identifier`

Aynı kayda ait birden fazla tanımlayıcı, tekrarlayan `<dc:identifier>` elemanları olarak gelir.

| # | Değer | Tür |
| :--- | :--- | :--- |
| 1 | `https://dergipark.org.tr/en/pub/tk/article/1674520` | DergiPark makale URL'si |
| 2 | `https://doi.org/10.24146/tk.1674520` | DOI (kalıcı tanımlayıcı) |
| 3 | `https://izlik.org/JA98XY65PC` | Kısa URL (izlik.org servisi) |

> **Tanımlama önerisi:** `doi.org` ile başlayan değer DOI; `dergipark.org.tr` ile başlayan değer platform URL'si olarak ayrıştırılabilir.

---

### 2.10 Kaynak — `dc:source`

| Değer |
| :--- |
| `Türk Kütüphaneciliği, Vol. 39 No. 4` |

> Makalenin yayımlandığı dergiye ait bibliyografik bilgiyi düz metin olarak içerir. Cilt ve sayı bilgisi bu alanda birleşik olarak sunulur; ayrıştırmak için regex gerekebilir.

---

### 2.11 Dil — `dc:language`

| Değer | Standart |
| :--- | :--- |
| `tr` | ISO 639-1 |

> Yayının birincil dili. DergiPark iki harfli ISO 639-1 kodunu kullanır (`tr`, `en` vb.).

---

### 2.12 İlişki — `dc:relation`

DergiPark, kaydı çeşitli bağlamlara bağlamak için birden fazla `<dc:relation>` elemanı ekler.

| # | Değer | Açıklama |
| :--- | :--- | :--- |
| 1 | `https://dergipark.org.tr/en/pub/tk` | Derginin ana sayfası |
| 2 | `https://dergipark.org.tr/en/pub/tk/archive` | Derginin arşiv sayfası |
| 3 | `https://dergipark.org.tr/en/pub/tk/issue/94987` | Makalenin ait olduğu sayının sayfası |
| 4 | `https://doi.org/10.24146/tk.1674520` | DOI bağlantısı (dc:identifier ile tekrar eder) |
| 5 | `https://izlik.org/JA98XY65PC` | Kısa URL (dc:identifier ile tekrar eder) |

> **Not:** `dc:relation`, `dc:identifier` ile çakışan değerler içerebilir. Veri işleme sırasında bu tekrarları tekilleştirmek gerekebilir.

---

### Dublin Core Alanları — Özet Tablosu

| Alan | Tekrar? | Dil Niteliği? | Bu Kayıtta Dolu mu? | Açıklama |
| :--- | :---: | :---: | :---: | :--- |
| `dc:title` | Evet | Evet | Evet (tr + en) | Makale başlığı |
| `dc:creator` | Evet | Hayır | Evet (2 yazar) | Yazar adları |
| `dc:subject` | Evet | Hayır | Evet (4 grup) | Konu/anahtar kelimeler |
| `dc:description` | Evet | Evet | Evet (tr + en) | Özet metni |
| `dc:publisher` | Hayır | Hayır | Evet | Yayıncı adı |
| `dc:date` | Hayır | Hayır | Evet | Yayın tarihi |
| `dc:type` | Hayır | Hayır | Evet | Kaynak türü |
| `dc:format` | Hayır | Hayır | Evet | Dosya biçimi |
| `dc:identifier` | Evet | Hayır | Evet (3 değer) | URL, DOI, kısa URL |
| `dc:source` | Hayır | Hayır | Evet | Dergi, cilt, sayı (metin) |
| `dc:language` | Hayır | Hayır | Evet | Dil kodu |
| `dc:relation` | Evet | Hayır | Evet (5 değer) | İlişkili kaynaklar |
| `dc:rights` | — | — | **Hayır** | Bu kayıtta mevcut değil |
| `dc:contributor` | — | — | **Hayır** | Bu kayıtta mevcut değil |
| `dc:coverage` | — | — | **Hayır** | Bu kayıtta mevcut değil |

---

## 3. MODS (oai_mods) Biçimi

MODS (Metadata Object Description Schema), Dublin Core'a kıyasla çok daha ayrıntılı ve hiyerarşik bir yapı sunar. Yazar adlarını `givenName` / `familyName` olarak ayırır, sayfa aralığı gibi ek bibliyografik alanlar içerir.

### 3.1 Kaynak Türü — `typeOfResource`

| Değer |
| :--- |
| `text` |

> Kaydın genel kaynak türü. MODS kontrolü listesinden alınır: `text`, `still image`, `moving image`, `sound recording` vb.

---

### 3.2 Tür — `genre`

| `@authority` | Değer |
| :--- | :--- |
| `marcgt` | `article` |

> MARC Genres Terms (marcgt) otoritesine göre kaynak türü. Dublin Core'daki `dc:type` alanının daha ayrıntılı karşılığıdır.

---

### 3.3 Başlık Bilgisi — `titleInfo/title`

| `@xml:lang` | Değer |
| :--- | :--- |
| `tr-TR` | `Bilgi ve Belge Yönetimi Bölümü Öğrencilerinin Yapay Zekâ Okuryazarlığı Düzeyleri Üzerine Bir Araştırma` |
| `en-US` | `A Study on the Artificial Intelligence Literacy Levels of Information and Records Management Students` |

> Dublin Core'dan farklı olarak başlık, ayrı bir `<titleInfo>` bloğunda `<title>` alt elemanı olarak yer alır. Alt başlık için `<subTitle>` kullanılır (bu kayıtta yok).

---

### 3.4 Yazar Bilgisi — `name`

Her yazar için ayrı bir `<name>` bloğu oluşturulur; ad ve soyad ayrıştırılmış halde gelir.

| Yazar | `@type` | `namePart[@type="given"]` | `namePart[@type="family"]` | `roleTerm` |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `personal` | `Emine` | `Cengiz Mater` | `author` |
| 2 | `personal` | `Bahattin` | `Yalçınkaya` | `author` |

> **MODS'un Dublin Core'a göre avantajı:** Ad ve soyad ayrıştırılmış gelir; atıf biçimlendirmesi ve yazar normalizasyonu kolaylaşır. `affiliation` ve `orcid` alt elemanları bu yapıda tanımlıdır; ancak bu kayıtta dolu değildir.

---

### 3.5 Yayın Bilgisi — `originInfo`

| Alt Eleman | Nitelikler | Değer |
| :--- | :--- | :--- |
| `dateIssued` | `@encoding="w3cdtf"`, `@keyDate="yes"` | `2025-12-30` |
| `publisher` | — | `Türk Kütüphaneciler Derneği` |

> `@keyDate="yes"` niteliği, birden fazla tarih alanı olduğu durumlarda hangi tarihin birincil/arama tarihi olduğunu belirtir. `@encoding="w3cdtf"` W3C Date and Time Format standardını ifade eder (ISO 8601 ile uyumlu).

---

### 3.6 Dil — `language/languageTerm`

| `@type` | `@authority` | Değer |
| :--- | :--- | :--- |
| `code` | `rfc3066` | `tr` |

> RFC 3066 dil etiketi standardı. Dublin Core'daki `dc:language` ile aynı değeri taşır; ancak MODS bu değerin hangi otoriteye göre verildiğini `@authority` niteliğiyle açıkça belirtir.

---

### 3.7 Özet — `abstract`

| `@xml:lang` | Değer |
| :--- | :--- |
| `tr-TR` | *(Türkçe yapılandırılmış özet metni)* |
| `en-US` | *(İngilizce yapılandırılmış özet metni)* |

> Dublin Core'daki `dc:description` alanının MODS karşılığıdır. Yapı ve içerik aynıdır; MODS'ta ayrıca `@displayLabel` niteliğiyle farklı özet türleri (örn. "Graphical Abstract") işaretlenebilir.

---

### 3.8 Konu Başlıkları — `subject/topic`

| # | Değer | Tür |
| :--- | :--- | :--- |
| 1 | `Library and Information Studies (Other)` | ASJC disiplin sınıflaması (İngilizce) |
| 2 | `Kütüphane ve Bilgi Çalışmaları (Diğer)` | ASJC disiplin sınıflaması (Türkçe) |
| 3 | `Yapay zekâ (YZ),Yapay zekâ (YZ) okuryazarlığı,Bilgi ve Belge Yönetimi Bölümü` | Yazar anahtar kelimeleri (Türkçe) |
| 4 | `Artificial Intelligence (AI),Artificial Intelligence (AI) literacy,Information and Records Management Department` | Yazar anahtar kelimeleri (İngilizce) |

> Dublin Core'daki `dc:subject` ile aynı değerler; ancak her biri ayrı `<subject>` bloğunda sunulur. MODS'ta `@authority` niteliğiyle konu otoritesi (LCSH, MeSH vb.) belirtilebilir; bu kayıtta belirtilmemiştir.

---

### 3.9 Tanımlayıcılar — `identifier`

| `@type` | Değer |
| :--- | :--- |
| `uri` | `https://dergipark.org.tr/en/pub/tk/article/1674520` |
| `doi` | `https://doi.org/10.24146/tk.1674520` |
| `uri` (2. tekrar) | `https://izlik.org/JA98XY65PC` |

> MODS, tanımlayıcı türünü `@type` niteliğiyle açıkça belirtir (`doi`, `uri`, `isbn`, `issn` vb.). Bu durum Dublin Core'daki tanımlayıcı türü belirsizliğini ortadan kaldırır.

---

### 3.10 Konum — `location/url`

| Değer |
| :--- |
| `https://dergipark.org.tr/en/pub/tk/article/1674520` |

> Kaydın fiziksel/dijital konumunu belirtir. `identifier[@type="uri"]` ile aynı değeri taşır; erişim URL'si olarak işaretlenmiş özel bir alandır.

---

### 3.11 İlişkili Kayıt (Ev Sahibi Dergi) — `relatedItem[@type="host"]`

Makalenin yayımlandığı dergiye ait bibliyografik bilgiler bu blokta hiyerarşik olarak sunulur.

| Alan | XPath | Değer |
| :--- | :--- | :--- |
| Dergi Adı | `relatedItem/titleInfo/title` | `Türk Kütüphaneciliği` |
| Cilt | `relatedItem/part/detail[@type="volume"]/number` | `39` |
| Sayı | `relatedItem/part/detail[@type="issue"]/number` | `4` |
| İlk Sayfa | `relatedItem/part/extent[@unit="pages"]/start` | `381` |
| Son Sayfa | `relatedItem/part/extent[@unit="pages"]/end` | `410` |

> **MODS'un en önemli avantajlarından biri:** Cilt, sayı ve sayfa aralığı yapılandırılmış alt elemanlarda ayrı ayrı gelir. Dublin Core'da bu bilgiler yalnızca `dc:source` alanında düz metin olarak bir arada sunulur ve ayrıştırma gerektirir.

---

### MODS Alanları — Özet Tablosu

| Alan (XPath özeti) | Bu Kayıtta Dolu mu? | Dublin Core Karşılığı | Açıklama |
| :--- | :---: | :--- | :--- |
| `typeOfResource` | Evet | — | Genel kaynak türü |
| `genre` | Evet | `dc:type` | Ayrıntılı kaynak türü |
| `titleInfo/title` | Evet (tr + en) | `dc:title` | Başlık |
| `name/namePart[given]` | Evet | `dc:creator` (kısmi) | Yazar adı (ayrıştırılmış) |
| `name/namePart[family]` | Evet | `dc:creator` (kısmi) | Yazar soyadı (ayrıştırılmış) |
| `name/affiliation` | **Hayır** | — | Yazar kurumu |
| `name/orcid` | **Hayır** | — | Yazar ORCID |
| `originInfo/dateIssued` | Evet | `dc:date` | Yayın tarihi |
| `originInfo/publisher` | Evet | `dc:publisher` | Yayıncı |
| `language/languageTerm` | Evet | `dc:language` | Dil kodu |
| `abstract` | Evet (tr + en) | `dc:description` | Özet |
| `subject/topic` | Evet (4 grup) | `dc:subject` | Konu/anahtar kelimeler |
| `identifier[@type="uri"]` | Evet | `dc:identifier` | URL tanımlayıcısı |
| `identifier[@type="doi"]` | Evet | `dc:identifier` | DOI tanımlayıcısı |
| `location/url` | Evet | `dc:identifier` | Erişim URL'si |
| `relatedItem/titleInfo/title` | Evet | `dc:source` (kısmi) | Dergi adı |
| `relatedItem/part/detail[volume]` | Evet | `dc:source` (kısmi) | Cilt numarası |
| `relatedItem/part/detail[issue]` | Evet | `dc:source` (kısmi) | Sayı numarası |
| `relatedItem/part/extent/start` | Evet | — | İlk sayfa numarası |
| `relatedItem/part/extent/end` | Evet | — | Son sayfa numarası |
| `accessCondition` | **Hayır** | `dc:rights` | Erişim koşulları |

---

## 4. Biçimler Arası Karşılaştırma

| Özellik | Dublin Core (oai_dc) | MODS (oai_mods) |
| :--- | :--- | :--- |
| Yapı karmaşıklığı | Düz (flat), 15 alan | Hiyerarşik, çok sayıda alt eleman |
| Yazar ayrıştırma | `Soyad, Ad` biçiminde tek metin | Ad ve soyad ayrı elemanlarda |
| Sayfa aralığı | Yok | `start` / `end` olarak ayrı |
| Cilt/sayı | `dc:source` metninde gömülü | Ayrı `detail` elemanlarında |
| Tanımlayıcı türü | Tür belirtilmez; URL/DOI karışık | `@type="doi"`, `@type="uri"` ile net |
| Dil otoritesi | Belirtilmez | `@authority="rfc3066"` |
| Anahtar kelimeler | Virgülle birleşik tek metin | Ayrı `<subject>` bloklarında (içerik aynı) |
| Eksik alanlar | `dc:rights`, `dc:contributor`, `dc:coverage` yok | `affiliation`, `orcid`, `accessCondition` yok |
| Öneri | Hızlı veri çekme / basit kullanım | Bibliyografik ayrıntı gerektiren durumlar |
