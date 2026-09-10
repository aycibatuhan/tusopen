## [0.4.0-alpha] — 2026-09-10

İlk herkese açık sürüm (private repo). Deck sürümü: v0.4.0-alpha.

### Added

- GitHub issue şablonu: içerik hatası bildirim formu (.github/ISSUE_TEMPLATE/).
- v0.4.0-alpha sürüm damgası (pyproject + deck açıklaması).

### Notes

- İçerik: 688+ dosya — 336 illness script, 315 fact, 60 vaka, 9 walkthrough.
- Deck: 2,249 not / 4,556 kart, 6 not tipi (hepsi gerçek içerikli).
- Tüm içerik `draft` durumundadır; insan incelemesi ilk beta için planlanmıştır.

# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com); versions are
`MAJOR.MINOR.PATCH` with an `-alpha`/`-beta` suffix until the first
community-reviewed release.

## [0.3.6-alpha] — 2026-09-09

Gece oturumu: üç analiz raporu (dış kaynak deck kapsamı — metadüzey; TUS
frekans haritası; USMLE-TUS kapsam uyumu) + web-doğrulamalı yüksek-kazanç
içerik paketleri (üretim listesi frekans haritasındaki boşluklardan geldi).

### Added

- **Analiz raporları** (local/decks-analysis/, gitignored — dış kaynak ürün
  adları içerdiği için public ağaçta değil):
  - konu dağılımı (metadüzey) + frekans/arz karşılaştırması: en büyük
    boşluklar mikro_genel_bakteriyoloji (40 soru / 0 içerik), gc_meme (33/1),
    ped_immunoloji_alerji (31/1), gc_safra_yollari (28/1)
  - 30 konuluk TUS-USMLE kapsam tablosu + 15 konuluk üretim önceliği
- **Yeni/yükseltilmiş içerik (web-doğrulamalı, kaynaklar dosyalarda)**:
  - Meme: meme_kanseri.yaml yeniden yazım (NCCN v2.2025/ESMO 2024/ASCO 2025 —
    SLNB de-eskalasyon, T-DM1, olaparib, CDK4/6), meme_benign.yaml (yeni),
    gc_meme_yardimci.yaml (tarama: KETEM 40-69 resmî standarda düzeltildi)
  - Peptik ülser/H. pylori: peptik_ulser.yaml (yeni; ACG 2024 — 14 gün
    bismut-dörtlü birinci seçim, direnç, test-of-cure), dah_gis_hpylori_rejim.yaml
  - Zehirlenme: antidotlar.yaml (yeni; ACMT eşleştirmeleri), dah_toks_antidot_tablo.yaml,
    ped_toks_parasetamol.yaml (Rumack-Matthew + NAC)
  - Diyabet: diyabet.yaml ADA 2025 (komorbiditeye göre GLP-1 RA/SGLT2i seçimi,
    FLOW/SELECT), dah_endo_diyabet_ilac.yaml
  - Kalp yetmezliği: kalp_yetmezligi.yaml ESC 2023 (4 sütun GDMT, EF
    sınıflaması, HFmrEF/HFpEF SGLT2i), dah_cardio_gdmt.yaml
  - Astım/KOAH: astim.yaml GINA 2024 (ICS-formoterol MART her basamak),
    koah.yaml GOLD 2024 (A/B/E), gog_gina_gold.yaml
  - Safra: kolelitiazis.yaml TG18 yükseltme, akut_kolanjit.yaml (yeni),
    gc_safra_tokyo18.yaml (TG18 şiddet + drenaj zamanlaması)
  - Antikoagülasyon: antikoagulasyon.yaml (yeni; DOAC birinci, mekanik kapakta
    warfarin, 4T/HIT, BRIDGE, reversiyel ajanlar), dah_cardio_antikoag.yaml,
    kd_gf_antikoag_gebelik.yaml
  - Konjenital kalp: konjenital_kalp_hastaliklari.yaml (yeni; 17 soru bağlandı),
    ped_kard_shuntlar.yaml
- Destemiz: 2,249 not / 4,556 kart (+81 not, +212 kart tek gecede).

## [0.3.5-alpha] — 2026-09-08

### Added

- **Görsel kaplama yeniden ölçümü (12/12)**: tüm Gorsel kartlarının maskeleri
  görsellerin gerçek içeriğine göre yeniden türetildi (raster görüntüler
  overlay ile, SVG'ler kaynak XML koordinatlarından). Figürde olmayan yapı
  etiketleri kaldırıldı (hipofiz kartı gerçek 5 yapıya oturtuldu), diyafram
  açıklıkları kendi hiatalarına taşındı, brakial pleksus diyagramın gerçek
  yönünü izliyor, nefron kartları numara-legend'e bağımlı olmaktan çıkıp
  yapı bölgelerini kapsıyor. Yakılan İngilizce etiket metinleri maskelerin
  altında kalıyor.
- **Walkthroughs ilk grup: 9 adet** (dahiliye 6: endokrinoloji×3, pankreatit,
  Mallory-Weiss, düzeltilmiş sodyum; TTBT 3: cisplatin nefrotoksisitesi,
  gemsitabin sınıflaması, trastuzumab hedefli tedavi) — her biri gerçek geçmiş
  TUS sorusuna özgün-yazım akıl yürütme kılavuzu; depoya soru metni girmez
  (yalnız soru_ref). **Çeldirici kartları ilk kez üretildi: 34 kart**
  (kavram/neden-yanlış/nerede-doğru üçlüsü).
- **Özgünlük denetimi walkthroughları da yakaladı**: 6 kelimelik pencere
  paylaşan ipucu metni tespit edilip yeniden yazıldı (mecanizma çalışıyor).

## [0.3.4-alpha] — 2026-09-08

Full-corpus Turkish grammar/proofread pass (14 parallel proofreader agents
in 4 waves over all 688 content files; ~215 corrections applied centrally
with per-file YAML validation).

### Fixed

- **~215 dil/düzeltme**: kalıntı yabancı sözcükler (systolic bruit →
  sistolik üfürüm, assay → koloni testi, Succinil kolin → süksinilkolin,
  alan postrema → area postrema, kollapse → kollaps, vasopressör →
  vazopressör), referent değiştiren yazımlar (allupurinol → allopurinol,
  dapsolon → dapson, gemkitabin → gemsitabin, sitaplopram → sitalopram,
  seftriyakon → seftriakson, rombosit → trombosit, sükksinat → süksinat,
  Tetradotoksin → Tetrodotoksin, mikroktik → mikrositik, klaudikasyon),
  bozuk cümle onarımları (porfiri, sepsis mikrodolaşım, myelom silindiri,
  NEK olgunlaşmamışlık, NMŞ dantrolen cümlesi, kalp yetmezliği kısır
  döngü, transfüzyon eşiği parantezi), ek/case hataları (bel'den →
  belden, yirmiiki → yirmi iki, diaframın → diyaframın, pupayla →
  pupillayla, tipde → tipte, reflekslar → refleksler), vinyet dil
  düzeltmeleri (40 vaka satırı).
- **Anatomik adlandırma**: Küllük (fibula) → Baldır kemiği (fibula),
  Dirensiz → Mutsuz üçlü (unhappy triad), fleksürüne → fleksurası,
  polün → kutbu, posteriyor → posterior, spinothalamic → spinothalamik.
- **Yeni tıbbi yazım standardizasyonu**: üç katmanlı rotavirus kapsidi
  ifadesi, atra/pankuronyum, Hücreserbest fetal DNA (cfDNA), sensörinöral,
  antipasyon, mikroanevrizma, pannikülit.

### Changed

- 19 spoiler vinyetinden 8 tanesi kullanıcı onayıyla düzeltildi (hipotiroidi,
  urtiker, toksoplazmoz, rektum kanseri, retinoblastom, endometriozis,
  menopoz, omuz distosisi); kalan 11'i kullanıcı kararıyla teknik terim
  olarak bilinçli tutuldu (hedef kitle tıp mensupları).
- Tartışmalı 4 tıbbi iddia hakemliği tamamlandı: flail göğüs ≥3 (+ATLS ≥2
  notu), postop ateş atelektazi çerçevesi, LJ 2-8 hafta, metastatik
  kalsifikasyon (PHT + ikincil HPT notu).

## [0.3.3-alpha] — 2026-09-07

Full-corpus clinical deep-review (24 parallel read-only auditor agents in
5 waves; whole 688-file corpus verified against named current standards:
GINA/GOLD 2024, ESC 2021-2023, AHA/ACC, ACR/EULAR, IDSA/ATS/CDC, ACOG/SMFM,
AAP/ISPAD, KDIGO, AAO PPP, ATLS-10, DSM-5-TR, ICHD-3, Robbins, Gray's,
Guyton, Katzung, Murray).

### Fixed

- **patognomonik taraması tamamlandı**: 185 dolu alanın tamamı değerlendirildi;
  ~100 alan "Patognomonik değil; tanıya yardımcı tipik bulgu" ifadesiyle
  dürüstleştirildi (ölçüt: bulgu başka hastalıkta da görülüyorsa
  patognomonik değildir). Gerçekten özgül imzalar (KF halkası, Koplik,
  Philadelphia, EWS-FLI1, Orphan Annie, Trethowan vb.) korundu.
- **Yeni CRITICAL düzeltmeleri**: masif transfüzyon eşiği tersine çevrilmişti
  (KAD'de 8 g/dL; masif kanamada eşik beklenmez, MTP); fibromiyalji
  laboratuvar cümlesi kendiyle çelişiyordu; ani bebek ölümü dosyasındaki
  şablon bozukluğu onarıldı (12 satıra sızan metin temizlendi, BRUE
  düşük-riskli tanımına ≥32 hafta doğru biçimde eklendi).
- **Yeni MAJOR düzeltmeleri**: flebotomi günlük değil 1-2 haftada bir (350-500
  mL); Lyme doksisiklini her yaşta çocukta birinci seçenek; tetanoz riskli
  yara >5 yıl; yanık merkezi sevk eşiği ≥%10 (resüsitasyon %20); ACR 2020
  gut atak sırasında ULT başlatılabilir; kayalık dağ benekli ateşi adlandırma
  ("OMSK ateşi" ayrı bir hastalıktır) ve "kırlangıç tifusu" → çalı tifusu;
  klon kordu çocukta doksisiklin beklemeden; mitral stenoz ciddi darlık
  ≤1,5 cm²; ESC 2023 IE ampirik düzeni (ampisilin/amoksisilin); yeni LBBB
  tek başına STEMI eşdeğeri değil (Sgarbossa); Bell prednizon toplam 10 gün;
  MH'de ısı 5 dakikada 1-2 °C; aspirasyon pH/hacim eşiği tarihsel işaretli
  (ASA 2022); gergin pnömotoraks 5. ICS/safe triangle; Rasmussen pulmoner
  arter anevrizması olarak yeniden bağlamsalandırıldı; DKA'da K <3,3'te
  insülin bekletilir; nistagmus Guedel II evresi; ABO antijeni karbonhidrat,
  Rh protein; Aspergillus'ta β-D-glukan düşük duyarlılık; pterijin...
  (dahiliye/enfeksiyon/pediatri/gc/kd/noroloji/psikiyatri/dermatoloji/
  kardiyoloji/kbb/göğüs/göz/ortopedi/anestezi/fiz/biyok/mikro/farm tüm
  dilimlerden toplam ~120 satır düzeltmesi).
- **Anatomi 43 dosya sorunsuz çıktı** (Gray's/Moore/Netter'a karşı tam doğrulama);
  patoloji 38 dosya sorunsuz çıktı (Robbins 10 + WHO).

### Known limitations (updated)

- Denetleyicilerin "doğrulanamayan" işaretlediği ~15 iddia (kaynaklar
  arasında gerçek görüş ayrılığı olan) insan hakemliğine kaldı: flail
  göğüs ≥2/≥3 kaburga, β-talasemi minor HbA2 eşiği, perioperatif
  anafilaksi tetikleyici sıralaması (NAP6 vs Fransız verisi),
  metastatik kalsifikasyonun en sık nedeni, rotavirüs kapsid katmanı.
- 19 vaka vinyeti hastalık adını geçiyor (build uyarısı sürüyor);
  görsel kaplama koordinatları hâlâ tahmini.

## [0.3.2-alpha] — 2026-09-07

Round-3 medical-accuracy deep-dive pass (corpus now swept in full three
times; ~70 content corrections).

### Fixed

- **15 CRITICAL medical errors** (union of three independent round-3
  reviews, every one verified at source before fixing):
  - Mikrobiyoloji: Aspergillus 45° dallanma (dik açı Mucor'un işaretidir)
  - Enfeksiyon: kronik Q ateşi faz 1 IgG (faz 2 ters); tularemi kapsüllü;
    toksoplazmoz Sabin birleşimi dağınık kalsifikasyon (periventriküler
    CMV'indir); toksoplazmoz ensefalit birinci seçenek pirimetamin +
    sülfadiazin + folinik asit; mukormikoz risk faktörü deferoksamin
    (deferasirox değil); tifo kemik iliği kültürü akut dönem için
  - Kardiyoloji: hipertansif ürjans yavaş düzeltme (hızlı düşürme
    acil duruma aittir); mitral yetmezlik hiperdinamik apex + üfürüm
    şiddeti kaçak miktarını yansıtmaz; mitral stenoz sefalizasyon
    bilateral (sağ üst lob MR kaçak jetidir); IE ampirik düzeni + S.
    epidermidis protez kapak + klindamisin profilakside düşürüldü
  - Göğüs: hemoptizi %90 bronşiyal dolaşım; ampiyem dornaz alfa +
    alteplaz (MIST2); uyku apnesi AASM eşiği tutarlı; pnömotoraks
    inspiratuvar graf; üremik plörit eksüda
  - Anatomi: D3/SMA geometrisi; hipofiz adenomu kiasmayı aşağıdan basar;
    T8 açıklığı sağ frenik siniri de geçirir; CN IV çıkışı
  - Nöroloji: migren ICHD-3 eşlik belirtisi ≥1; blefarospazm kasılma ile
    açılamama; tromboliz sonrası <180/105 (permissive yalnız
    reperfüzyonsuz hastada); ALS'de edaravon
  - Kadın-doğum: preeklampsi 2+ bant proteinürisi + ağır özelliklere
    160/110 eklendi; makat tipleri frank ayrı kategori; GTN FIGO/WHO
    skoru; oligohidramnios tek ölçümle tanı; ektopik hCG >5.000 göreli
    kısıt (vaka + script)
  - Pediatri/metabolik: CPT-I hepatik (kardiyomiyopati CPT-II'de)
  - KBB: Le Fort III muayenesi sabit kafatasına karşı orta yüz hareketi;
    çocukta bilateral polipoz → kistik fibrozis; LMN bağırsak flasit
    sfinkter
  - Psikiyatri: deliryum etyolojisinde madde kesilmesi dışlanmaz;
    anoreksiyada DSM-5 BMI eşiği yok; Tourette bir yıl eşiği
  - Ortopedi/dahiliye: AVN'de bisfosfonat standart değil; Ewing
    lökositozla taklit eder; porfiri nöropatisi proksimal (asendan GBS
    kalıbı değil)
  - Behçet: ISG 1990 ve ICBD 2014 ayrı ayrı doğru aktarıldı
- **Vaka düzeltmeleri**: case-menenjit-01 ampirik düzenine vankomisin +
  deksametazon eklendi (0.3.1'de eksik kalan fix); case-ektopik-01'e
  hCG >5.000 göreli kısıtı yazıldı.
- **~40 MAJOR düzeltme**: patognomonik kötü kullanımı için 6 alanda
  "tipik bulgu" ibaresi (Virchow, Wilms kitlesi, halka lezyonlar,
  miksoma, Grey-Turner/Cullen, Aspergillus hifi); kolon kanseri taraması
  45 yaş; gergin pnömotoraks ATLS 5. ICS; takotsubo ventrikülografi;
  Apfel 4 faktör; gestasyonel diyabet 100 g OGTT ≥2 anormal; anafilaksi
  bifazik 1-72 saat; NAP6 antibiyotik birinci; CDI 125 mg; feokromositoma
  ailesellik %30-40; GINA/MART; DREAM negatif omega-3; ambliyopi 12
  yaşa yanıt; kimyasal yanık erken steroid; Reid indeksi 0,4; FAP ≥100
  polip; ductus venosus göbek veni kanı; Rathke çatısı; Wolff/Müller
  ayrımı AMH'e bağlandı; talidomid kereblon yolu; Coccidioides sferül
  istisnası; alkolik ketoasidozda glukoz düşük; lenf duktusu payı;
  ASB 12-16 hafta tek kültür; yüksek yoğunluklu statin; fibromiyalji
  laboratuvar şartı değil; HHO'da etidronat ilk basamak değil; Beers
  listesinde steroid durum-bağımlı; rozase rinofima erkek baskın;
  aort yetmezliği asemptomatik vazodilatasyon önerilmez; apandisit
  36-48 saat tutarlılığı; sanrıda tuhaf olmayan ölçüt belirteç.
- **~30 MINOR terminoloji/sayı düzeltmesi**: iletim tipi işitme kaybı
  (×3 dosya), epitimpanik, amiloidoz, ince ral, rektovajinal, takizoit,
  Negri inklüzyon cisimcikleri, Ziehl-Neelsen, otozomal dominant,
  café-au-lait, craving, pleksiform, kulak kepçesi, antemortem, kısmen
  kompanse alkaloz, 6-24 saat nötrofil, HEV 3. genotip kronikliği,
  HBV çift sarmallı, HFrEF ≤%40, inhibin-A dörtlü teste, Koch üçgeni,
  7 g/dL masif transfüzyon, Bell IIIB perforasyon, hipermatür ≠ olgun,
  SLiM CRAB, MANT/MART → MART.

### Known limitations (updated)

- Üç turda tüm derlem en az bir kez okundu; ancak tur-3 algılama
  hassasiyeti analizi 10-20 CRITICAL'in hâlâ yakalanmamış olabileceğini
  söylüyor. Sonraki en verimli işler: 185 alanlık patognomonik taraması
  ve sayısal iddia taraması; ardından insan gözden geçirmesi.
- 18 dosyada tur-3 MINOR satırı raporda kesik kalmıştı; dosya adları
  biliniyor, satır düzeyinde düzeltme gözden geçirme turuna kaldı.

## [0.3.1-alpha] — 2026-09-07

Round-2 external review pass (two independent reviews).

### Fixed

- **[CRITICAL] Simulator was dead on arrival**: the 0.2.0 licence-footer
  edit leaked Python implicit string concatenation into the JS template
  → SyntaxError killed the whole page. Fixed; the smoke test now
  parse-checks the built JS with `node --check` (substring greps can
  never catch this class of bug).
- **[CRITICAL] 11 medical content corrections** (both reviews):
  Heimlich on the unconscious choking patient → CPR/compressions;
  hipokalsiürik hiperkalemi → hiperkalsemi (FHH); ALL blast eşiği ≥%25
  (AML ≥%20); retinoblastom taraması tüm kardeş/çocuklar (cinsiyet farkı
  yok); fenitoin granülomatöz iddiası → hipoalbuminemi/üremi serbest
  fraksiyon; piyodermi → ARA değil AGN; polisitemia vera WHO 2016
  ölçütleri; kolelitiazis özeti ateş kuralı ters düzeltildi; diseksiyon
  vitalleri fiziksel olarak tutarlı hale getirildi; menenjit ampirik
  rejimine vankomisin + deksametazon eklendi; ektopik gebelikte hCG
  >5.000 göreli kısıtı belirtildi. Ayrıca: GINA ICS-formoterol
  kurtarıcı, toxo profilaksisi CD4 <100 + IgG pozitif, ISPAD 50–75
  mg/dL/saat, pemfigus vulgaris/foliaceus agresyon düzeltmesi, raşitizm
  genu varum "O harfi", RS hücresi simetrik baykuş gözü, mivakuryum
  karaciğer yetmezliğinde uzar (organ bağımsız yalnız atracurium).
- **[MAJOR] Vaka kartı arka yüzündeki anahtar bulgular tekrarı
  kaldırıldı** (ön yüzde kalmaya devam eder — vakayı cevaplanabilir
  yapan odur); hastalık adını vinyette geçiren 19 script için build
  uyarısı eklendi (73 vinyette konu adı geçiyor; yeniden yazım gözden
  geçirme turunda).
- **[MAJOR] Spot atomization tamamlandı**: noktalama işaretlerine ek
  olarak `;` üzerinde bölme — silme sayısı 2.073 → 3.704, medyan 156 →
  81 karakter, >200 karakter silme oranı %28 → %3,5. Not GUID'leri
  sabit (yeniden içe aktarımda planlama korunur).
- **[MAJOR] Validator artık şema-geçersiz dosyada çökmüyor** (round-1
  bulgusu): şema hatası olan dosyanın çapraz referansları atlanır,
  hatalar raporlanır. `case.hastalik` artık illness script id'lerine
  karşı denetleniyor.
- **[MAJOR] review --apply sertleştirildi**: içerik kökü dışına yazım
  engellendi (resolve + is_relative_to + .yaml), reviewed/published
  için reviewer zorunlu, geçersiz status uyarılı atlama,
  last_reviewed yenilemede güncellenir, utf-8-sig (Excel uyumlu),
  safe_dump width=100 (40 satırlık diff yerine okunabilir).
- **[MAJOR] --originality önbellek yokken "OK" basmıyor**: SKIPPED
  ayrı satırda, kod 0 ama PASS iddiası yok; docstring 0.40 ile
  mutabık.
- **[MAJOR] Türkçe İ normalizasyonu**: "İ".lower() → i + U+0307
  bütün dizinleri bozuyordu; İ→i, I→ı map eklendi (denetim testi ile).
- **[MAJOR] README güncellendi**: 0.3.0-alpha, 31 ders / 2.601
  alt_konu, "community-reviewed" iddiası kaldırıldı (hiçbir öğe henüz
  incelenmedi), garantisi/sorumluluğu TR+EN metin, medya karvesi,
  PyMuPDF AGPL notu.
- **[MAJOR] 24 yazım düzeltmesi** (porfobilinojen, Kingella kingae,
  intussusceptum/suscipiens, plazmaferez, granülozus, peteşik-purpurik,
  oftalmopleji, berrak hücreli, Deprescribing, psödokolinesteraz...).
- Taksonomi yeni derslerde bozuk etiketler düzeltildi (TUGA → İdrar
  Akım Ölçümü, Repasyon → Reparasyon, Olurlar Sorgusu → Adli
  Değerlendirme); ayirici bloğu olmayan 2 dosyada `kart_uret.ayirici`
  false'a çekildi.
- Simülatör: soru adımlarında "Önceki bulgular" etiketi; geri bildirim
  kapsayıcısına odak (ekran okuyucu düzgün duyurur); adım geçişte
  scroll reset; tamamlama yalnızca ≥1 soru yanıtlanmışsa işaretlenir.

### Known limitations (updated)

- 73 vaka vinyeti konu adını geçiyor; tanıyı elle gizleyen yeniden
  yazım gözden geçirme turunun işi (uyarı build'de basılıyor).
- Görsel kaplama koordinatları hâlâ tahmini; render edilmiş görseller
  üzerinde yeniden ölçüm gerekli.
- Yeni 5 ders henüz 0 içerik/0 etiket taşıyor; eski düğümlerdeki
  ilgili soruların yeniden etiketlenmesi bekliyor.

## [0.3.0-alpha] — 2026-09-07

### Added

- **5 missing official subjects in the taxonomy** (cards to follow later):
  - KTBT: Üroloji, Beyin ve Sinir Cerrahisi, Plastik Cerrahi, Adli Tıp
  - TTBT: Tıbbi Biyoloji ve Genetik
  - Tree grows 26 → 31 ders, 371 → 393 konu, 2,532 → 2,601 alt_konu; new
  ders appended at the end of each test's list so existing positional
  tree_ids are unchanged. All existing tags resolve.
- **Spot atomization**: multi-sentence Spot values are now split into
  per-sentence cloze deletions (capped at 5 per card, short sentences
  merged); single-sentence values stay one deletion. Deck: 2,194 → 2,703
  cards on the same 2,134 notes — each card now tests exactly one fact.
  Note GUIDs unchanged, so re-imports preserve scheduling.
- **Test suite**: 23 pytest tests (taxonomy integrity, validator smoke,
  Anki builder unit tests, review round-trip, originality detection
  including the one-word-substitution case, simulator smoke) plus ruff
  lint in CI (`pip install -e ".[dev]"`).
- **Strengthened own-words check** (plan §8.2): 6-word window (was 8),
  5-word shingle containment ≥ 0.40 (paraphrase-resistant), fuzzy ≥ 0.6
  vs *individual* stems/options instead of the whole question (fixes the
  length-dilution that hid short copies). Lab-value windows and short
  medical nomenclature are excluded to kill false positives. A missing
  local cache is reported and skipped (CI-advisory), not a crash.
- **CI**: ruff + pytest on every push/PR; `tusopen validate
  --originality` runs as an explicit advisory step.

### Known limitations (updated)

- PyMuPDF is AGPL-3.0; the parse stage imports it. Content produced by
  the pipeline is unaffected, but distributors of the *code* should note
  the AGPL for that dependency (or swap the parser to pypdfium2, a
  BSD/Apache-licensed alternative, for a fully permissive chain).

## [0.2.0-alpha] — 2026-09-07

Friend-review readiness release.

### Added

- **Deck versioning**: every build stamps `DECK_VERSION` into the deck
  description (currently 0.2.0-alpha); the build output reports it. Deck
  name stays fixed ("TUS Open") so re-imports never fork scheduling.
- **`tusopen review`** — human review workflow for named reviewers:
  `tusopen review --dump [DERS]` writes a CSV worksheet of all content
  items (scripts/facts/cases) with `reviewer` + `status` columns;
  `tusopen review --apply sheet.csv` merges them back into the YAML
  (`reviewed_by`, `last_reviewed`, idempotent).
- **Sentence-level line breaks** across cards: Anki fields (Vaka vignette
  bulleted, Spot/Bilgi answers, açıklamalar) and simulator vignettes now
  break per sentence — long clinical prose reads as paragraphs, not walls.

### Changed

- `docs/deck-landscape-gap-analysis.md` moved out of the public tree into
  the gitignored `local/` area (names third-party commercial products).

## [0.1.1-alpha] — 2026-09-07

External review pass (two independent multi-agent reviews) followed by fixes.

### Fixed

- **Medical content corrections** (6 critical, verified at source):
  - subaraknoid kanama: okulomotor felç tanımı düzeltildi (içebakış kısıtlı,
    göz aşağı-dışa dönük; dışa bakamama VI. sinirdir)
  - Kawasaki: tam tanı kriteri "ateş + beş kriterden en az dördü" olarak
    düzeltildi; 2–3 kriter = eksik Kawasaki
  - Sıtma: "içme suyu kaynaklı bulaş" ifadesi kaldırıldı (bulaş yalnızca
    anofel ısırığıyla; yerel/otohton bulaş olarak yeniden yazıldı)
  - Siroz vakası: "İnteröz transhepatik şant" → "Transjugüler intrahepatik
    portosistemik şant (TIPS)"; SBP eşiği lökosit değil PMN ≥250/mm³ olarak
    düzeltildi
  - Siroz vakası: "sabah başağrısı" ensefalopati bulgusu olmaktan çıkarıldı
    (uyku düzeni bozukluğu + gündüz uyku hali korundu)
  - Biyokimya: "arginin nitrik oksit ile kreatinin kaynağıdır" → arginin NO
    öncüsü + glisinle kreatin sentezi (kreatin ≠ kreatinin ayrımı)
- **Yazım düzeltmeleri** (15 adet): sakubitril, Todd paralizisi,
  levetirasetam, konvülsiyon, eksizyon, psödokolinesteraz, küçük dil,
  Kıvrım diüretikleri.
- **Gorsel (görsel kapama) reveal düzeltmesi**: kapatma kutusunda açıklanan
  cevap artık görünür (`.io-mask .cloze{color:#fff}`).
- **Görsel atıfları desteye gömüldü**: her Gorsel kartında yazar · lisans ·
  kaynak görüntülenir; deste açıklamasına lisans + tıbbi uyarı + ÖSYM
  bağlantısızlık bildirimi eklendi.
- **Vaka kartı kendi cevabını ön yüzde iki kez veriyordu**: anahtar bulgular
  ön yüzden çıkarıldı, arka yüze açıklayıcı katman olarak taşındı;
  `aciklama` alanı patofizyoloji ile dolduruldu (327/327).
- **Sıklık rozeti payı**: "Son 20 sınavda N kez" → "N sınavda soruldu"
  (arşiv 27 oturum içeriyor; yanlış pay beyanı kaldırıldı).
- **tree_id çakışmaları giderildi**: kart sıra sayacı artık tüm derlemde
  alt_konu bazında global; 2,134 kartta 0 çakışma (öncesinde 17 kopya).
  Build sırasında çakışma denetimi uyarı basar.
- **Sıralama alanı okunabilir hale getirildi**: tarayıcı sıralaması artık
  id bilgisinin değil soru/vinyet/metin alanının üzerinden çalışır.
- **Simülatör**: soru adımında sunum ve ara sonuçlar ekranda kalır (31 soru
  bağlamı olmadan cevaplanamaz durumdaydı); geri bildirim `aria-live`
  bölgesi ile ekran okuyucuya duyurulur; sözlü mod artık vakayı tamamlanmış
  işaretlemez ve "Cevabı Göster" vakanın özetini model cevap çerçevesi
  olarak gösterir; seçenek/kontrast oranları iyileştirildi.
- Çeldirici not tipi artık ortak alanları (id, kaynak, versiyon) doldurur.

### Known limitations (updated)

- Spot cloze kartlarında bazı cevaplar paragraf uzunluğunda; atomik boşluklara
  bölme planlandı (0.2.0).
- Görsel kapama koordinatları elle tahminidir; görseller üzerinde yeniden
  ölçüm gerektirir.
- Walkthroughs ve Çeldirici içeriği henüz yok; istatistik modülü plan M4'te.
- `tusopen validate --originality` yalnızca yerel ÖSYM korpusu olan
  makinede çalışır; CI'da koşullu/advisory hale getirilecek.
## [0.1.0-alpha] — 2026-09-07

First public milestone: the full content pipeline, first content corpus, and
the tagged question archive. All content is `draft` status pending community
review.

### Added

- **Fetch/parse pipeline** (`tusopen fetch | import | parse`): official ÖSYM
  booklet download from `sources.yaml` (54 sittings, 2013–2026), local-only
  cache, PyMuPDF-based parsing with Turkish normalization, A/B variants,
  cancelled-question handling, and metadata stub generation.
- **Topic taxonomy** (`taxonomy/taxonomy.json`): 26 ders (7 TTBT + 19 KTBT),
  371 konu, 2,532 alt konu with stable lowercase ids. AI-seeded; human review
  pending.
- **Six JSON Schemas** (`schemas/`) and a three-layer validator
  (`tusopen validate`): schema validation, cross-reference checks (taxonomy
  paths, illness-script links, question refs, duplicate ids, reviewer rules),
  and the own-words originality check (8-word window + fuzzy 0.6, plan §8.2).
- **Content corpus** (all `status: draft`):
  - 327 illness scripts across 16 ders
  - 60 scripted cases with `sozlu_sorular`
  - 301 fact cards covering all 7 TTBT ders (30 KTBT gap-topic facts included)
- **Case simulator** (`tusopen export simulator`): self-contained SPA at
  `site/simulator/index.html` — 60 cases, step-through branching, oral exam
  mode with model-answer summary, progress in localStorage.
- **Anki exporter** (`tusopen export anki`): single deck, 2,134 notes with
  stable GUIDs derived from content ids, 6 note types (Bilgi, Vaka, Ayırıcı,
  Çeldirici, Spot cloze, Gorsel image-occlusion), data-stamped tag hierarchy,
  numeric tree IDs (`TUS_v1::ID::`), and `siklik` badges. Card layout:
  short answer first, then a separated explanation layer (fact cards are
  auto-split at the first sentence); night-mode aware styling for both light
  and dark Anki themes.
- **Question tagging pipeline** (`tusopen tag`): worksheet dump, merge with
  human-value precedence, taxonomy validation at merge time, and script
  backfill. **4,253/4,292 questions tagged (100% of active questions across
  all 54 exams)**, including 1,097 question→illness-script links and real
  first frequency data (top all-time topics: fırsatçı mikozlar, herpesvirüsler,
  antiprotozoal ilaçlar, meme karsinomu).
- **Docs**: beginner's guide to Anki and spaced repetition in Turkish with
  verified scientific references (`docs/anki-ve-aralikli-tekrar.md`);
  CONTRIBUTING.md, CHANGELOG.md, PERMISSIONS.md, and README disclaimers.
- **CI** (`.github/workflows/validate.yml`): schema + cross-reference
  validation on every push/PR.
- **Licenses decided**: Apache-2.0 (code), CC BY-SA 4.0 (content).

### Known limitations

- Content is AI-assisted draft quality; community review is the active gate
  (707 files in the review backlog).
- Taxonomy needs a human skim before v1.
- Walkthroughs, Çeldirici cards, case simulator, oral-exam mode, statistics,
  and mock-exam mode are not yet built (plan M3–M5).
- ÖSYM question text is never stored in the repository; it lives only in the
  local cache (`~/.tusopen/cache`), which is never committed or distributed.

