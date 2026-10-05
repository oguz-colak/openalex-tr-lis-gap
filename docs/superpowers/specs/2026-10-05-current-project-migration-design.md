# Güncel Projenin Private GitHub Reposuna Taşınması — Tasarım

## 1. Amaç

`openalex-tr-lis-gap` reposunu altı ay önceki ara çalışma durumundan çıkarıp,
mevcut `5th_GGBBYS` projesinin güncel ve yeniden üretilebilir kaynak deposu
haline getirmek.

Migration sonunda `main` dalının çalışma ağacında yalnızca güncel proje
bulunacak; eski dosyalar normal bir silme commit'i ile kaldırılacaktır. Eski
Git geçmişi korunacak ve migration öncesi commit'i ayrıca etiketlenecektir.

## 2. Kapsam

### Taşınacaklar

- Mevcut `bby-metadata-project` içindeki güncel harvester betikleri.
- DergiPark MODS, Bilgi Dünyası MARCXML ve OpenAlex ham XML/JSON veri
  snapshot'ları.
- Analiz kapsamını ve ölçüm kurallarını tanımlayan güncel plan.
- Veri kaynakları, alan eşlemeleri, eşleştirme kuralları ve sınırlılıkları
  açıklayan dokümantasyon.
- Her snapshot için kaynak/provenance bilgisi ve kayıt kapsamı.

### Taşınmayacaklar

- Zotero veya başka kaynaklardan alınmış PDF tam metinleri.
- Python `__pycache__` ve `.pyc` dosyaları.
- Geçici harvest logları ve makineye özgü çalışma çıktıları.
- API anahtarı, parola, token veya kişisel erişim bilgileri.

Ham bibliyografik XML/JSON kayıtları proje kapsamının parçası olarak
korunacaktır. Repo private olsa da telifli tam metinler depoya eklenmeyecektir.

## 3. Git stratejisi

1. Migration öncesi `main` commit'i `legacy-before-current-project` etiketiyle
   işaretlenecek.
2. Eski çalışma ağacındaki dosyalar normal bir migration commit'i ile
   kaldırılacak; history rewrite veya orphan branch kullanılmayacak.
3. Güncel proje ve dokümantasyon aynı migration commit'inde eklenecek.
4. Migration commit'i doğrulandıktan sonra private `origin/main` dalına push
   edilecek; legacy etiketi de geri dönüş noktası olarak push edilecek.

Bu yaklaşım `main` dalını güncel tutarken eski çalışmanın denetlenebilir ve
geri alınabilir kalmasını sağlar.

## 4. Hedef içerik düzeni

Mevcut proje dizin yapısı, çalışan yolları gereksiz yere değiştirmemek için
korunacaktır. Repo kökünde aşağıdaki destek dosyaları bulunacaktır:

- `README.md`: amaç, veri kapsamı, klasör yapısı ve çalıştırma akışı.
- `docs/methodology/analysis-plan.md`: güncel analiz planı.
- `docs/methodology/data-dictionary.md`: ortak 11 alanın kaynak eşlemeleri.
- `docs/reproducibility.md`: ortam, snapshot tarihi, kaynak URL'leri ve
  yeniden çalıştırma notları.
- `requirements.txt`: kullanılan Python paketleri.
- `.gitignore`: cache, log, yerel ortam ve gizli bilgileri dışarıda bırakır.

`bby-metadata-project/02_data_collection/raw_data/` altında bulunan ham
veriler kaynak türlerine göre korunacaktır. Harvester betikleri mevcut proje
konumlarında tutulacak; taşıma sırasında algoritmik analiz değişikliği
yapılmayacaktır.

## 5. Güvenlik ve provenance

- OpenAlex iletişim e-postası kod içine sabitlenmek yerine ortam değişkeninden
  okunacaktır; örnek değer dokümantasyonda gösterilmeyecektir.
- `.env` dosyaları ve credential kalıpları ignore edilecektir.
- Snapshot'ların kaynak endpoint'i, çekim zamanı, kayıt sayısı ve SHA-256
  özeti provenance dokümanında belirtilecektir.
- Push öncesinde secret-pattern taraması ve takip edilen dosya listesi
  denetlenecektir.

## 6. Doğrulama ölçütleri

Migration tamamlanmış sayılmadan önce:

1. `main` çalışma ağacında eski repo dosyaları kalmadığı doğrulanacak.
2. PDF, `.pyc`, geçici log ve gizli dosya bulunmadığı doğrulanacak.
3. Güncel ham veri dosyalarının sayısı ve boyutları kayıt altına alınacak.
4. Python dosyaları syntax kontrolünden geçirilecek.
5. README'deki yolların gerçek dosya yapısıyla uyumlu olduğu kontrol edilecek.
6. Git diff, commit içeriği ve remote branch durumu incelenecek.
7. Push sonrasında `origin/main` ve legacy etiketi tekrar doğrulanacak.

## 7. Kapsam dışı

Bu migration, analiz planında tanımlanan parse/normalize/eşleştirme/tamlık/
tutarlılık hesaplarının tamamlanmasını veya bilimsel sonuçların yeniden
hesaplanmasını kapsamaz. Bu işlemler ayrı uygulama adımlarıdır; burada amaç
mevcut güncel çalışma durumunu güvenli ve yeniden üretilebilir biçimde
versiyonlamaktır.
