# TUS Open'a Katkı Sağlama

Katkıyı düşündüğün için teşekkürler. Bu proje, baştan kabul edilen iki kural
üzerine çalışır: **özgün sözler** ve **insan incelemesi**. Geri kalan her şey
teknik detaydır.

## Kısa özet

1. Fork / branch → YAML yaz → `tusopen validate` → PR
2. Her PR, aşağıdaki own-words onayını içerir
3. CI şema + çapraz referans denetimi çalıştırır; yeşil kalmalı
4. Bir insan gözden geçiren (yazar değil) `draft → reviewed` çevirisi yapar;
   yalnızca `published` öğeler dağıtılır

## Neye katkı yapabilirsin

| Tür | Konum | Şema |
|---|---|---|
| Hastalık scripti (her hastalık için bir) | `content/scripts/<ders>/<id>.yaml` | `schemas/illness_script.schema.json` |
| Senaryolu vaka | `content/cases/` | `schemas/case.schema.json` |
| Bilgi kartı | `content/facts/` | `schemas/fact.schema.json` |
| Walkthrough (gerçek geçmiş soruya akıl yürütme) | `content/walkthroughs/` | `schemas/walkthrough.schema.json` |
| Soru etiketleri | `content/questions/...` stubs | `schemas/question.schema.json` |
| Kod, şema, doküman | `src/`, `schemas/`, `docs/` |, |

## Own-words politikası (bağlayıcı, plan §8)

Dağıtılan her öğe, tıbbi gerçeklerin **senin özgün ifadenle** yazılmış olmak
zorundadır. ÖSYM'nin ifadesi (soru sapları, seçenekler, vinyetler) asla
aynen kopyalanmaz, yakın parafraz edilmez ya da yeniden kurulmaz. Somut
olarak:

1. Konuyu sorudan değil, kendi bilginden yaz. Yazmadan önce kitapçığı kapat.
2. Gerçekler özgür; ifadeler değil. "Wilson'da ilk tetkik seruloplazmin" bir
   gerçektir, ÖSYM'nin bunu soran cümlesi kopyalanacak metin değildir.
3. `content/` içinde hiçbir yerde aynen soru sapı, seçenek veya vinyet
   bulunmaz. Walkthrough'lar soruya yalnızca kimlikle atıf yapar ve akıl
   yürütmeyi anlatır, metni asla aktarmaz.
4. "Hafif" parafraz yok. Metnin orijinalle cümle cümle hizalanabiliyorsa,
   gerçekten yeniden yaz.
5. Vaka vinyetleri icattır: farklı hasta, farklı kurgu; paylaşılan tek şey
   klinik mantıktır.
6. Çeldirici kartlar yanlış seçeneğin *arkasındaki kavramı* anlatır, seçenek
   metnini değil.
7. Dershane/yayınevi kitapları ve notları da teliflidir; aynı kurallar geçerli.
8. Kaynakları atıf olarak listele; kopyalanacak metin olarak değil.

**AI desteği taslak yardımcısı olarak serbesttir**, ancak kayıtlı yazar sensin:
göndermeden önce her satırı tıbbi doğruluk ve özgünlük açısından gözden geçir,
`author` alanını dürüstçe doldur. Her öğenin yine senden başka bir insan
gözden geçirene ihtiyacı vardır.

**Denetim mekanizması**: her PR'da CI, içerikleri yerel ÖSYM arşiviyle karşılaştıran
özgünlük denetimi (6 kelimelik pencere + shingle + fuzzy katmanları) çalıştırır;
politika ihlali şüphesi build'i düşürür ve düzeltilmeden birleştirilmez. İhlal
saptanan öğe, bir sonraki yama sürümünde ya yeniden yazılır ya da
`status: deprecated` olur (not kimlikleri korunur, kullanıcıların zamanlaması
bozulmaz).

## PR onayı (PR açıklamasında zorunlu)

> Bu içeriğin kendi sözlerimle yazıldığını (AI destekli ise satır satır
> incelediğimi) onaylıyorum; ÖSYM kitapçıklarından, dershane/yayınevi
> kitaplarından ya da başka telifli kaynaklardan metin içermediğini; kaynakların
> yalnızca atıf olarak listelendiğini bildiririm.

## İçerik kuralları

- İçerik değerleri Türkçe; kimlikler ve şema anahtarları küçük ASCII
  (`^[a-z][a-z0-9_]*$`), Türkçe harfler çevrilerek (ş→s, ğ→g, ü→u, ö→o, ç→c,
  ı→i).
- Kimlikler kalıcıdır: yeniden adlandırma `ad`'i değiştirir, `id`'yi asla. Genel
  toplama düğümleri yok (`diger`, `genel`).
- Her hastalık için bir script; birincil klinik ders klasörüne konur; diğer
  konumlar `taksonomi` yolları olarak yazılır.
- Alan değerlerinde ham `<`, `>`, `&` karakteri kullanma; yazı ile yaz.
- Stil/derinlik ölçüsü: script için `content/scripts/dahiliye/wilson.yaml`,
  vaka için `content/cases/case-wilson-01.yaml`.
- Fact (spot kart) yazımı: `docs/fact-yazim-rehberi.md` standardı bağlayıcıdır —
  her kart tek bilgi noktası, soru-cevap formu, cevap hedefi ≤15 kelime
  (üst sınır 25); ayrıntı için bkz. rehber.

## Push öncesi yerel kontroller

```bash
pip install -e .
tusopen validate                  # şemalar + çapraz referanslar
tusopen validate --originality    # own-words denetimi (yerel parsed cache ister)
tusopen export anki               # deste hâlâ kurulabilmeli
```

CI her PR'da aynı doğrulamayı çalıştırır; yeşil kalmalı.

## İnceleme ve durum yaşam döngüsü

```
draft ──(inceleyen)──> reviewed ──(sürüm sorumlusu)──> published
```

- İnceleyenler: en az bir asistan/daha üst sınıf öğrenci, **yazar olmayan** biri;
  hem tıbbi doğruluğu hem özgünlüğü teyit eder.
- Kimlikler asla silinmez: kaldırılan öğeler `notlar` alanına gerekçeyle
  `status: deprecated` alır.

## Soru etiketleme

Soru stub'ları yalnızca meta veridir (kimlikler, cevap anahtarları, etiketler;
soru metni yok). Etiketleme akışı: `tusopen tag --dump <exam>` →
`taxonomy/taxonomy.json`'dan `ders/konu/alt_konu` doldur (AI destekli etiketleme
serbest) → `tusopen tag --apply <exam>`. Etiketler taslaktır ve her şey gibi
incelemeden geçer.

## Lisanslama

Katkı yaparak, katkının depo lisanslarıyla lisanslandığını kabul etmiş olursun:
kod için Apache-2.0, içerik için CC BY-SA 4.0. Commit'lerine
`Signed-off-by: Adın <e-posta>` (DCO) eklemen memnuniyetle karşılanır.

---

# Contributing to TUS Open (English)

Thanks for considering a contribution. This project runs on two rules everyone
accepts up front: **own words** and **human review**. Everything else is
mechanics.

## TL;DR

1. Fork / branch → write YAML → `tusopen validate` → PR
2. Every PR includes the own-words affirmation (below)
3. CI runs schema + cross-reference validation; it must stay green
4. A human reviewer (not the author) flips `draft → reviewed`; releases ship
   only `published`

## What you can contribute

| Type | Where | Schema |
|---|---|---|
| Illness script (one per condition) | `content/scripts/<ders>/<id>.yaml` | `schemas/illness_script.schema.json` |
| Scripted case | `content/cases/` | `schemas/case.schema.json` |
| Fact card | `content/facts/` | `schemas/fact.schema.json` |
| Walkthrough (reasoning on a real past question) | `content/walkthroughs/` | `schemas/walkthrough.schema.json` |
| Question tags | `content/questions/...` stubs | `schemas/question.schema.json` |
| Code, schemas, docs | `src/`, `schemas/`, `docs/` |, |

## The own-words policy (binding, plan §8)

Every shipped item must be **your original expression of medical facts**.
ÖSYM's expression (stems, options, vignettes) is never reproduced, closely
paraphrased, or reconstructed. Concretely:

1. Write from your understanding of the topic, not from the question. Close
   the booklet before writing.
2. Facts are free; wording is not. "Wilson'da ilk tetkik seruloplazmin" is a
   fact; ÖSYM's sentence asking it is not yours to copy.
3. No verbatim stems, options, or vignettes anywhere in `content/`.
   Walkthroughs refer to questions by id and describe the *reasoning*, never
   the text.
4. No "light" paraphrase. If your text could be aligned sentence-by-sentence
   with an original, rewrite from the fact.
5. Case vignettes are invented: different patient, different framing; only the
   clinical logic is shared.
6. Distractor cards describe the *concept* behind a wrong option, never the
   option text.
7. Prep-company books and notes are copyrighted too; the same rules apply.
8. Cite sources as references, not as text to reproduce.

**AI assistance is allowed as a drafting aid**, but you are the author of
record: review every line for medical accuracy and originality before
submitting, and set the `author` field honestly. Every item still needs a
human reviewer who is not you.

**Enforcement**: every PR runs the originality check (6-word window + shingle
+ fuzzy layers against the local exam archive); a suspected policy violation
fails the build and cannot be merged until fixed. An item found to reproduce
protected text is rewritten or marked `status: deprecated` in the next patch
release (note IDs are preserved so users keep their review history).

## PR affirmation (required in the PR description)

> I affirm this content is written in my own words (or reviewed line-by-line
> where AI-assisted); it contains no text from ÖSYM booklets, prep books, or
> other copyrighted sources; sources are listed as references only.

## Content conventions

- Content values in Turkish; ids and schema keys lowercase ASCII
  (`^[a-z][a-z0-9_]*$`), transliterating Turkish letters (ş→s, ğ→g, ü→u,
  ö→o, ç→c, ı→i).
- ids are permanent: renames change `ad`, never `id`. No catch-all nodes
  (`diger`, `genel`).
- One illness script per condition, filed in the primary clinical ders
  directory; other homes are `taksonomi` paths.
- No raw `<`, `>`, `&` characters in field values; write them out in words.
- Match the style/depth of `content/scripts/dahiliye/wilson.yaml` (scripts) or
  `content/cases/case-wilson-01.yaml` (cases).
- Fact (spot card) authoring: the standard in `docs/fact-yazim-rehberi.md` is
  binding — one information point per card, question/answer form, target answer
  ≤15 words (hard cap 25); see the guide for details.

## Local checks before pushing

```bash
pip install -e .
tusopen validate                  # schemas + cross-references
tusopen validate --originality    # own-words check (needs local parsed cache)
tusopen export anki               # deck must still build
```

CI runs the same validation on every PR; it must stay green.

## Review and status lifecycle

```
draft ──(reviewer)──> reviewed ──(maintainer)──> published
```

- Reviewers: at least one resident or later-year student, **distinct from the
  author**, confirming both medical accuracy and originality.
- ids are never deleted: deprecated items get `status: deprecated` with a
  reason in `notlar`.

## Question tagging

Question stubs are metadata-only (ids, answer keys, tags; no question text).
Workflow: `tusopen tag --dump <exam>` → fill `ders/konu/alt_konu` from
`taxonomy/taxonomy.json` (AI-assisted tagging is welcome) →
`tusopen tag --apply <exam>`. Tags are drafts and reviewed like everything
else.

## Licensing

By contributing you agree your contribution is licensed under the repo
licenses: Apache-2.0 for code, CC BY-SA 4.0 for content. Adding
`Signed-off-by: Your Name <email>` to your commits (DCO) is appreciated.