# Abstract Draft — IMRAD Structure

## Türkiye'deki Bilgi ve Belge Yönetimi Dergilerinin Üstveri Kalitesi: OpenAlex ve DergiPark Karşılaştırmalı Analizi

**Metadata Quality of Library and Information Science Journals in Turkey: A Comparative Analysis of OpenAlex and DergiPark**

---

### Öz

**Giriş (Introduction):** Açık bilimsel altyapıların sürdürülebilirliği, büyük ölçüde bu altyapılarda yer alan üstverilerin (metadata) kalitesine bağlıdır. OpenAlex, 2022 yılından bu yana tescilli veri tabanlarına açık bir alternatif olarak sunulmuş ve hızla benimsenmesine karşın üstveri kalitesine ilişkin önemli sınırlılıklar rapor edilmiştir (Delgado-Quirós ve Ortega, 2024; Céspedes vd., 2025; Forchino ve Torres-Salinas, 2026). Özellikle İngilizce dışı dillerde yayın yapan ve ulusal dizin platformları kullanan ülkelerin bilimsel çıktıları, küresel sistemlerdeki üstveri eksikliklerinden orantısız biçimde etkilenmektedir (Alonso-Álvarez ve van Eck, 2025; Zhang vd., 2025; Chavarro vd., 2025). Türkiye'de Bilgi ve Belge Yönetimi (BBY) alanındaki dergilerin tamamı DergiPark altyapısı üzerinden yayınlanmakta olup bu dergilerin üstveri kalitesine ilişkin sistematik bir karşılaştırma henüz gerçekleştirilmemiştir. Bu çalışma, söz konusu boşluğu doldurmayı amaçlamaktadır.

**Yöntem (Method):** Araştırma, Türkiye'deki altı BBY dergisini kapsamaktadır: Türk Kütüphaneciliği, Bilgi Dünyası, Bilgi Yönetimi, Bilgi ve Belge Araştırmaları, Kadın/Woman 2000 ve Türk Arşivciliği. Üstveri kayıtları OpenAlex REST API (n=2.880) ve DergiPark OAI-PMH protokolü (Dublin Core, MODS, MARC formatları) aracılığıyla toplanmıştır. DergiPark verileri "altın standart" (ground truth) olarak belirlenmiştir (Alonso-Álvarez ve van Eck, 2025). Karşılaştırma, Delgado-Quirós ve Ortega (2024) tarafından önerilen çerçeveye uygun şekilde alan düzeyinde tamlık oranı (Completeness Degree) ve doğruluk (Accuracy) boyutlarında gerçekleştirilmiştir. Değerlendirme kapsamında öz, kurum bilgisi, dil, yazar, anahtar kelime, DOI, ORCID ve yayın türü alanları analiz edilmiştir.

**Bulgular (Results):** Analiz sonucunda üç temel yapısal sorun tespit edilmiştir. Birincisi, DergiPark OAI-PMH servisinin hiçbir dışa aktarım formatında (DC, MODS, MARC) yazar kurum bilgisini (affiliation) aktarmadığı belirlenmiştir; bu durum bir format kısıtı değil, platformun eşleme (mapping) hatasıdır. İkincisi, Bilgi Dünyası dergisinin OpenAlex sisteminde üç farklı Source ID altında parçalanmış olduğu (entity resolution hatası) saptanmıştır; bu parçalanma derginin bibliyometrik profilini doğrudan olumsuz etkilemektedir. Üçüncüsü, bazı dergilerde yayıncı bilgisi hatalı eşleşmekte (örneğin Bilgi Yönetimi'nin yayıncısının Ankara Üniversitesi yerine Süleyman Demirel Üniversitesi olarak kaydedilmesi) olup bu durum köken (provenance) denetiminde sistematik bir zafiyet olduğuna işaret etmektedir. Ayrıca OpenAlex'te yukarıdaki altı dergiye ait kayıtların önemli bir bölümünde öz (abstract), kurum aidiyeti ve ORCID alanlarının eksik olduğu gözlemlenmiştir.

**Tartışma ve Sonuç (Discussion):** Elde edilen bulgular, Türkiye'deki BBY dergilerinin hem ulusal (DergiPark) hem de küresel (OpenAlex) düzeyde üstveri kalitesi sorunları barındırdığını ortaya koymaktadır. DergiPark'ın OAI-PMH eşleme eksikliği, OpenAlex gibi aşağı yönlü (downstream) sistemlere veri kaybının ana kaynağını oluşturmaktadır. Bu yapısal zayıflıklar, FAIR ilkelerinin (Findability, Accessibility, Interoperability, Reusability) karşılanmasını tehlikeye düşürmekte ve yerel bilimsel iletişimin dijital sürdürülebilirliğini doğrudan tehdit etmektedir. Araştırma, DergiPark altyapısındaki OAI-PMH eşleme standartlarının iyileştirilmesi, ORCID ve ROR entegrasyonunun zorunlu kılınması ve OpenAlex'in yerel dizin platformlarıyla düzenli doğrulama protokollerinin geliştirilmesi yönünde öneriler sunmaktadır.

**Anahtar Kelimeler:** Üstveri kalitesi, OpenAlex, DergiPark, Bilgi ve Belge Yönetimi, açık bilim, FAIR ilkeleri, bibliometrik analiz

**Keywords:** Metadata quality, OpenAlex, DergiPark, Library and Information Science, open science, FAIR principles, bibliometric analysis
