# Permissions

Records the project's position on third-party permissions and any written
permissions obtained.

## Current status

**No written permissions have been obtained. None are required for the
current scope of what this repository ships.**

## Why (the legal model, plan §9)

This repository ships only:

1. **Original code** (Apache-2.0), no third-party rights involved.
2. **A topic taxonomy**, a factual classification; classifications are not
   protected works under FSEK and contain no ÖSYM expression.
3. **Own-words content** (scripts, cases, facts, walkthroughs), original
   expression by contributors describing uncopyrightable medical facts,
   enforced by the own-words policy (§8) and the automated originality check.
4. **Question metadata**, ids, tags, `soru_tipi`; pure data. The one gray
   zone is the **answer-key letters** (`cevap`): a key table is factual data
   with no creative expression and is published openly by ÖSYM, but before
   wide publicity the project owner should obtain a written opinion from the
   university legal office confirming this position.

ÖSYM **question text, stems, options and vignettes** never enter the
repository, they live only in a local cache (`~/.tusopen/cache`) that is
never committed, distributed, or hosted. This is enforced by architecture,
not by policy alone: the parse step writes question text only outside the
repo, and the release-time originality check re-verifies zero overlap.

## Do we need ÖSYM's permission?

**No, not for the current scope.** A goodwill permission request is optional
and non-blocking (see draft below). It may be sent for future options (e.g.
deeper cooperation, mock-exam text licensing) and for goodwill, but the
project does not depend on it.

## Takedown posture

If ÖSYM (or any rights holder) identifies a specific item as problematic:
that item is rewritten or `deprecated` in the next patch release, note GUIDs
are preserved so users keep their review history. The project does not rely
on the FSEK quotation exception (m. 35) or on non-enforcement; own-words
content is the sole basis for redistribution.

## Optional goodwill letter (draft, not sent)

> Konu: TUS açık kaynak çalışma sistemi hakkında
>
> Sayılı ilgili birim,
> TUS'a hazırlık için topluluk tarafından geliştirilen, açık kaynaklı bir
> çalışma sistemi yürütüyoruz. Sistemimiz ÖSYM soru metinlerini hiçbir
> biçimde çoğaltmaz, dağıtmaz veya saklamaz; yalnızca kendi özgün ifademizle
> yazılmış ders içerikleri ile sınav sorularına ait üst veri (soru numarası,
> cevap anahtarı, konu etiketi) kullanır. Projenin ÖSYM ile resmi bir bağı
> yoktur ve hiçbir onay ima etmez.
> İyi niyet kapsamında bu durumu bilginize sunar, görüş ve önerilerinizi
> memnuniyetle karşılarız.

Send via CİMER or to ÖSYM Hukuk Müşavirliği if the owner chooses to. A
non-response (the likely outcome) changes nothing about the project's
legality.

## Log

| Date | From | Scope | Status |
|---|---|---|---|
|, |, |, | No requests sent or received yet. |
