# Türkiye KBB Dergilerinde Üstveri Kalitesi Analizi Uygulama Planı

> **Uygulama notu:** Plan, mevcut kararları temel alır. Uygulama aşamasında parse → normalize → tekilleştir → eşleştir → tamlık → tutarlılık → çıktı üretimi sırası izlenecektir.

**Amaç:** Türkiye'de yayın yapan altı Kütüphane ve Bilgi Bilimi dergisinin ulusal platformlardaki üstverilerini OpenAlex ile karşılaştırarak tamlık ve kaynaklar arası tutarlılık düzeylerini ölçmek.

**Yaklaşım:** Beş dergi için DergiPark MODS, Bilgi Dünyası için kendi platformundan alınan MARC21/slim verisi ulusal referans kümesini oluşturur. OpenAlex JSON kayıtlarıyla başlık+yıl temelinde eşleştirme yapılır. İkinci boyut gerçek yayın nüshasına karşı doğruluk değil, ulusal kayıt ile OpenAlex arasındaki tutarlılık olarak raporlanır.

**Teknoloji:** Python; XML (`xml.etree.ElementTree` veya eşdeğeri), JSON, CSV/JSON ara çıktıları, pandas ve matplotlib/seaborn (gerektiğinde).

**Veri yolları:**
- Ulusal DergiPark verisi: `bby-metadata-project/02_data_collection/raw_data/dergipark/`
- Bilgi Dünyası MARC21 verisi: `bby-metadata-project/02_data_collection/raw_data/bilgi_dunyasi/oai_bd.xml`
- OpenAlex verisi: `bby-metadata-project/02_data_collection/raw_data/openalex/`

## Global constraints

- Altı dergideki tüm kayıtlar analize dahil edilecek; tür filtresi uygulanmayacak.
- Tür dağılımları ayrıca betimsel olarak raporlanacak.
- Anahtar kelime alanı ölçüm kapsamı dışındadır; yapısal karşılaştırılamazlık sınırlılık olarak yazılacaktır.
- Eşleştirme anahtarı normalize başlık + yıl olacaktır; DOI eşleştirme anahtarı olarak kullanılmayacak, ayrı bir alan olarak ölçülecektir.
- İkinci boyut “doğruluk” değil, “tutarlılık (kaynaklar arası uyum)” olarak adlandırılacaktır.
- B3 precision/recall ve karışıklık matrisi uygulanmayacaktır; gerçek etiket seti bulunmamaktadır.
- BD'de sayfa alanı bulunmadığı için sayfa karşılaştırması BD için uygulanamaz.
- BD tarihi tam tarih değil, yalnızca yıl düzeyinde karşılaştırılacaktır.
- BD kayıtlarının tekilleştirilmesi yapılacak; kayıt türleri silinmeyecek.

## Review focus

- Aynı başlığa sahip farklı yıllardaki kayıtlar yanlış eşleşmemeli; eşleştirmede yıl zorunlu olmalıdır.
- BD'deki `100$a` ve `720$a` yazarları tek bir yazar listesinde ve “Soyad, Ad” biçiminden normalize edilmelidir.
- OpenAlex `abstract_inverted_index` özetleri karşılaştırmadan önce doğru sırayla yeniden oluşturulmalıdır.
- BD `786$n` içindeki “Cilt … Sayı … (Yıl)” ifadesi cilt, sayı ve yıl alanlarına ayrılmalıdır.
- Boş ulusal kaynakta boş OpenAlex alanı “tam uyum” değil, karşılaştırılamaz/boş durum olarak işaretlenmelidir; CMI yalnızca ulusal alan doluyken OpenAlex alanı boşsa atanmalıdır.

## Kesinleşmiş veri kapsamı

| Dergi | Ulusal kaynak ve kayıt | OpenAlex kayıt |
|---|---:|---:|
| Türk Kütüphaneciliği | DergiPark, 1.037 | 1.918 |
| Arşiv Dünyası | DergiPark, 207 | 32 |
| Bilgi Yönetimi | DergiPark, 195 | 155 |
| Bilgi ve Belge Araştırmaları | DergiPark, 89 | 58 |
| LAM Research Journal | DergiPark, 74 | 55 |
| Bilgi Dünyası | bd.org.tr, 633 | 610 |
| **Toplam** | **2.235** | **2.828** |

Bilgi Dünyası verisi DergiPark'ta değildir; `bilgi_dunyasi/oai_bd.xml` ayrı ulusal platform verisi olarak kullanılacaktır. `harvest_log.json` içinde BD'nin görünmemesi analiz açısından engel değildir.

## Ölçüm alanları

Anahtar kelime çıkarıldıktan sonra **11 çekirdek alan** ölçülecektir:

| Alan | DergiPark MODS | BD MARC21 | OpenAlex JSON |
|---|---|---|---|
| Başlık | `titleInfo/title` | `245$a` | `title` |
| Yazarlar | `name` (`given` + `family`) | `100$a` + `720$a` | `authorships[].raw_author_name` |
| Yıl | `originInfo/dateIssued` | `008` veya `786$n` | `publication_year` |
| Tarih | `originInfo/dateIssued` | yalnız yıl | `publication_date` |
| DOI | `identifier[@type=doi]` | `024$a`, `$2=doi` | `doi` |
| Dil | `language/languageTerm` | `546$a` | `language` |
| Tür | `genre[@authority=marcgt]` | OAI `setSpec` | `type` |
| Cilt | `detail[@type=volume]/number` | `786$n` içinden ayrıştırılır | `biblio.volume` |
| Sayı | `detail[@type=issue]/number` | `786$n` içinden ayrıştırılır | `biblio.issue` |
| Sayfa | `extent/start` ve `extent/end` | yok | `biblio.first_page` / `last_page` |
| Özet | `abstract` | `520$a` | `abstract_inverted_index` |

## Uygulama görevleri

### Görev 1: Kaynak kayıtlarını ortak şemaya aktarma

- DergiPark XML kayıtlarını MODS alanlarından çıkar.
- BD MARC21 kayıtlarını `245`, `100`, `720`, `024`, `520`, `546`, `786`, `008` ve `setSpec` alanlarından çıkar.
- OpenAlex JSON kayıtlarını ortak şemaya aktar.
- Her kayda `journal`, `source`, `source_record_id`, `raw_fields` ve 11 ortak alanı ekle.
- BD'de `100$a` ve `720$a` birleştirilmeli; `024$a` yalnızca `$2=doi` olduğunda DOI kabul edilmelidir.
- OpenAlex özetleri inverted index'ten kelime konumlarına göre yeniden kurulmalıdır.

**Kontrol:** Her kaynak ve dergi için kayıt sayısı, alan doluluk sayısı ve tür dağılımı raporlanır.

### Görev 2: Normalizasyon ve tekilleştirme

- Metinlerde Unicode normalize et, baş/son boşlukları ve tekrar eden boşlukları kaldır, karşılaştırma için casefold uygula.
- Noktalama ve DOI URL öneklerini normalize et; DOI'lerde `https://doi.org/` ve `doi:` öneklerini kaldır.
- Türkçe karakterleri silme; karakterleri doğruluk hatasını gizlemeyecek şekilde koru.
- Yazarları ortak “ad soyad” biçimine getir; BD'deki “Soyad, Ad” biçimini dönüştür.
- Cilt, sayı, yıl ve sayfa değerlerini sayısal/metinsel eşdeğer biçime getir.
- Aynı kaynak içindeki yinelenen DOI kayıtlarını; DOI yoksa normalize başlık+yıl kayıtlarını tekilleştir.

**Kontrol:** BD'deki 633 kayıt için yinelenen başlıklar ve tekilleştirme sonucu açıkça raporlanır; hiçbir kayıt sessizce silinmez.

### Görev 3: Başlık+yıl ile eşleştirme

- Her dergi için ulusal ve OpenAlex kayıtlarını ayrı eşleştir.
- Birincil anahtar `normalized_title + publication_year` olacaktır.
- Aynı anahtar birden fazla kayda karşılık gelirse yazar benzerliği ve DOI yardımcı kanıt olarak kullanılmalıdır.
- Belirsiz eşleşmeler ayrı bir inceleme tablosuna yazılmalıdır; otomatik olarak kesin eşleşme sayılmamalıdır.
- Eşleşen, yalnız ulusalda bulunan ve yalnız OpenAlex'te bulunan kayıt sayılarını dergi bazında üret.

**Kontrol:** Aynı başlıklı fakat farklı yıllı kayıtların eşleşmediğini ve eşleşme oranlarını doğrula.

### Görev 4: Tamlık ölçümü (A1-A3)

- **A1 alan doluluk oranı:**
  `C_p(f) = f alanı dolu kayıt sayısı / platformdaki toplam kayıt sayısı × 100`
- **A2 kayıt tamlık indeksi:**
  `RCR_i = 11 alanda dolu alan sayısı / 11`
- **A3 platform tamlık skoru:** 11 alanın A1 oranlarının aritmetik ortalaması.
- Sonuçları kaynak × dergi × alan kırılımında üret.
- BD sayfa alanını “kaynakta bulunmuyor” olarak işaretle; genel platform ortalamasında bu alanın nasıl ele alındığını tabloda açıkça belirt.

**Çıktı:** Alan doluluk matrisi, kayıt tamlık dağılımı ve platform skorları.

### Görev 5: Tutarlılık ölçümü (B1-B2)

Ulusal platform kaydı vekil referans olarak kullanılacak; sonuçlar gerçek doğruluk değil, kaynaklar arası uyum olarak yorumlanacaktır.

- **B1 — Genel uyum:** Eşleşen kayıtlar üzerinde normalize değerlerin eşitlik oranı.
- **B2 — Uyuşmazlık tipolojisi:** Her karşılaştırılabilir alan ve kayıt için aşağıdaki durumlardan biri atanır:
  - **Tam uyum (FI):** Değerler normalize sonrası eşit veya önceden belirlenen benzerlik eşiğini geçiyor.
  - **Eksik (CMI):** Ulusal değer dolu, OpenAlex değeri boş.
  - **Kısmi (PMI):** Çok değerli alanda OpenAlex değerleri ulusal değerlerin alt kümesi.
  - **Uyuşmazlık (NMI):** İki değer de dolu fakat eşit/alt küme değil.
- Ulusal ve OpenAlex alanı da boşsa sonuç “iki tarafta da boş” olarak ayrı gösterilir; FI sayılmaz.
- Yazarlar için tam küme, alt küme ve kesişim oranı hesaplanır.
- Sayfa karşılaştırması BD dışındaki dergilerde; tarih karşılaştırması BD için yalnız yıl düzeyinde yapılır.
- B3 precision/recall/karışıklık matrisi uygulanmaz.

**Çıktı:** Alan bazında B1 uyum oranları ve FI/CMI/PMI/NMI dağılım tabloları.

### Görev 6: Tür dağılımı ve kapsam tabloları

- Tür filtresi uygulanmaz.
- DergiPark kayıtlarının `genre=article` dağılımı raporlanır; bu etiketin tür ayrımını sınırlı yansıttığı belirtilir.
- BD `setSpec` değerleri (MAK, GO, TE, ED, HAB vb.) ayrı dağılım olarak raporlanır.
- OpenAlex `type` değerleri (article, review, paratext, book-chapter vb.) ayrı dağılım olarak raporlanır.
- Tür dağılımı, eşleşme/kapsam sonuçlarının yorumlanmasına yardımcı olan betimsel bir tablo olacaktır; kayıtlar tür temelinde dışlanmayacaktır.

### Görev 7: Tablo, şekil ve yöntem çıktıları

- **Tablo 1:** Dergi bazında ulusal/OpenAlex kayıt sayıları, ortak kayıtlar, yalnız-ulusal ve yalnız-OpenAlex kayıtlar.
- **Tablo 2:** Kaynak × dergi × alan tamlık oranları.
- **Tablo 3:** Alan bazında B1 uyum oranı ve B2 FI/CMI/PMI/NMI dağılımı.
- **Tablo 4:** Üç kaynakta tür dağılımları.
- **Şekil 1:** Tamlık ısı haritası.
- **Şekil 2:** Alan bazında tutarlılık ve uyuşmazlık grafiği.
- Bildirinin analiz/yöntem bölümünde kaynak şeması farkları, eşleştirme kuralları ve karşılaştırma sınırları açıklanmalıdır.

## Yöntemsel sınırlılıklar

1. Tutarlılık, yayınların orijinal sürümüne (version of record) karşı değil, ulusal platform kaydına karşı ölçülmektedir; ortak hatalar görülemez.
2. Bu nedenle sonuçlar gerçek doğruluktan ziyade kaynaklar arası uyumu gösterir.
3. BD kayıtlarında sayfa bilgisi yoktur ve tarih tam tarih değil, yıl düzeyindedir.
4. DergiPark kayıtlarında tür etiketi tüm kayıtlar için `article` olduğundan, platform içi tür ayrımı yapılamaz.
5. Anahtar kelimeler farklı şema ve içerik yapıları nedeniyle karşılaştırma kapsamına alınmamıştır.
6. DOI kapsamı dergiler arasında değiştiği için DOI eşleştirme anahtarı yapılmamıştır.
7. Gerçek etiket seti bulunmadığından precision, recall, balanced accuracy ve karışıklık matrisi hesaplanmamıştır.

## Bildiride kullanılabilecek temel ifade

> Bu çalışmada üstveri kalitesi iki boyutta incelenmiştir: (i) platform-içi alan doluluklarını ve kayıt tamlığını ifade eden tamlık ve (ii) ulusal platform kayıtları ile OpenAlex kayıtları arasındaki alan düzeyli uyumu ifade eden kaynaklar arası tutarlılık. İkinci boyut bir yayın gerçeğine (version of record) dayalı doğruluk ölçümü değil, ulusal kayıtların vekil referans olarak kullanıldığı karşılaştırmalı bir uyum ölçümüdür.
