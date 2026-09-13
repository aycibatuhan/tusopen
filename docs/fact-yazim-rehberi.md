# Fact yazım rehberi (spot kart standardı)

Bu rehber `content/facts/*.yaml` dosyalarının yazım standardını tanımlar. Amaç:
destedeki her fact, TUS SPOT profiliyle ölçülmüş **tek bilgi noktalı, hızlı
geçilebilir** bir spot karta dönüşür. Elle yazanlar ve içerik üreten yardımcı
ajanlar (AI) aynı kurallara uyar.

Kısa ölçüt: **medyan cevap ~9-15 kelime, Q3 ≤ ~15, p90 ≤ ~20; tek kartta tek
nokta.** Karşılaştırma ölçütü ve ölçüm aracı için bkz. [Dağılım hedefi](#dağılım-hedefi).

## Kart anatomisi

Anki exportunda fact kartının ön yüzü `ad`, arka yüzü `metin`'dir:

```yaml
id: biyok_vit_b12_folat_2
version: 1
status: draft
author: "ai-drafts/biyokimya-facts"
sources:
  - "Biyokimya ders kaynakları — referans olarak listelendi, metin özgün yazımdır"
ad: "B12 eksikliğini folat eksikliğinden ayırt eden idrar bulgusu?"
taksonomi:
  - [ttbt, biyokimya, biyok_vitamin_mineral, biyok_vit_suda_eriyen]
metin: "Metilmalonik asit artışı (B12'de metilmalonil-KoA dönüşümü bloke; folat eksikliğinde normal)."
# kaynak: 1._Sınıf_1.2_Biyokimya_VİTAMİNLER_2018.txt, ...
```

## `ad` (ön yüz) kuralları

- **Soru üslubu**, başlık üslubu değil: "...nedir?", "...hangi arterdir?",
  "...kaç haftadır?".
- **Kendine yeterli**: kart destede tek başına görülür; hangi bağlamda
  sorulduğu açık olmalı ("ilk tetkik?" değil "Wilson hastalığında ilk tetkik?").
- **Cevabı ele vermez**: soruda cevabın kendisi ya da ayırt edici anahtar kelime
  geçmez.
- **≤ 12 kelime** (hedef 5-9).

## `metin` (arka yüz) kuralları

- **Tek bilgi noktası**: bir sayı/eşik, bir eşleşme, bir mekanizma özeti, bir
  ölçüt. Birden çok nokta varsa ayrı kartlara bölünür (bkz. [Bölme kuralı](#bölme-kuralı)).
- **Hedef ≤ 15 kelime; mutlak üst sınır 25.**
- Liste ancak listenin kendisi bilgi noktasıysa (örn. PALM-COEIN açılımı) ve en
  fazla 4 ögeyle yazılır; daha uzun listeler bölünür ya da en kritik öge
  tutulur.
- Sayılar, eşik değerleri, dozlar, ilaç/gen/etken adları **birebir korunur**;
  çevresindeki ifade özgündür.
- Alan değerlerinde ham `<`, `>`, `&` kullanılmaz (repo kuralı); çift tırnak
  içinde tek satır.

## Bölme kuralı

- Kaynak not (slayt, ders kitabı özeti) çok noktalıysa fact **1-5 karta**
  ayrıştırılır; her kart yukarıdaki tek-nokta kuralına uyar.
- Fact tek karta iniyorsa orijinal `id` **korunur**, dosya yerinde yazılır.
- Birden çok karta iniyorsa `_<orijinal-id>_1`, `_2`, ... sonekli yeni id'ler
  kullanılır; orijinal dosya, tüm yedekler başarıyla yazılıp şemadan
  doğrulandıktan **sonra** silinir.
- Bilgi kaybı istenmez: atlanacak tek şey, tek-nokta kuralına uymayan düşük
  verimli ikincil ayrıntılardır (bunlar raporda/not defterinde listelenir).

## Değişmez alanlar ve izlenebilirlik

- `taksonomi`: `taxonomy/taxonomy.json`'daki geçerli 4 seviyeli yollarla birebir
  eşleşmeli; aynı nottan gelen kartlar aynı yolu taşır.
- `sources`: kurum/hoca adı geçmeyen genel atıf; telifli kaynaklardan metin
  alınmaz (bkz. CONTRIBUTING, own-words politikası).
- `status: draft`, `author: "ai-drafts/<ders>-facts"` (AI taslaklarında).
- **`# kaynak:` yorumu zorunludur**: kartın türetildiği extracted kaynak
  dosya adları, virgülle. Own-words denetimi bu yorum üzerinden çalışır;
  olmadığında denetim ders genelinde kabaca tarar.

## Own-words denetimi (bu rehbere özel ölçütler)

Kısa kartlarda shingle benzerliği yanıltıcı olur (sabit tıbbi terimler kaçınılmaz
eşleşir). Denetim aracı (`local/tools/check_overlap.py`) repo politikasıyla
uyumlu iki sinyal kullanır:

1. **6 kelimelik birebir pencere**: kart ile kaynak slayt arasında ardışık 6
   kelime örtüşmesi her boyutta ihlaldir — yeniden yazım gerekir.
2. **5-kelime shingle containment ≥ 0,40**: yalnızca ≥ 12 shingle'lık (≈ 16+
   kelime) kartlarda ihlal sayılır; daha kısa kartlarda değerlendirilmez.

Saf terminoloji numaralandırmalarında öge sırasını değiştirmek ya da araya bağlaç
yerleştirmek pencereyi kırar; listeyi silmek gerekmez.

## Dağılım hedefi

Deste geneli şu profili korumalı (ölçüm: `local/tools/kart_uzunluk_analizi.py`):

| | medyan | Q3 | p90 |
|---|---|---|---|
| Hedef (bizim) | 9-15 | ≤ 15 | ≤ 20 |
| TUS SPOT (ölçüt deste) | 10 | 14 | 22 |

Yeni eklenen kartlar bu profili bozuyorsa (örn. toplu medyan 20'ye çıkıyorsa)
sebep genellikle tek-nokta kuralının esnetilmesidir; bölme kuralı yeniden
uygulanır.

## Script spot kartları (**vurgu** kuralı)

Hastalık scriptleri (`content/scripts/*/*.yaml`) spot cloze kartları üretir.
Kart üreten alanlar: `tipik_hasta`, `patofizyoloji`, `anahtar_bulgular` (liste),
`patognomonik`, `ilk_tetkik`, `kesin_tani`, `ilk_tedavi`,
`klasik_komplikasyon`.

- **`**terim**` işaretlemesi**: exportta hem **bold** hem cloze hedefi olur;
  cümlenin gerisi görünür ipucu olarak kalır. Cloze söz dizimini (`{{c1::...}}`)
  elle yazma — build üretir; sen yalnız `**` işareti koyarsın.
- **Ne işaretlenir**: ilaç adları, dozlar, eşikler/sayılar, etkenler, ölçüt
  adları — yani cevabı oluşturan anahtar ögeler. Tanımlayıcı gövde metni
  işaretlenmez.
- **Gruplama**: aynı cümle/`;` bölümündeki işaretler aynı cloze indeksini paylaşır
  (üç antibiyotik tek seferde gizlenir); nokta ya da `;` yeni indeks açar.
- **Uzunluk**: her segment gövde+terim toplamı ~≤20 kelime; alan başına 2-4
  segment. Daha uzun içerik ya bölünür ya en kritik kısım korunup ayrıntı
  raporlanır (bilgi kaybı şeffaf olmalı).
- `anahtar_bulgular` liste alanı: her madde kendi kartına düşer (stem'de sıra
  numarası görünür); madde içinde `**` işaretlemesi kullanılır.
- Alan değerlerinde ham `<`, `>`, `&` yasak; `*` serbest.
- Tam ifade gizleyen "mini ders notu" kartları bu standarda uymaz.

Örnek — önce (tam ifade cloze, kabul edilmez):

```text
ilk_tedavi: 'Kültür sonrası gecikmeden ampirik tedavi: seftriakson veya
sefotaksim ve vankomisin; Listeria olasılığı olanlarda ampisilin eklenir...'
```

Sonra (gövde görünür, anahtar terimler cloze+bold):

```text
ilk_tedavi: 'Kültür sonrası gecikmeden ampirik tedavi: **seftriakson** veya
**sefotaksim** ve **vankomisin**; Listeria riskinde (50 yaş üstü, immün
baskılanma, yenidoğan) **ampisilin** eklenir. Deksametazonu **lomber
ponksiyondan hemen önce** başlanır (**10 mg**, altı saatte bir, dört gün)...'
```

## Push öncesi kontrol dizisi

```bash
tusopen validate                  # şema + taksonomi + çapraz referanslar
python3 local/tools/check_overlap.py content/facts/<yeni-dosyalar...>
python3 local/tools/kart_uzunluk_analizi.py   # dağılım hâlâ hedefte mi
tusopen export anki               # deste kurulabilmeli
```

## Alt ajan talimat şablonu

İçerik üretimini yardımcı ajana yaptırırken şu şablon kullanılır; ders adı, önek
ve kaynak dosya listesi yerine konur:

```text
TUS projesinde <ders> slaytlarından spot bilgi fact kartları üreceksin.
Çalışma dizini: /Users/batuhanayci/Documents/tus-anki
Standart: docs/fact-yazim-rehberi.md (önce oku; kurallar bağlayıcı).

## Kapsam
local/extracted/_refs/isler_<ders>.txt (her satır bir extracted txt yolu;
spot-yoğun olanları seç, hedefe ulaşınca dur). HEDEF: <alt-sınır>-<üst-sınır> kart.

## Yazım kuralları (özet — ayrıntı rehberde)
- Her kart TEK bilgi noktası: soru (`ad`, ≤12 kelime, cevabı ele vermeyen,
  kendine yeterli) + doğrudan cevap (`metin`, hedef ≤15, üst sınır 25 kelime).
- Spot tercihi: tanı eşiği, ilk/altın standart tetkik, ilk tedavi, etken-hastalık
  eşleşmesi, sayı/eşik değerleri. Jenerik anlatım kart olmaz.
- Own-words: slayt cümlesi kopyalanmaz; gerçek kendi cümlesiyle yazılır, sayılar
  ve terimler birebir korunur. Hoca/kurum adları kartlara girmez.
- Şema: `id` ASCII `^[a-z][a-z0-9_]*$` + ders öneki, `status: draft`,
  `author: "ai-drafts/<ders>-facts"`, genel `sources` atfı, `taksonomi` yolu
  local/extracted/_refs/tax_<ders>.txt kimlikleriyle birebir, dosya sonunda
  `# kaynak:` yorumu (kullanılan extracted dosya adları).

## Doğrulama
tusopen validate; check_overlap.py (yeni dosyalar); id benzersizliği + taksonomi
kimlik kontrolü scriptle.

## Rapor
Kart sayısı + id listesi, kapsanan konular, atlanan dosyalar/nedenler,
taksonomi eşleştiremeyen konular.
```

Not: birden çok fact'e bölünme gerektiren "mini not" girdileri için (eskiden
üretilmiş uzun fact'ler) ayrıca bkz. dönüşüm kuralı — `ad`/`metin` dışındaki
alanlar aynen taşınır, çoklu kartta `_<orijinal-id>_1.._n` id'leri kullanılır.
