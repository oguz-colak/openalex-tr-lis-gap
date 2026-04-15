"""
update_abstract.py
Replaces the Abstract (Özet) paragraph in Symposium_Proceeding_Draft.docx
with the new content from abstract_draft.md.
"""

from docx import Document
from docx.shared import Pt
import copy

DOCX_PATH = r"c:\Users\oguzc\OneDrive\Masaüstü\Antigravity_Projeleri\Symposium-Proceeding\Symposium_Proceeding_Draft.docx"

# ── New abstract text (from abstract_draft.md) ─────────────────────────────
NEW_ABSTRACT_TR = (
    "Açık bilimsel altyapıların sürdürülebilirliği, büyük ölçüde bu altyapılarda yer alan "
    "üstverilerin (metadata) kalitesine bağlıdır. OpenAlex, 2022 yılından bu yana tescilli "
    "veri tabanlarına açık bir alternatif olarak sunulmuş ve hızla benimsenmesine karşın "
    "üstveri kalitesine ilişkin önemli sınırlılıklar rapor edilmiştir (Delgado-Quirós ve "
    "Ortega, 2024; Céspedes vd., 2025; Forchino ve Torres-Salinas, 2026). Özellikle İngilizce "
    "dışı dillerde yayın yapan ve ulusal dizin platformları kullanan ülkelerin bilimsel çıktıları, "
    "küresel sistemlerdeki üstveri eksikliklerinden orantısız biçimde etkilenmektedir "
    "(Alonso-Álvarez ve van Eck, 2025; Zhang vd., 2025; Chavarro vd., 2025). Türkiye'de Bilgi "
    "ve Belge Yönetimi (BBY) alanındaki dergilerin tamamı DergiPark altyapısı üzerinden "
    "yayınlanmakta olup bu dergilerin üstveri kalitesine ilişkin sistematik bir karşılaştırma "
    "henüz gerçekleştirilmemiştir. Bu çalışma, söz konusu boşluğu doldurmayı amaçlamaktadır. "
    "Araştırma, Türkiye'deki altı BBY dergisini kapsamaktadır: Türk Kütüphaneciliği, Bilgi "
    "Dünyası, Bilgi Yönetimi, Bilgi ve Belge Araştırmaları, Kadın/Woman 2000 ve Türk Arşivciliği. "
    "Üstveri kayıtları OpenAlex REST API (n=2.880) ve DergiPark OAI-PMH protokolü (Dublin Core, "
    "MODS, MARC formatları) aracılığıyla toplanmıştır. DergiPark verileri 'altın standart' "
    "(ground truth) olarak belirlenmiştir (Alonso-Álvarez ve van Eck, 2025). Karşılaştırma, "
    "Delgado-Quirós ve Ortega (2024) tarafından önerilen çerçeveye uygun şekilde alan düzeyinde "
    "tamlık oranı (Completeness Degree) ve doğruluk (Accuracy) boyutlarında gerçekleştirilmiştir. "
    "Değerlendirme kapsamında öz, kurum bilgisi, dil, yazar, anahtar kelime, DOI, ORCID ve yayın "
    "türü alanları analiz edilmiştir. Analiz sonucunda üç temel yapısal sorun tespit edilmiştir. "
    "Birincisi, DergiPark OAI-PMH servisinin hiçbir dışa aktarım formatında (DC, MODS, MARC) "
    "yazar kurum bilgisini (affiliation) aktarmadığı belirlenmiştir; bu durum bir format kısıtı "
    "değil, platformun eşleme (mapping) hatasıdır. İkincisi, Bilgi Dünyası dergisinin OpenAlex "
    "sisteminde üç farklı Source ID altında parçalanmış olduğu (entity resolution hatası) "
    "saptanmıştır; bu parçalanma derginin bibliyometrik profilini doğrudan olumsuz etkilemektedir. "
    "Üçüncüsü, bazı dergilerde yayıncı bilgisi hatalı eşleşmekte (örneğin Bilgi Yönetimi'nin "
    "yayıncısının Ankara Üniversitesi yerine Süleyman Demirel Üniversitesi olarak kaydedilmesi) "
    "olup bu durum köken (provenance) denetiminde sistematik bir zafiyet olduğuna işaret "
    "etmektedir. Ayrıca OpenAlex'te söz konusu altı dergiye ait kayıtların önemli bir bölümünde "
    "öz (abstract), kurum aidiyeti ve ORCID alanlarının eksik olduğu gözlemlenmiştir. Elde edilen "
    "bulgular, Türkiye'deki BBY dergilerinin hem ulusal (DergiPark) hem de küresel (OpenAlex) "
    "düzeyde üstveri kalitesi sorunları barındırdığını ortaya koymaktadır. DergiPark'ın OAI-PMH "
    "eşleme eksikliği, OpenAlex gibi aşağı yönlü (downstream) sistemlere veri kaybının ana "
    "kaynağını oluşturmaktadır. Bu yapısal zayıflıklar, FAIR ilkelerinin (Findability, "
    "Accessibility, Interoperability, Reusability) karşılanmasını tehlikeye düşürmekte ve yerel "
    "bilimsel iletişimin dijital sürdürülebilirliğini doğrudan tehdit etmektedir. Araştırma, "
    "DergiPark altyapısındaki OAI-PMH eşleme standartlarının iyileştirilmesi, ORCID ve ROR "
    "entegrasyonunun zorunlu kılınması ve OpenAlex'in yerel dizin platformlarıyla düzenli "
    "doğrulama protokollerinin geliştirilmesi yönünde öneriler sunmaktadır."
)

NEW_KEYWORDS_TR = (
    "Anahtar Kelimeler: Üstveri kalitesi, OpenAlex, DergiPark, Bilgi ve Belge Yönetimi, "
    "açık bilim, FAIR ilkeleri, bibliometrik analiz"
)

# ── Load document ───────────────────────────────────────────────────────────
doc = Document(DOCX_PATH)

# ── Find the Özet header paragraph index ────────────────────────────────────
ozet_idx = None
keywords_idx = None

for i, para in enumerate(doc.paragraphs):
    text = para.text.strip()
    if text in ("Özet", "özet", "ÖZET", "\u00d6zet"):
        ozet_idx = i
    if text.startswith("Anahtar Kelimeler"):
        keywords_idx = i

print(f"Özet paragraph index : {ozet_idx}")
print(f"Keywords paragraph index: {keywords_idx}")

if ozet_idx is None:
    raise ValueError("'Özet' başlığı DOCX'te bulunamadı!")

# ── Replace abstract body (paragraph right after 'Özet') ────────────────────
abstract_para = doc.paragraphs[ozet_idx + 1]
# Preserve formatting from the existing run if possible
if abstract_para.runs:
    # Copy formatting from first run
    base_run = abstract_para.runs[0]
    font_name = base_run.font.name
    font_size = base_run.font.size
    bold = base_run.bold
else:
    font_name = None
    font_size = None
    bold = False

# Clear existing runs
for run in abstract_para.runs:
    run.text = ""

# Set new text in first run (or add one)
if abstract_para.runs:
    abstract_para.runs[0].text = NEW_ABSTRACT_TR
else:
    run = abstract_para.add_run(NEW_ABSTRACT_TR)
    if font_name:
        run.font.name = font_name
    if font_size:
        run.font.size = font_size

print(f"Abstract paragraph updated (index {ozet_idx + 1}).")

# ── Replace Keywords line ────────────────────────────────────────────────────
if keywords_idx is not None:
    kw_para = doc.paragraphs[keywords_idx]
    for run in kw_para.runs:
        run.text = ""
    if kw_para.runs:
        kw_para.runs[0].text = NEW_KEYWORDS_TR
    else:
        kw_para.add_run(NEW_KEYWORDS_TR)
    print(f"Keywords paragraph updated (index {keywords_idx}).")
else:
    print("WARNING: Keywords paragraph not found, skipping.")

# ── Save ─────────────────────────────────────────────────────────────────────
doc.save(DOCX_PATH)
print("✅ Document saved successfully.")
