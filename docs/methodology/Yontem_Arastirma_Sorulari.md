# Yöntem ve Araştırma Soruları: Türk LIS Dergileri OpenAlex Analizi

Bu doküman, literatürdeki "Altın Standart" çalışmaların (Alonso-Álvarez & van Eck, 2025; Céspedes vd., 2025; Doğan & Sezen, 2026) bulgularına ve metodolojilerine dayanarak, projenin yöntemini ve araştırma sorularını sempozyumun **"Sürdürülebilirlik"** temasına uygun olarak güçlendirmek amacıyla hazırlanmıştır.

---

## 1. Araştırma Soruları (Research Questions - RQs)

Sempozyumun *“Açık Bilim, Açık Veri ve Sürdürülebilir Bilgi Ekosistemi”* alt temasıyla doğrudan bağlantılı olarak projenin araştırma soruları şu şekilde güçlendirilmiştir:

*   **RQ1 (Eksiksizlik - Completeness):** Türk Kütüphanecilik ve Bilgi Bilimi (LIS) dergilerinin OpenAlex altyapısındaki temel bibliyografik (özet, kurum bağları, yazar, fon) metadata eksiksizlik oranı nedir?
*   **RQ2 (Doğruluk - Accuracy):** OpenAlex'teki yazar kurumsal kimlikleri (affiliation) ve yayın dilleri, ulusal veritabanındaki (DergiPark/TR-Dizin) gerçek verilerle (Ground Truth) karşılaştırıldığında ne düzeyde tutarlılık göstermektedir? 
    *   *Alt Soru:* Najko Jahn (2025)'ın belirttiği üzere "Walden Güncellemesi" sonrasındaki affiliation düşüşü Türk LIS verilerinde spesifik sistematik hatalara (ör. Türkçe karakter bozulmaları veya kurumsal id eşleşme hataları) yol açmış mıdır?
*   **RQ3 (Sürdürülebilirlik - Sustainability):** Ulusal bilimsel dergilerin küresel açık veri ekosistemlerindeki (OpenAlex) bu metadata kalite sorunları, yerel akademik üretimin "sürdürülebilir bilimsel iletişimine" ve dijital uzun vadeli görünürlüğüne nasıl bir engel teşkil etmektedir?

---

## 2. Araştırma Yöntemi (Methodology)

Araştırmanın tasarımı, OpenAlex verileri ile ulusal kaynak verilerini karşılaştırmalı bir değerlendirmeye dayanan **karmada (nicel ve manuel doğrulama)** bir model üzerine kurulmalıdır.

### Adım 1: Veri Toplama Evreni ve "Ground Truth"
*   **Veri Seti:** Türkiye'deki önde gelen LIS dergileri (Türk Kütüphaneciliği, Bilgi Dünyası, Bilgi Yönetimi vb.) temel çalışma kapsamı olarak belirlenir. Bu dergilerin temel metaverileri (DOI'ye sahip tüm makaleleri) DergiPark veya Crossref üzerinden çekilerek "Doğru / Temel Veri" (Ground Truth) veri seti oluşturulur.

### Adım 2: OpenAlex Veri Entegrasyonu ve Eşleştirme
*   Çekilen yayın kümesinin DOI numaraları (veya ISSN blokları) kullanılarak **OpenAlex REST API** üzerinden makalelerin aynı gruba ait OpenAlex yansımaları (`Works` endpoint) elde edilir (Mevcut `scripts/json_to_csv.py` bu adım için bir prototiptir).

### Adım 3: İki Boyutlu Ölçüm Mimarisi

**A) Eksiksizlik (Completeness) Ölçümü (Nicel Değerlendirme)**
*   Elde edilen OpenAlex verilerindeki kritik bibliyometrik alanların (Abstract, Authorships.institutions, Funder ID, vs.) boş (`null`) gelme oranları Python kütüphaneleri (Pandas) yardımıyla oransal (%) olarak analiz edilir. 
*   *Referans:* Alonso-Álvarez & van Eck (2025) "Availability of Metadata" modeli.

**B) Doğruluk (Accuracy) Ölçümü (Kalitatif / Manuel Validasyon)**
*   Tespit edilen verilerin doğruluğu, %10-20'lik rastgele (stratified) bir örneklem üzerinden manuel formalarla kontrol edilir.
*   **Odak Noktaları:**
    1.  *Dil Yanılgısı:* Türkçe yazılmış makalelerin OpenAlex algoritmaları tarafından yanlışlıkla İngilizce (`en`) etiketlenip etiketlenmediği kontrol edilir (Céspedes vd., 2025).
    2.  *Kurum Uyuşmazlığı:* "Institution display_name" alanında Türk üniversitelerinin İngilizceye çevirilirken veya Türkçe karakterlerden dolayı yaşadığı birleşme (disambiguation) hataları incelenir. 
    3.  *Yayın Türü (Document Type):* Özgün bir araştırma makalesinin ("article") OpenAlex içerisinde kitap bölümü veya editorial ("paratext") gibi yanlış atanma oranları ölçülür (Doğan & Sezen, 2026).

### Adım 4: Sentez ve Sempozyum Odaklı Tartışma
*   Sürdürülebilirlik argümanı işlenir: Açık veritabanlarında Türkiye gibi "küresel güney" (Global South) veya İngilizce dışı akademik üretim yapan ülkelerin karşılaştığı teknik asimetriler tartışılır. Metadata kalitesi tam olmayan bir yayın altyapısının uzun vadeli dijital erişim ("dijital koruma") açısından bir tehdit olduğu savunulur.
