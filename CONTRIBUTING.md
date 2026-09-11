# Contributing to TUS Open

Thanks for considering a contribution. This project only works because of two
rules everyone accepts up front: **own words** and **human review**. Everything
else is mechanics.

## TL;DR

1. Fork / branch → write YAML → `tusopen validate` → PR
2. Every PR affirms the own-words affirmation (below)
3. CI runs schema + cross-reference validation; it must stay green
4. A human reviewer (not the author) flips `draft → reviewed`; releases ship only `published`

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
   fact, ÖSYM's sentence asking it is not yours to copy.
3. No verbatim stems, options, or vignettes anywhere in `content/`.
   Walkthroughs refer to questions by id and describe the *reasoning*, never
   the text.
4. No "light" paraphrase. If your text could be aligned sentence-by-sentence
   with an original, rewrite from the fact.
5. Case vignettes are invented: different patient, different framing, only the
   clinical logic shared.
6. Distractor cards describe the *concept* behind a wrong option, never the
   option text.
7. Prep-company books and notes are copyrighted too, same rules apply.
8. Cite sources as references, not as text to reproduce.

**AI assistance is allowed as a drafting aid**, but you are the author of
record: review every line for medical accuracy and originality before
submitting, and set the `author` field honestly. Every item still needs a
human reviewer who is not you.

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
- No raw `<`, `>`, `&` characters in field values, write them out in words.
- Match the style/depth of `content/scripts/dahiliye/wilson.yaml` (scripts) or
  `content/cases/case-wilson-01.yaml` (cases).

## Local checks before pushing

```bash
pip install -e .
tusopen validate                  # schemas + cross-references
tusopen validate --originality    # own-words check (needs local parsed cache)
tusopen export anki               # deck must still build
```

CI runs the same validation on every PR, it must stay green.

## Review and status lifecycle

```
draft ──(reviewer)──> reviewed ──(maintainer)──> published
```

- Reviewers: at least one resident or later-year student, **distinct from the
  author**, confirming both medical accuracy and originality.
- ids are never deleted: deprecated items get `status: deprecated` with a
  reason in `notlar`. If any item is found to reproduce protected text, it is
  rewritten or deprecated in the next patch release (note GUIDs are preserved
  so users keep their review history).

## Question tagging

Question stubs are metadata-only (ids, answer keys, tags, no question text).
Tagging workflow: `tusopen tag --dump <exam>` → fill `ders/konu/alt_konu`
from `taxonomy/taxonomy.json` (AI-assisted tagging is welcome) →
`tusopen tag --apply <exam>`. Tags are drafts and reviewed like everything
else.

## Licensing

By contributing you agree your contribution is licensed under the repo
licenses: Apache-2.0 for code, CC BY-SA 4.0 for content. Adding
`Signed-off-by: Your Name <email>` to your commits (DCO) is appreciated.
