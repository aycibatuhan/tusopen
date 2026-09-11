# TUS Open, Content Authoring Roadmap (subagent-assisted)

Companion to `TUS_OPEN_PROJECT_PLAN.md`. This is the execution plan for going
from 3 pilot illness scripts to **extensive coverage across every ders**.

## 1. Principles (non-negotiable, plan §1/§8)

1. **LLMs draft; humans ship.** Subagents (or Fable) are drafting aids.
   Every item stays `status: draft` with an AI-draft author marker until a
   human reviewer (resident or later-year student) reads it and flips it to
   `reviewed`/`published`. No batch is ever marked published on generation.
2. **Own words at drafting time.** Drafts are written from medical
   understanding, not paraphrased from any source. The originality gate
   (`tusopen validate --originality`) blocks anything that overlaps cached
   ÖSYM text (8-word window / fuzzy > 0.6).
3. **One script per condition.** The YAML lives in the *primary* clinical
   ders directory; other homes are `taksonomi` paths (cross-listing), never
   duplicate files. Condition ids are globally unique and ASCII lowercase.
4. **Everything validates.** Schema + cross-refs run on every batch
   (`tusopen validate`); nothing merges with a red validator.

## 2. Coverage targets

Surface area from `taxonomy.json`: 371 konu, 2,532 alt_konu.
Not every node needs a script, scripts cover *conditions*; procedure/method
ders get facts and walkthroughs instead.

### Tier 1, high-yield core (first two releases)

| Ders | Scripts | Notes |
|---|---|---|
| dahiliye | 40 | the backbone; biggest yield |
| pediatri | 30 | |
| enfeksiyon_hastaliklari | 30 | condition-rich |
| genel_cerrahi | 28 | |
| kadin_dogum | 25 | |
| noroloji | 25 | |
| dermatoloji | 22 | |
| psikiyatri | 22 | |
| kardiyoloji | 20 | |
| ortopedi | 20 | |
| gogus_hastaliklari | 18 | |
| kbb | 16 | |
| goz_hastaliklari | 14 | |
| anesteziyoloji | 8 | malign hipertermi, LA toksisitesi, ... |
| ftr | 8 | omurilik yaralanması, fibromiyalji, ... |
| aile_hekimligi | 6 | mostly cross-lists from other ders |
| halk_sagligi | 4 | rare scripts (aşı reaksiyonları, salgın tipleri) |
| **Script total** | **~320** | |

### Tier 2, method ders coverage (facts, not scripts)

Illness scripts don't fit anatomi/fizyoloji/biyokimya/histoloji/farmakoloji/
radyoloji/nükleer tıp. These get standalone **facts** (`content/facts/`,
schema §5.5) that carry their own TTBT taxonomy paths:

| Ders | Fact cards | Notes |
|---|---|---|
| anatomi | 60 | high-yield regional/neuro facts |
| fizyoloji | 50 | mechanism facts |
| biyokimya | 50 | pathways, deficiencies |
| mikrobiyoloji | 40 | organism properties (not conditions) |
| patoloji | 40 | general-pathology mechanisms |
| histoloji_embriyoloji | 30 | |
| farmakoloji | 45 | drug-class facts |
| **Fact total** | **~270** | |

Cross-referencing does the rest: a script's `patofizyoloji`/`ayirici`
automatically links clinical knowledge to TTBT nodes (like Wilson carries a
`patoloji` path), and facts may also link clinical conditions.

### Tier 3, cases and walkthroughs

- **Cases** (`content/cases/`): one scripted case per Tier-1 condition,
  starting with the top 60. Each case carries `sozlu_sorular` for the
  oral-exam mode.
- **Walkthroughs** (`content/walkthroughs/`): own-words reasoning per real
  past question; prioritized after stub tagging gives frequency data. This is
  the track that also unlocks Çeldirici cards.

## 3. Wave plan

| Wave | Scope | Output |
|---|---|---|
| 1 (done) | Pipeline proof: 3 scripts, 1 case, exporter | 26 cards |
| 2 (done) | Finish M2: 10 scripts across 5 ders | review batch #1 |
| 3 (tranche 4 done) | Tier 1 scripts, 15 ders in parallel | 79 scripts → 327 total, 2,475 notes, **Tier 1 closed** |
| 4 (done) | 32 cases for classic vignettes; 266 facts for 7 TTBT ders (anatomi, fizyoloji, biyokimya, mikrobiyoloji, patoloji, histoloji-embriyoloji, farmakoloji) | deck → 2,741 notes |
| 5 | Walkthroughs after stats-driven frequency table | Çeldirici cards |

Waves 3–4 are parallelizable: batches are dispatched per ders with
independent condition lists.

## 4. Subagent batch protocol

Each batch = one ders (dahiliye split into 2–3 batches). Per batch:

1. **Dispatch**, I pre-assign: condition list, ASCII script ids, primary
   directory, and (for shared conditions) which scripts already exist.
   The subagent must read:
   - `schemas/illness_script.schema.json` (exact field contract)
   - `taxonomy/taxonomy.json` (only real ids go in `taksonomi`/stubs)
   - `content/scripts/dahiliye/wilson.yaml` (style/depth template)
   - plan §7 card rules (what makes a card)
2. **Draft**, 5–8 scripts per batch, all own-words Turkish, `status: draft`,
   `author: ai-drafts/<agent>`, sources as reference citations only.
   `ayirici` entries may only reference scripts that exist after the batch.
3. **QA gate**, `tusopen validate --originality`, then `tusopen export anki`
   and count delta. Any failure loops back to the subagent with the validator
   output verbatim.
4. **Review queue**, the human review backlog grows; nothing becomes
   `published` without a named human reviewer (validator enforces this).

## 5. Sequencing dependency

Question-stub tagging (ders/konu/hastalik) and stats (§6.4) are the compass
for frequency-first ordering. Tier 1 lists are subjective high-yield now;
after tagging, `siklik` re-ranks the queue so the next batch targets what TUS
actually repeats.

## 6. Scale accounting

| Content type | Now | Tier 1 target |
|---|---|---|
| Illness scripts | 327 (16 ders) | ~300, **REACHED** |
| Cases | 60 | ~60, **REACHED** |
| Facts | 266 | ~270, **REACHED** |
| Walkthroughs | 0 | **tagging COMPLETE, unblocked** |
| Tagged stubs | **4,253/4,292** (100% of active questions; 39 iptal excluded by design) | 4,292, **REACHED** |
| Anki notes | 2,741 | scales with content |

Tagging archive stats (54 exams, 2013–2026): 1,097 illness-script links; 14 scripts
gained their first real question refs via backfill; top all-time topics: fırsatçı
mikozlar (23x), herpesvirüsler (17x), antiprotozoal/antihelmintik ilaçlar (17x),
meme karsinomu (16x).
