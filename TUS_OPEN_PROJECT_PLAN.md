# TUS Open — Project Plan

An open-source, community-reviewed study system for the Turkish medical specialization exam (TUS), built around a single structured content database that exports to Anki, a case simulator, an oral-exam mode, and topic/overlap statistics.

This document is a build plan. Sections marked **OPEN** are decisions deliberately left for later; they should be surfaced to the project owner, not silently resolved.

---

## 1. Goals and non-goals

### Goals
- One canonical, structured, versioned representation of TUS content: past questions (by reference), illness scripts, scripted cases, and reasoning walkthroughs.
- A hierarchical topic taxonomy (ders → konu → alt konu) applied consistently to everything.
- Deterministic exporters: Anki deck (primary), static case simulator, oral-exam mode, mixed practice sets, statistics.
- Legally clean redistribution: the repo ships code, schema, taxonomy, tags, and human-authored content; it does **not** redistribute ÖSYM question text. Users fetch official PDFs locally.
- Contributor workflow with mandatory human review before anything ships in a release.

### Non-goals (for now)
- No LLM-generated content in the shipped dataset. LLMs may be used by contributors as drafting aids, but every shipped item is human-authored or human-reviewed and marked as such.
- No hosted service, accounts, or backend. Everything runs locally or as static files.
- No commercial question banks. Only ÖSYM questions are referenced.
- No school-specific lecture material in the public repo (see §11 for the local extension model).

---

## 2. Facts about TUS the system must encode

- Run by ÖSYM, twice a year (İlkbahar ~March, Sonbahar ~August).
- Two tests per sitting: Temel Tıp Bilimleri Testi (TTBT) and Klinik Tıp Bilimleri Testi (KTBT).
- Current format: 100 questions per test, 135 minutes each. Older sittings had 120 per test; the parser must handle both.
- Scoring: correct − (wrong / 4), then standardized (mean 50, SD 10) per test. Simulator must reproduce raw net scoring; standardized score is an estimate only.
- Temel branches: Anatomi, Fizyoloji, Tıbbi Biyokimya, Tıbbi Mikrobiyoloji, Tıbbi Patoloji, Histoloji ve Embriyoloji, Tıbbi Farmakoloji.
- Klinik branches: Dahiliye, Pediatri, Genel Cerrahi, Kadın Hastalıkları ve Doğum, Küçük Stajlar (Ortopedi, Göğüs Hastalıkları, Radyoloji, Deri ve Zührevi, Nöroloji, Psikiyatri, Göz, KBB, FTR). Some schemes also break out Halk Sağlığı, Anesteziyoloji, Nükleer Tıp, Aile Hekimliği, Enfeksiyon, Kardiyoloji. **OPEN:** decide whether these are their own ders nodes or alt konu under a parent.
- Availability of official question text (verified Sept 2026):
  - **~2006–2021:** full booklets and answer keys are public on osym.gov.tr under "Geçmiş Yıllardaki Sorular → TUS Çıkmış Sorular". Released in batches (≤2017 in May 2018; 2018 in 2019; 2019–2021 in May 2022).
  - **2022 onward:** after each sitting ÖSYM publishes only **10% of the booklet plus the full answer key** publicly. The complete booklet is visible to registered candidates on ais.osym.gov.tr (TC kimlik + password) for **10 days**. No later full release of 2022+ has been found as of this writing; check ÖSYM announcements each cycle.
  - ÖSYM explicitly states the questions are copyrighted works under FSEK. Public ≠ redistributable.
- Cancelled questions happen; the parser must handle "iptal" annotations from the answer key.

---

## 3. Repository layout

```
tus-open/
├── README.md
├── LICENSE-CODE            # MIT or Apache-2.0  (OPEN)
├── LICENSE-CONTENT         # CC BY 4.0 or CC BY-SA 4.0  (OPEN)
├── CONTRIBUTING.md
├── GOVERNANCE.md
├── PERMISSIONS.md          # any written permissions obtained (ÖSYM, faculties)
├── CHANGELOG.md
├── taxonomy/
│   └── taxonomy.yaml
├── content/
│   ├── questions/          # metadata + tags per official question; NO question text
│   │   └── 2025/
│   │       └── sonbahar/
│   │           ├── ttbt.yaml
│   │           └── ktbt.yaml
│   ├── scripts/            # illness scripts, one YAML per condition
│   │   ├── dahiliye/
│   │   ├── pediatri/
│   │   └── ...
│   ├── cases/              # scripted step-by-step cases, one YAML per case
│   ├── walkthroughs/       # annotated reasoning for real past case stems
│   └── facts/              # standalone high-yield facts not tied to a script (use sparingly)
├── schemas/                # JSON Schema for every content type
│   ├── taxonomy.schema.json
│   ├── question.schema.json
│   ├── illness_script.schema.json
│   ├── case.schema.json
│   ├── walkthrough.schema.json
│   └── fact.schema.json
├── src/tusopen/
│   ├── fetch/              # download official ÖSYM PDFs into a local cache
│   ├── parse/              # PDF → structured questions (local only)
│   ├── validate/           # schema + cross-reference validation
│   ├── stats/              # frequency, overlap, trend computation
│   ├── export/
│   │   ├── anki/           # genanki-based exporter
│   │   ├── simulator/      # static site generator for cases + practice sets
│   │   └── oral/           # oral-exam mode (same engine, different prompts)
│   └── cli.py
├── site/                   # generated static output (gitignored except CI artifacts)
├── tests/
│   ├── fixtures/           # synthetic PDFs and YAML for tests; never real ÖSYM text
│   └── ...
└── docs/
    ├── writing-an-illness-script.md
    ├── writing-a-case.md
    ├── writing-a-walkthrough.md
    ├── own-words-policy.md      # §8, with good/bad examples
    ├── tagging-guide.md
    └── release-process.md
```

Language conventions: code and code comments in English; content field **names** in Turkish where they are user-facing in Anki (`soru`, `cevap`, `açıklama`), but schema keys in ASCII-safe Turkish or English (**OPEN:** pick one and stick to it; recommendation: ASCII keys like `aciklama`, Turkish labels in templates).

---

## 4. Taxonomy

`taxonomy/taxonomy.yaml` is the single source of truth for ders → konu → alt konu.

```yaml
version: 1
tests:
  TTBT:
    dersler:
      - id: anatomi
        ad: Anatomi
        konular:
          - id: noroanatomi
            ad: Nöroanatomi
            alt_konular:
              - id: kranial_sinirler
                ad: Kranial Sinirler
              - id: pleksuslar
                ad: Pleksuslar
          - id: ust_ekstremite
            ad: Üst Ekstremite
  KTBT:
    dersler:
      - id: dahiliye
        ad: Dahiliye
        konular:
          - id: endokrin
            ad: Endokrinoloji
            alt_konular:
              - id: tiroid
                ad: Tiroid Hastalıkları
```

Rules:
- Every `id` is unique across the whole tree and stable forever. Renames change `ad`, never `id`.
- No catch-all nodes (`diger`, `genel`). If content has nowhere to go, add a node.
- Cross-listing is allowed: an illness script may carry multiple taxonomy paths (e.g. Wilson under `patoloji.karaciger` and `dahiliye.gastro.karaciger`).
- **OPEN:** initial depth. Recommendation: three levels (ders/konu/alt_konu) for v1; add a fourth only where a konu exceeds ~40 alt_konu.
- **OPEN:** seed source. Options: (a) hand-build from TUS prep-book chapter structures, (b) bootstrap from the `konu` column of alibayram/turkish_mmlu then refine. Either way the result is hand-curated before v1.

---

## 5. Content schemas

All content files are YAML validated against JSON Schema. Common header on every file:

```yaml
id: <stable-unique-id>        # never changes once published
version: 1
status: draft | reviewed | published
author: <github-handle>
reviewed_by: [<handle>, ...]
last_reviewed: 2026-09-05
sources: [<free-text citations or question refs>]
```

### 5.1 Question reference (`content/questions/YYYY/donem/test.yaml`)

No question text. Only metadata that the parser can re-derive and humans add on top.

```yaml
sinav: {yil: 2025, donem: sonbahar, test: KTBT}
sorular:
  - no: 47
    id: tus-2025-sonbahar-ktbt-47
    cevap: C                      # from official key
    iptal: false
    ders: dahiliye
    konu: endokrin
    alt_konu: tiroid
    hastalik: [graves]            # links to illness script ids
    soru_tipi: vaka | bilgi       # case stem vs direct fact
    alt_tip: tani | tetkik | tedavi | komplikasyon | mekanizma   # if vaka
    zorluk: 1-5                   # optional, subjective
    benzer: [tus-2019-ilkbahar-ktbt-52]   # near-duplicate references, filled by stats + human confirm
    notlar: ""
```

### 5.2 Illness script (`content/scripts/<ders>/<id>.yaml`)

The backbone. One per condition.

```yaml
id: wilson
ad: Wilson Hastalığı
taksonomi:
  - [ttbt, patoloji, karaciger, metabolik]
  - [ktbt, dahiliye, gastro, karaciger]
  - [ktbt, pediatri, gastro]
tipik_hasta: "10–40 yaş, hepatik veya nöropsikiyatrik bulgularla başvuran"
patofizyoloji: "ATP7B mutasyonu, bakır atılım defekti, karaciğer ve bazal ganglionlarda birikim"
anahtar_bulgular:
  - "Kayser-Fleischer halkası"
  - "Düşük serum seruloplazmin"
  - "Artmış 24 saatlik idrar bakırı"
patognomonik: "Kayser-Fleischer halkası (nörolojik tutulumda ~%100)"
ilk_tetkik: "Serum seruloplazmin"
kesin_tani: "Karaciğer biyopsisinde bakır > 250 µg/g kuru ağırlık"
ilk_tedavi: "D-penisilamin (veya trientin)"
klasik_komplikasyon: "Fulminan hepatit, Coombs-negatif hemolitik anemi"
ayirici:
  - hastalik: hemokromatoz
    ayirt_edici: "Bakır yerine demir; ferritin ve transferrin satürasyonu yüksek"
  - hastalik: otoimmun_hepatit
    ayirt_edici: "ANA/ASMA pozitif, IgG yüksek, seruloplazmin normal"
tus_gecmisi: [tus-2021-ilkbahar-ktbt-63, tus-2018-sonbahar-ttbt-88]   # filled from questions
kart_uret:
  bilgi: true
  vaka: true
  celdirici: true
  ayirici: true
```

### 5.3 Case (`content/cases/<id>.yaml`)

Scripted, branching, no LLM at runtime.

```yaml
id: case-wilson-01
hastalik: wilson
baslik: "Tremor ve karaciğer enzim yüksekliği olan genç erkek"
adimlar:
  - tip: sunum
    metin: "19 yaşında erkek, 3 aydır ellerde tremor ve konuşmada bozulma..."
  - tip: secim
    soru: "İlk istenecek tetkik?"
    secenekler:
      - {metin: "Serum seruloplazmin", dogru: true, geri_bildirim: "..."}
      - {metin: "Karaciğer biyopsisi", dogru: false, geri_bildirim: "Kesin tanı için ama ilk adım değil"}
      - {metin: "MR", dogru: false, geri_bildirim: "..."}
  - tip: sonuc
    metin: "Seruloplazmin 8 mg/dL (düşük). Yarık lamba: KF halkası pozitif."
  - tip: secim
    soru: "İlk tedavi?"
    secenekler: [...]
  - tip: ozet
    metin: "Öğrenme noktaları: ..."
sozlu_sorular:                 # used by oral-exam mode
  - "Neden önce seruloplazmin?"
  - "Seruloplazmin normal gelirse tanıyı dışlar mısın?"
  - "D-penisilamin yan etkileri?"
```

### 5.4 Walkthrough (`content/walkthroughs/<question-id>.yaml`)

Reasoning commentary on a real past question, written entirely in the contributor's own words. References the question id; never reproduces or closely paraphrases the stem or options. A reader with the booklet open should recognize which question it is; a reader without it should not be able to reconstruct it.

```yaml
id: wt-tus-2025-sonbahar-ktbt-47
soru_ref: tus-2025-sonbahar-ktbt-47
sinanan_bilgi: "Hipertiroidi kliniğinde ilk basamak tetkik seçimi"
ipucu_turleri: ["yaş/cinsiyet profili", "hipermetabolik semptomlar", "guatr karakteri"]   # categories, not the stem's phrases
gurultu_turleri: ["aile öyküsü ayrıntısı"]
mantik: "Klinik tablo hipertiroidiyi düşündürüyorsa önce TSH ve serbest T4; TSH baskılıysa etiyolojiye yönelik ileri tetkik sonraki adımdır."
celdirici_kavramlar:                 # the concept behind each wrong option, in own words
  - kavram: "Sintigrafi"
    neden_yanlis: "Etiyolojiyi ayırt eder ama tanıyı koyan ilk test değildir"
    dogru_oldugu_durum: "TSH baskılı, etiyoloji belirsiz"
```

Validation rejects any field that fails the originality check in §8.2.

### 5.5 Fact (`content/facts/*.yaml`)

For high-yield facts that don't belong to a condition (e.g. anatomy, biochemistry pathways). Keep this small; prefer attaching facts to scripts where possible.

---

## 6. Pipeline

### 6.1 Fetch
- `tusopen fetch --year 2019 --donem ilkbahar` downloads the official booklet and answer-key PDFs from osym.gov.tr into `~/.tusopen/cache/`. Works fully for ~2006–2021.
- For 2022+ the public fetch yields the answer key and the 10% sample only. The CLI must report this clearly rather than silently producing a partial dataset.
- `tusopen import --year 2025 --donem sonbahar --file my_booklet.pdf` lets a candidate load their own AİS copy (saved within the 10-day window) into the local cache. The file never leaves the machine; only the tags they write go into `content/questions/`.
- Cache is never committed.
- **OPEN:** ÖSYM URL patterns change; maintain a small `sources.yaml` mapping sitting → URLs and coverage level (`full` / `sample10`), updated each cycle.

### 6.2 Parse
- PDF text extraction with layout awareness (pdfplumber or PyMuPDF; **OPEN:** benchmark both on a few sittings).
- Turkish handling: normalize İ/ı/i, ş, ğ, ç; watch for OCR-style substitutions in older scanned booklets; older booklets may need OCR (Tesseract with `tur` + `eng`).
- Output: local structured questions (text + options + key) in the cache, plus a metadata stub written into `content/questions/` with `no`, `id`, `cevap`, `iptal`. Humans fill taxonomy and script links.
- Handle both A/B booklet variants and cancelled questions.
- Tests use synthetic fixture PDFs generated in-repo; never real booklets.

### 6.3 Validate
- JSON Schema validation for every YAML.
- Cross-reference checks: every taxonomy path exists; every `hastalik` id resolves to a script; every `soru_ref` resolves; every `benzer` target exists; no duplicate ids; every `published` item has ≥1 reviewer.
- Run in CI on every PR.

### 6.4 Stats
Computed from local parsed text + committed metadata; only aggregate outputs are committed/published.
- Per-sitting and per-ders question counts.
- Topic frequency over time (konu and alt_konu).
- Overlap: exact match, near-duplicate (fuzzy string + embedding similarity, threshold **OPEN**), same-fact-different-angle (human-tagged via `benzer`), same-topic recurrence.
- `siklik` value per script/fact: number of distinct sittings it appears in.
- Outputs: CSV/JSON in `site/stats/` and charts.

### 6.5 Export — Anki
- `genanki` with **stable note GUIDs derived from content ids** (e.g. `guid = hash("tusopen:" + id + ":" + card_type)`). Never regenerate randomly.
- Single deck, no subdecks. Navigation via tags.
- Note types (fields listed in §7).
- Tag stamping from data, never hand-written.
- Versioned `.apkg` per release; keep model ids fixed across versions.
- Optional: publish to AnkiWeb under a project account (**OPEN**).

### 6.6 Export — Simulator (static site)
- Generates a static HTML/JS site from `cases/` and `questions/` metadata.
- Modes: single case, mixed practice set (interleaved by ders/konu, confusable conditions adjacent), timed mock exam (100 questions, 135 minutes, net scoring) — mock exam uses locally cached question text and therefore runs only after the user has fetched booklets.
- No backend; progress in memory or exported as a file.

### 6.7 Export — Oral exam mode
- Same case engine; presents `sozlu_sorular` after the case, with model answers revealed on demand.
- **OPEN:** whether to add examiner "personas" (strict/lenient) as prompt sets.

---

## 7. Anki design

### Tag hierarchy
```
#TUS_v1::Ders::TTBT::Anatomi::Nöroanatomi::KranialSinirler
#TUS_v1::Ders::KTBT::Dahiliye::Endokrin::Tiroid
#TUS_v1::Sınav::2025::Sonbahar::KTBT::Q47
#TUS_v1::Sıklık::5+
#TUS_v1::Sıklık::2-4
#TUS_v1::Sıklık::1
#TUS_v1::Sıklık::0
#TUS_v1::KartTipi::Bilgi | Vaka | Çeldirici | Ayırıcı
#TUS_v1::Hastalık::Wilson
#TUS_v1::Fakülte::<Okul>::<Dönem>::<Ders>     # local extension only
```

### Note types
Common fields on all: `id`, `ders`, `konu`, `alt_konu`, `siklik`, `kaynak`, `hastalik`, `versiyon`, `notlar`.

| Note type | Extra fields | Cards generated |
|---|---|---|
| Bilgi | `soru`, `cevap`, `aciklama` (or cloze) | 1 |
| Vaka | `vinyet`, `soru_tipi`, `cevap`, `anahtar_bulgular`, `aciklama` | 1 per soru_tipi |
| Çeldirici | `vinyet`, `yanlis_secenek`, `neden_yanlis`, `hangi_durumda_dogru` | 1 per distractor |
| Ayırıcı | `tablo` (2–3 conditions × distinguishing features) | cloze per cell |

Card templates show `siklik` as a small badge ("Son 20 sınavda 6 kez").

### Card-generation rules from illness scripts
- Bilgi: one card per field among `patognomonik`, `ilk_tetkik`, `kesin_tani`, `ilk_tedavi`, `klasik_komplikasyon`.
- Vaka: `tipik_hasta` + 2 `anahtar_bulgular` → ask `tani`, `ilk_tetkik`, `ilk_tedavi`.
- Ayırıcı: one table per `ayirici` entry.
- Çeldirici: only from walkthroughs' `celdirici_kavramlar` (concepts behind real distractors, in own words), not synthesized and never the option text.

---

## 8. Content originality policy ("own words")

This is the project's core legal and editorial rule. Every piece of shipped content is an original work by its contributor, describing medical facts and reasoning in their own words. ÖSYM's expression (stems, options, vignettes) is never reproduced, closely paraphrased, or reconstructed.

### 8.1 Rules for contributors
1. Write from your understanding of the topic, not from the question. Close the booklet before writing.
2. Facts are free; wording is not. "Wilson'da ilk tetkik seruloplazmin" is a fact. ÖSYM's sentence asking it is not yours to copy.
3. No verbatim stems, options, or vignettes anywhere in `content/`. This includes walkthroughs: refer to the question by id, describe what it tests, and explain the reasoning without quoting it.
4. No "light" paraphrase. If your text could be aligned sentence-by-sentence with the original, it is a copy. Rewrite from the fact, not from the sentence.
5. Vignettes in `Vaka` cards and `cases/` are invented. Different patient, different framing, different incidental details. Only the clinical logic is shared with the real question.
6. Distractor cards (`Çeldirici`) describe the *concept* behind a wrong option ("sintigrafi ikinci basamaktır, çünkü…"), never the option text as ÖSYM wrote it.
7. Do not copy from prep-company books, notes, or explanations either. They are copyrighted too.
8. Cite sources as references (textbook chapter, guideline), not as text to reproduce.

### 8.2 Automated originality check
`tusopen validate --originality` runs on every PR and release:
- Compares every text field in `content/` against the locally cached ÖSYM booklets (if present on the runner) and against a maintainer-held reference cache.
- Flags n-gram overlap above a threshold (**OPEN:** start at any shared 8-word window, plus fuzzy ratio > 0.6 on any field vs any stem/option) and blocks merge until rewritten.
- Also flags cross-contributor near-duplicates so the deck doesn't accumulate redundant cards.
- CI does not need the booklets to pass; the check is advisory in CI and mandatory in the maintainer's release run.

### 8.3 Review and governance
- Content states: `draft` → `reviewed` → `published`. Only `published` ships.
- Reviewer requirement: at least one reviewer who is a resident or later-year student, distinct from the author. Reviewer confirms both medical accuracy and originality. **OPEN:** two reviewers for `Vaka`/`Çeldirici`.
- PR template requires the contributor to affirm: written in own words; no text from ÖSYM booklets, prep books, or other copyrighted sources; sources listed as references only.
- CODEOWNERS per ders once maintainers exist.
- Release cadence: one release after each sitting (target: within 6 weeks of the ÖSYM key), plus patch releases for corrections.
- Deprecation: ids are never deleted; mark `status: deprecated` with a reason.
- Takedown: if any item is found to reproduce protected text, it is rewritten or deprecated in a patch release; the note GUID is preserved so users keep review history.

---

## 9. Licensing and legal

- Code: MIT or Apache-2.0 (**OPEN**; Apache-2.0 adds an explicit patent grant, MIT is simpler).
- Content (taxonomy, scripts, cases, walkthroughs, facts, tags): CC BY 4.0 or CC BY-SA 4.0 (**OPEN**). This license is valid because, under §8, the project owns everything it ships.
- ÖSYM question text: never committed, never redistributed, never quoted. Fetched by the user from osym.gov.tr or imported from their own AİS copy. Repo stores only ids, answer keys, and tags. ÖSYM states the questions are protected under FSEK; the project treats that as binding.
- The project does not rely on the FSEK quotation exception (m. 35) or on non-enforcement. Own-words content is the sole basis for redistribution.
- `PERMISSIONS.md` records any written permissions (ÖSYM via Hukuk Müşavirliği or CİMER; faculty consent for school-specific extensions). A permission request to ÖSYM may still be sent for goodwill and future options; the build does not depend on it.
- Contributors affirm original authorship in the PR template; a lightweight DCO (`Signed-off-by`) is recommended (**OPEN**).
- Not legal advice; confirm with university legal office.

---

## 10. Milestones

### M0 — Skeleton (1 week)
- Repo layout, licenses (placeholders if undecided), CI running schema validation on fixtures.
- `taxonomy.yaml` for two ders end to end (recommend Anatomi and Dahiliye).
- All JSON Schemas drafted.

### M1 — Parse and stats (2–3 weeks)
- Fetch + parse working on the last 6 fully public sittings (2019–2021), plus the 2022+ answer keys and 10% samples.
- `import` command for candidate-held booklets.
- Metadata stubs generated for those sittings.
- Frequency table by ders; overlap report (exact + fuzzy) between sittings.
- Publish first stats chart, clearly labelled with coverage per sitting.

### M2 — First content and Anki (2–3 weeks)
- 10 illness scripts across 5 ders, fully reviewed.
- Anki exporter with stable GUIDs, all four note types, tag stamping, `siklik` badge.
- Owner uses the deck for two weeks; schema revised.

### M3 — Cases and simulator (3–4 weeks)
- 10 scripted cases (one per script), case schema finalized.
- Static simulator site: single case + mixed practice set.
- Oral-exam mode on the same engine.

### M4 — Open to contributors (ongoing)
- CONTRIBUTING and writing guides with worked examples.
- Tag remaining questions for the 6 parsed sittings (community task).
- Expand scripts toward ~150 high-frequency conditions.
- First versioned release.

### M5 — Full history and mock exams
- Parse the full public archive back to ~2006 (older booklets: 120/test, separate Temel Tıp-1/-2 for non-medical graduates, İngilizce test, scanned PDFs needing OCR).
- Timed mock exam mode using local question text (full for ≤2021; candidate-imported copies for later sittings).
- Overlap statistics across the full history, with a per-sitting coverage flag.
- Watch for ÖSYM batch releases of 2022+ and add them to `sources.yaml` when they appear.

---

## 11. School-specific extensions (local, not in the public repo)

A faculty (or a student at one) can add a private overlay:
- `local/taxonomy_map.yaml`: maps lecture ids → taxonomy nodes.
- `local/lectures/`: lecture metadata (title, professor, date, slide count); slide content stays out of any repo.
- `local/exams/`: parsed faculty exam metadata with taxonomy tags, same schema as ÖSYM questions.
- Exporter adds `#TUS_v1::Fakülte::...` tags and a "TUS relevance" score per lecture (sum of `siklik` over mapped nodes).
- Comparison report: faculty exam topic distribution vs TUS topic distribution.

This overlay is a separate, gitignored directory with its own README; the public repo only ships the schema and tooling for it.

---

## 11b. External datasets — reference only, never ingested

The following datasets exist and may be consulted locally (e.g. to inspect topic labels or sanity-check the parser). **None may be committed, vendored, redistributed, or used to generate shipped content.** Do not add any of them as a dependency, download step, or fixture.

| Dataset | Stated license | Actual status | Allowed use here |
|---|---|---|---|
| alibayram/turkish_mmlu (Zenodo 13378019 / 16283327) | CC BY 4.0 badge | Description says non-commercial only and admits possible copyrighted content; author does not own underlying questions | Local inspection of `konu` labels for taxonomy design |
| bezir/turkish_exam_instructions | none listed | Derived from turkish_mmlu; answers generated by Gemini, may be hallucinated | None |
| turkerberkdonmez/TUSGPT-TR-Medical-Dataset-v1 | Apache 2.0 | Instruction/answer pairs, not TUS questions, provenance unclear | None (not useful) |
| ituperceptron/turkish_medical_reasoning | none listed | Translation of an English dataset; answers from DeepSeek-R1 via a third-party site | None (not TUS) |

Rationale: the repo's content license (CC BY / CC BY-SA) can only cover material the project actually owns. Ingesting any of the above would import unresolvable upstream terms.

## 12. Open decisions (collected)

1. Code license: MIT vs Apache-2.0.
0. Originality-check thresholds (n-gram window, fuzzy ratio) and where the reference cache lives.
2. Content license: CC BY vs CC BY-SA.
3. Taxonomy depth (3 vs 4 levels) and treatment of minor clinical branches.
4. Taxonomy seed: hand-built vs bootstrapped from turkish_mmlu `konu` labels.
5. Schema key language: ASCII-Turkish vs English.
6. PDF library: pdfplumber vs PyMuPDF; OCR path for older booklets.
7. Near-duplicate threshold and method (fuzzy ratio vs embeddings; if embeddings, which Turkish model, run locally).
8. Reviewer count for reasoning-type cards.
9. DCO / CLA policy.
10. AnkiWeb publication and account ownership.
11. Oral-exam examiner personas.
12. Whether to seek a faculty sponsor before or after M2.

---

## 13. Immediate next actions

1. Create the repo with the layout in §3 and placeholder licenses.
2. Write `taxonomy.yaml` for Anatomi and Dahiliye.
3. Write the six JSON Schemas from §5.
4. Implement fetch + parse against the Sonbahar 2025 sitting; write synthetic fixtures for tests.
5. Author one complete illness script (Wilson is the worked example above) and one case; run them through the Anki exporter to validate the end-to-end path.
