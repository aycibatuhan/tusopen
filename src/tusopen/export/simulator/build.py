"""Build the static TUS Open case simulator (plan §6.6).

Reads content/cases/*.yaml and emits a single self-contained HTML SPA
(site/simulator/index.html, vanilla JS + inline CSS, no CDN) plus the raw
case data (site/simulator/cases.json). The output opens directly via file://.
"""
import json
import re
from pathlib import Path

import yaml

DONE_KEY = "tusopen_sim_done_v1"

# Sentence-level line breaking for vignettes/feedback (readability).
_ABBREVS = {"dr", "prof", "doç", "vs", "vb", "bkz", "md", "bk", "çev",
            "ing", "fr", "alm", "lat", "yun"}
_SENT_BOUNDARY = re.compile(r"(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ\"“«(0-9])")


def _prose_nl(text) -> str:
    if not text:
        return text
    parts, prev = [], 0
    for m in _SENT_BOUNDARY.finditer(text):
        tail = re.search(r"(\S+)$", text[:m.start()])
        word = tail.group(1).lower().rstrip(".") if tail else ""
        if re.fullmatch(r"[a-zçğıöşü]", word) or word in _ABBREVS:
            continue
        parts.append(text[prev:m.end()].rstrip())
        prev = m.end()
    parts.append(text[prev:])
    return "\n".join(p for p in parts if p)

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>TUS Open · Vaka Simülatörü</title>
<style>
:root{--bg:#fafafa;--fg:#222;--muted:#666;--panel:#f5f5f5;--card:#fff;--border:#aaa;--accent:#35c;--accent-bg:#eef;--ok:#0f6a2f;--ok-bg:#e6f4ea;--bad:#a93226;--bad-bg:#fdecea}
@media (prefers-color-scheme:dark){:root{--bg:#1b1b1d;--fg:#e8e8e8;--muted:#aaa;--panel:#333;--card:#242427;--border:#555;--accent:#9ec1ff;--accent-bg:#25324a;--ok:#7ee2a8;--ok-bg:#24382b;--bad:#ff9a8f;--bad-bg:#3d2422}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
main{max-width:720px;margin:0 auto;padding:20px 16px 56px}
header.site{border-bottom:1px solid var(--border)}
header.site .inner{max-width:720px;margin:0 auto;padding:12px 16px}
.brand{font-weight:600;color:var(--fg)}
.brand:hover{text-decoration:none}
.brand .badge{margin-left:8px}
h1{font-size:22px;line-height:1.3;margin:6px 0 4px}
h2.soru{font-size:18px;line-height:1.4;margin:4px 0 12px}
.muted{color:var(--muted)}
.badge{display:inline-block;background:var(--accent-bg);color:var(--accent);border-radius:4px;padding:1px 8px;font-size:13px}
.meta{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:4px 0 8px}
.back{display:inline-block;font-size:14px}
.case-head{margin-bottom:16px}
.step-label{font-size:13px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;margin:0 0 6px}
.vinyet{background:var(--panel);padding:12px 14px;border-radius:6px;margin:0 0 12px;white-space:pre-line}
.vinyet.ozet{border-left:4px solid var(--accent)}
.bar{height:4px;background:var(--panel);border-radius:2px;overflow:hidden;margin-top:10px}
.bar-fill{height:100%;width:0;background:var(--accent);transition:width .2s}
.options{display:flex;flex-direction:column;gap:8px;margin:0 0 12px}
.btn{font:inherit;line-height:1.4;text-align:left;background:var(--card);color:var(--fg);border:1px solid var(--border);border-radius:6px;padding:10px 14px;cursor:pointer}
.btn:hover:not(:disabled){border-color:var(--accent)}
.btn:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.btn:disabled{cursor:default}
.btn.primary{background:var(--accent-bg);border-color:var(--accent-bg);color:var(--accent);font-weight:600;text-align:center}
.btn.secondary{border-color:var(--accent);color:var(--accent);text-align:center}
.btn.option:disabled{opacity:.8}
.btn.option.correct{border-color:var(--ok);color:var(--ok);background:var(--ok-bg)}
.btn.option.picked-bad{border-color:var(--bad);color:var(--bad);background:var(--bad-bg)}
.btn.option.correct:disabled,.btn.option.picked-bad:disabled{opacity:1}
.actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:4px}
.fb{display:none;border-radius:6px;padding:10px 14px;margin:0 0 12px;white-space:pre-line}
.fb:focus{outline:none}
.fb.ok{display:block;background:var(--ok-bg);color:var(--ok)}
.fb.bad{display:block;background:var(--bad-bg);color:var(--bad)}
.fb.note{display:block;background:var(--panel);color:var(--muted)}
.fb-label{font-weight:700;font-size:13px;text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px}
.score{font-weight:600;margin:0 0 12px}
.case-list{display:flex;flex-direction:column;gap:8px}
.case-item{display:flex;align-items:stretch;border:1px solid var(--border);border-radius:6px;background:var(--card);overflow:hidden}
.case-item:hover{border-color:var(--accent)}
.case-main{flex:1;display:block;padding:12px 14px;color:inherit;min-width:0}
.case-title{font-weight:600}
.case-main:hover{text-decoration:none}
.check{color:var(--ok);font-size:13px}
.oral-link{display:flex;align-items:center;padding:0 14px;border-left:1px solid var(--border);color:var(--accent);font-size:14px;white-space:nowrap}
.foot{margin-top:24px;font-size:13px;color:var(--muted)}
@media (max-width:480px){.oral-link{padding:0 10px;font-size:13px}}
</style>
</head>
<body>
<header class="site"><div class="inner">
<a class="brand" href="#/">TUS Open<span class="badge">Vaka Simülatörü</span></a>
</div></header>
<main id="app"></main>
<noscript>Bu simülatör JavaScript gerektirir.</noscript>
<script id="case-data" type="application/json">__CASE_DATA__</script>
<script>
"use strict";
var DATA = JSON.parse(document.getElementById("case-data").textContent);
var CASES = DATA.cases;
var DONE_KEY = "__DONE_KEY__";
var app = document.getElementById("app");
var session = null;

function byId(id){ return CASES.find(function(c){ return c.id === id; }); }
function doneSet(){
  try{ return new Set(JSON.parse(localStorage.getItem(DONE_KEY) || "[]")); }
  catch(e){ return new Set(); }
}
function markDone(id){
  var s = doneSet();
  if(s.has(id)) return;
  s.add(id);
  try{ localStorage.setItem(DONE_KEY, JSON.stringify(Array.from(s))); }catch(e){}
}
function el(tag, cls, text){
  var n = document.createElement(tag);
  if(cls) n.className = cls;
  if(text != null) n.textContent = text;
  return n;
}
function btn(label, cls, onClick){
  var b = el("button", cls ? "btn " + cls : "btn", label);
  b.type = "button";
  b.addEventListener("click", onClick);
  return b;
}
function devamLabel(){
  return session.i + 1 < session.c.adimlar.length ? "Devam" : "Bitir";
}
function goNext(){
  session.i += 1;
  if(session.i >= session.c.adimlar.length){ location.hash = "#/"; return; }
  renderStep();
}
function caseHead(title, badgeText, stepText, ratio){
  var head = el("div", "case-head");
  var back = el("a", "back", "← Vakalar");
  back.href = "#/";
  head.appendChild(back);
  head.appendChild(el("h1", null, title));
  var meta = el("div", "meta");
  meta.appendChild(el("span", "badge", badgeText));
  if(stepText) meta.appendChild(el("span", "muted", stepText));
  head.appendChild(meta);
  var bar = el("div", "bar"), fill = el("div", "bar-fill");
  fill.style.width = Math.round(100 * ratio) + "%";
  bar.appendChild(fill);
  head.appendChild(bar);
  return head;
}
function renderHome(){
  app.textContent = "";
  var done = doneSet();
  var head = el("div", "case-head");
  head.appendChild(el("h1", null, "Vakalar"));
  head.appendChild(el("p", "muted", CASES.length + " vaka · " + done.size + " tamamlandı"));
  app.appendChild(head);
  if(!CASES.length){
    app.appendChild(el("p", "muted", "Vaka bulunamadı."));
    return;
  }
  var list = el("div", "case-list");
  CASES.forEach(function(c){
    var item = el("div", "case-item");
    var main = el("a", "case-main");
    main.href = "#/case/" + c.id;
    main.appendChild(el("div", "case-title", c.baslik));
    var meta = el("div", "meta");
    meta.appendChild(el("span", "badge", c.hastalik));
    meta.appendChild(el("span", "muted", c.adimlar.length + " adım"));
    if(done.has(c.id)) meta.appendChild(el("span", "check", "✓ Tamamlandı"));
    main.appendChild(meta);
    item.appendChild(main);
    if((c.sozlu_sorular || []).length){
      var oral = el("a", "oral-link", "Sözlü");
      oral.href = "#/oral/" + c.id;
      oral.title = "Sözlü sınav";
      item.appendChild(oral);
    }
    list.appendChild(item);
  });
  app.appendChild(list);
  app.appendChild(el("p", "foot",
    "© 2026 Batuhan Ayci ve katkıcılar · TUS Open · İçerik CC BY-SA 4.0, kod Apache-2.0 · "
    + "Tıbbi doğruluk garantisi yoktur, tek başına çalışma kaynağı değildir · ÖSYM ile bağı yoktur · "
    + "İlerleme yalnızca bu tarayıcıda saklanır."));
}
function startCase(id){
  var c = byId(id);
  session = { c: c, i: 0, score: 0, answered: 0 };
  renderStep();
}
function renderStep(){
  var c = session.c, step = c.adimlar[session.i];
  app.textContent = "";
  app.appendChild(caseHead(c.baslik, c.hastalik,
    "Adım " + (session.i + 1) + " / " + c.adimlar.length,
    (session.i + 1) / c.adimlar.length));
  var body = el("div", "step");
  if(step.tip === "secim"){
    var prior = c.adimlar.slice(0, session.i).filter(function(p){ return p.tip !== "secim"; });
    if(prior.length){
      body.appendChild(el("p", "step-label", "Önceki bulgular"));
      prior.forEach(function(prev){
        body.appendChild(el("div", "vinyet", prev.metin));
      });
    }
    renderSecim(body, step);
  }
  else if(step.tip === "ozet") renderOzet(body, step);
  else {
    body.appendChild(el("div", "vinyet", step.metin));
    body.appendChild(btn(devamLabel(), "primary", goNext));
  }
  app.appendChild(body);
  window.scrollTo(0, 0);
}
function renderSecim(body, step){
  body.appendChild(el("h2", "soru", step.soru));
  var opts = el("div", "options");
  var fb = el("div", "fb");
  fb.setAttribute("role", "status");
  fb.setAttribute("aria-live", "polite");
  fb.setAttribute("tabindex", "-1");
  var actions = el("div", "actions");
  var picked = false;
  step.secenekler.forEach(function(o){
    var b = btn(o.metin, "option", function(){
      if(picked) return;
      picked = true;
      session.answered += 1;
      if(o.dogru) session.score += 1;
      Array.prototype.forEach.call(opts.children, function(ob, j){
        ob.disabled = true;
        if(step.secenekler[j].dogru) ob.classList.add("correct");
      });
      if(!o.dogru) b.classList.add("picked-bad");
      fb.className = "fb " + (o.dogru ? "ok" : "bad");
      fb.appendChild(el("div", "fb-label", o.dogru ? "Doğru" : "Yanlış"));
      fb.appendChild(el("div", null, o.geri_bildirim));
      var d = btn(devamLabel(), "primary", goNext);
      actions.appendChild(d);
      fb.focus();
    });
    opts.appendChild(b);
  });
  body.appendChild(opts);
  body.appendChild(fb);
  body.appendChild(actions);
}
function renderOzet(body, step){
  if(session.answered) markDone(session.c.id);
  body.appendChild(el("p", "step-label", "Özet"));
  body.appendChild(el("div", "vinyet ozet", step.metin));
  if(session.answered){
    body.appendChild(el("p", "score",
      "Bu vaka: " + session.score + " / " + session.answered + " doğru"));
  }
  var actions = el("div", "actions");
  actions.appendChild(btn("Ana Sayfa", "primary", function(){ location.hash = "#/"; }));
  if((session.c.sozlu_sorular || []).length){
    actions.appendChild(btn("Sözlü Sınav", "secondary",
      function(){ location.hash = "#/oral/" + session.c.id; }));
  }
  body.appendChild(actions);
}
function oralView(c){
  var qs = c.sozlu_sorular || [];
  var ozet = null;
  c.adimlar.forEach(function(s){ if(s.tip === "ozet") ozet = s.metin; });
  var idx = 0, revealed = false;
  function paint(){
    app.textContent = "";
    var head = el("div", "case-head");
    var back = el("a", "back", "← Vakalar");
    back.href = "#/";
    head.appendChild(back);
    head.appendChild(el("h1", null, "Sözlü Sınav"));
    var meta = el("div", "meta");
    meta.appendChild(el("span", "badge", c.hastalik));
    meta.appendChild(el("span", "muted", c.baslik));
    head.appendChild(meta);
    app.appendChild(head);
    var body = el("div", "step");
    if(!qs.length){
      body.appendChild(el("p", "muted", "Bu vaka için sözlü soru yok."));
      app.appendChild(body);
      return;
    }
    body.appendChild(el("p", "step-label", "Soru " + (idx + 1) + " / " + qs.length));
    body.appendChild(el("div", "vinyet", qs[idx]));
    var actions = el("div", "actions");
    if(revealed){
      var note = el("div", "fb note");
      note.setAttribute("role", "status");
      note.setAttribute("aria-live", "polite");
      note.appendChild(el("div", "fb-label", "Model cevap çerçevesi"));
      note.appendChild(el("div", null,
        "Cevabını yüksek sesle söyle; anahtar noktaları aşağıdaki özetle karşılaştır."));
      if(ozet) note.appendChild(el("div", "vinyet", ozet));
      body.appendChild(note);
      if(idx + 1 < qs.length){
        actions.appendChild(btn("Sonraki Soru", "primary",
          function(){ idx += 1; revealed = false; paint(); }));
      } else {
        actions.appendChild(btn("Ana Sayfa", "primary",
          function(){ location.hash = "#/"; }));
      }
    } else {
      actions.appendChild(btn("Cevabı Göster", "primary",
        function(){ revealed = true; paint(); }));
    }
    body.appendChild(actions);
    app.appendChild(body);
  }
  paint();
}
function route(){
  var parts = location.hash.replace(/^#\/?/, "").split("/").filter(Boolean);
  session = null;
  if(parts[0] === "case" && byId(parts[1])) startCase(parts[1]);
  else if(parts[0] === "oral" && byId(parts[1])) oralView(byId(parts[1]));
  else renderHome();
  window.scrollTo(0, 0);
}
window.addEventListener("hashchange", route);
route();
</script>
</body>
</html>
"""


def _load_cases(content_root: Path) -> list:
    cases_dir = content_root / "cases"
    cases = []
    if not cases_dir.is_dir():
        return cases
    for path in sorted(cases_dir.rglob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if data.get("status") == "deprecated":
            continue
        for adim in data.get("adimlar", []):
            if adim.get("metin"):
                adim["metin"] = _prose_nl(adim["metin"])
            for sec in adim.get("secenekler", []) or []:
                if sec.get("geri_bildirim"):
                    sec["geri_bildirim"] = _prose_nl(sec["geri_bildirim"])
        cases.append(data)
    cases.sort(key=lambda c: c["id"])
    return cases


def _json_blob(data) -> str:
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return (text.replace("</", "<\\/")
                 .replace("\u2028", "\\u2028")
                 .replace("\u2029", "\\u2029"))


def run(content_root: Path, out_path: Path) -> int:
    cases = _load_cases(content_root)
    payload = {"cases": cases}
    out_path.mkdir(parents=True, exist_ok=True)
    (out_path / "cases.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    html = (HTML_TEMPLATE
            .replace("__DONE_KEY__", DONE_KEY)
            .replace("__CASE_DATA__", _json_blob(payload)))
    (out_path / "index.html").write_text(html, encoding="utf-8")
    return len(cases)
