# TUS Open

> **İsim**: TUS (Tıpta Uzmanlık Sınavı) + Open (açık kaynak) = TUS Open.
> TUS, ÖSYM'nin sınav adıdır ve burada yalnızca tarayıcı (nomsal) olarak kullanılır; proje ÖSYM ile bağlantılı değildir.

An open-source study system for the Turkish medical specialization exam
(TUS), built around a single structured content database that exports to
Anki, a case simulator, an oral-exam mode, and topic/overlap statistics.
The full build plan is [`TUS_OPEN_PROJECT_PLAN.md`](TUS_OPEN_PROJECT_PLAN.md).

## Amaç ve bağımsızlık beyanı

Bu projenin amacı **aralıklı tekrar (spaced repetition) yöntemini TUS
adaylarına tanıtmak ve yaygınlaştırmaktır**: kanıta dayalı çalışma
tekniklerinin (aralıklı tekrar, aktif hatırlama, test-tekrar döngüsü)
TUS hazırlığında ne kadar etkili olduğunu göstermek ve bu yöntemi herkesin
ücretsiz kullanabilmesini sağlamak. Yöntemin bilimsel temelleri
[docs/anki-ve-aralikli-tekrar.md](docs/anki-ve-aralikli-tekrar.md)
belgesinde, kaynak gösterilerek açıklanmıştır.

Bu proje **TUS hazırlığı sunan herhangi bir dershane, kurs ya da yayıneviyle
hiçbir bağı, anlaşması, sponsorluğu veya izni olmadan bağımsız olarak
geliştirilmektedir** ve hiçbir kazanç amacı taşımamaktadır. İçerikler bu kurumların ders kitaplarından, soru
bankalarından veya eğitim materyallerinden alınmamış, kopyalanmamış ya da
uyarlanmamıştır; tamamı bu projeye özgü yazımdır ve telif/ticari kaynaklara
atıf yalnızca bilimsel referans düzeyinde (kılavuz/ders kitabı adı) kullanılır.

**Rekabet değil, bilinçlendirme hedeflenmektedir.** Piyasada aralıklı tekrar
temelli ücretli kaynaklar da vardır; bu proje hiçbirinin alternatifi ya da
rakibi olarak konumlanmaz. Amacı, aralıklı tekrar yönteminin bilimsel
dayanağını herkese açık ve ücretsiz biçimde göstermek, yöntemi herkesin
kullanımına sunmaktır. Hangi kaynağı kullanacağınız tamamen sizin tercihiniz;
burada anlatılan yöntem mevcut çalışma düzeninizin yanında da yürür.

ÖSYM sınav soruları da depoya girmez: yalnızca soru kimlikleri, cevap anahtarları
ve konu etiketleri gibi **öğrenci kataları** kullanılır (bkz. PERMISSIONS.md).
Herhangi bir dershane/yayınevi içerik talebi gelirse (DMCA/telif bildirimi),
bildirim süreci ve kaldırma prosedürü de hazır durumdadır.

## Legal model (important)

- The repository ships **code, schemas, taxonomy, tags and own-words
  content only**, never ÖSYM question text (protected works under FSEK).
- Question text lives only in a local, never-committed cache. Users fetch
  official PDFs from osym.gov.tr themselves, or import their own AİS copy with
  `tusopen import` (full booklets are publicly downloadable for ~2006–2021;
  2022+ only a 10% sample + answer key is public).
- Content is written in own words. Some drafts were produced with AI
  assistance; items pass through named human review (`reviewed_by`) before
  being marked `published`, see CONTRIBUTING.md and plan §8.
- Licenses: code under Apache-2.0 (`LICENSE-CODE`); content (scripts, cases,
  walkthroughs, facts) under CC BY-SA 4.0 (`LICENSE-CONTENT`). Illustrations
  in `content/facts/media/` are third-party Wikimedia works under their own
  free licenses (CC0/PD/CC BY/CC BY-SA), per-image attribution lives in
  `content/facts/media/LICENSE-MANIFEST.md` and is embedded in the study
  materials. Note: the parse stage depends on PyMuPDF (AGPL-3.0); study
  content is unaffected.

## Disclaimers

- **Not affiliated with ÖSYM.** TUS, TTBT and KTBT are ÖSYM's exam and test
  names, used here nominatively to describe what this community study aid
  prepares for. This project is not endorsed by, connected to, or approved
  by ÖSYM.
- **Educational use only, not medical advice.** Content describes medical
  facts for exam study; always verify clinical decisions against current
  textbooks and guidelines before applying them to patients.
- **No warranty.** Provided "as is", without warranty of any kind; the
  authors are not liable for any damages arising from use of the materials.
- **Draft quality (v0.3.0-alpha).** ALL items are currently in `draft`
  status: AI-assisted drafts awaiting human review. Nothing here is
  reviewer-approved yet, verify facts against a textbook, and report
  errors via issues or PRs.
- ÖSYM question text never appears in this repository, question text lives
  only in a local, never-committed cache (see the licensing section above).

## Layout

```
taxonomy/taxonomy.json     topic taxonomy: ders -> konu -> alt_konu (3 levels, stable ids)
content/                   committable content (metadata stubs, own-words files)
  questions/               per-sitting question metadata (no question text)
  scripts/ cases/ walkthroughs/ facts/   authoring targets
schemas/                   JSON Schema for every content type
src/tusopen/               CLI pipeline (fetch, parse, stubs, validate)
~/.tusopen/cache/          local-only: raw PDFs + parsed question text (never committed)
```

## Desteyi indir (kullanıcılar için)

Kod yazmadan kullanmak isteyenler için:

1. [Releases](https://github.com/aycibatuhan/tusopen/releases) sayfasından
   en son `tusopen.apkg` dosyasını indirin
2. Dosyaya çift tıklayın (ya da Anki ▸ Dosya ▸ İçe Aktar)
3. Kartlar Anki'ye gelir; sonraki güncellemeler için
   [güncelleme eklentisini](addon/tusopen_guncelle/README.md) kurun
   (indirir, bildirir, zamanlamanızı korur)

İçeriği kaynak haliyle incelemek isterseniz tam bu depodasınız:
`content/` klasörü tüm kartların kaynağıdır; `site/` build çıktısıdır
(README üstündeki hızlı başlangıçla kendiniz üretebilirsiniz).

## Eklenti (otomatik güncelleme)

Anki eklentisi, desteyi GitHub Releases üzerinden otomatik günceller
(zamanlama korunur). Kurulum:

1. [Releases](https://github.com/aycibatuhan/tusopen/releases) sayfasından
   `tusopen_guncelle.ankiaddon` dosyasını indirin
2. Anki ▸ Araçlar ▸ Eklentiler ▸ **Install from file** → dosyayı seçin
3. Anki'yi yeniden başlatın, sonraki güncellemeleri eklenti bildirir

Detaylar: [addon/tusopen_guncelle/README.md](addon/tusopen_guncelle/README.md)

## Quick start

New to Anki or spaced repetition? Read
[`docs/anki-ve-aralikli-tekrar.md`](docs/anki-ve-aralikli-tekrar.md), a
beginner's guide in Turkish, with scientific references.

```bash
python3 -m venv .venv
.venv/bin/pip install -e .

.venv/bin/tusopen --help
.venv/bin/tusopen validate          # schemas + cross-refs; needs no cache
.venv/bin/tusopen fetch             # download official ÖSYM PDFs into the cache
.venv/bin/tusopen parse --all       # parse PDFs -> local JSON + content/ stubs
.venv/bin/tusopen validate --originality   # own-words check (needs local cache)
```

The cache defaults to `~/.tusopen/cache` and is never committed or shipped.
`content/questions/<yil>/<donem>/<test>.yaml` files are metadata-only stubs
(question ids, answer keys, `iptal` flags, empty tagging fields); contributors
fill taxonomy ids and illness-script links there.

## Status

- Fetch/parse pipeline: 54 sittings (2013–2026), 4,253 questions parsed locally,
  4,292 metadata stubs committed (39 ÖSYM-cancelled questions kept as `iptal`).
- Taxonomy: 31 ders (8 TTBT + 23 KTBT), 393 konu, 2,601 alt_konu, seeded with
  AI assistance, human skim pending before v1.
- Content: 327 illness scripts, 60 cases, 301 facts, all `draft` status.
- Anki deck (0.3.0-alpha): 2,134 notes / 2,703 cards; case simulator with 60
  cases; both built by `tusopen export`.
- Six JSON Schemas + schema/cross-reference validator, pytest suite, ruff and
  advisory own-words check wired into CI (`.github/workflows/validate.yml`).
- Next: human review sprint, walkthroughs + Çeldirici cards, coverage for
  zero-content ders (plan M3–M4).

## Contributing

Contributing guides are being written (plan §10, M4). Until then, every PR
should follow the own-words policy in `TUS_OPEN_PROJECT_PLAN.md` §8: write
from your understanding of the topic, never reproduce or closely paraphrase
ÖSYM stems/options or prep-company text. CI runs schema and cross-reference
validation on every PR.
