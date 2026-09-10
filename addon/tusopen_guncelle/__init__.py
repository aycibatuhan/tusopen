# -*- coding: utf-8 -*-
"""TUS Open — Anki güncelleme eklentisi.

GitHub releases sayfasındaki en son tusopen.apkg dosyasını bulur,
yeni sürüm varsa indirip standart içe aktarma penceresini açar.
Notlar kalıcı kimliklerle eşleştiği için zamanlama korunur.
"""
import json
import tempfile
import urllib.request

from aqt import gui_hooks, mw
from aqt.qt import QAction, QMenu, QTimer
from aqt.utils import askUser, showInfo, tooltip

REPO = "aycibatuhan/tusopen"
API_LATEST = "https://api.github.com/repos/{repo}/releases?per_page=1"
UA = "tusopen-anki-eklenti"


def _http_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())


def _download(url, path):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=180) as r:
        with open(path, "wb") as f:
            while True:
                parca = r.read(1 << 16)
                if not parca:
                    break
                f.write(parca)


def _son_suru():
    data = _http_json(API_LATEST.format(repo=REPO))
    if not data:
        return None
    surum = data[0]
    tag = surum.get("tag_name", "")
    apk = next(
        (a for a in surum.get("assets", []) if a["name"].endswith(".apkg")),
        None,
    )
    return {
        "tag": tag,
        "url": apk["browser_download_url"] if apk else None,
        "notlar": surum.get("body", ""),
    }


def _kurulu_suru():
    desteler = mw.col.decks.all_names() if hasattr(mw.col.decks, "all_names") else []
    if "TUS Open" not in desteler:
        return None
    d = mw.col.decks.by_name("TUS Open")
    aciklama = d.get("description") or d.get("desc") or ""
    # "sürüm vX" biçimini ayıkla
    for kelime in aciklama.replace("(", " ").split():
        if kelime.startswith("v0") or kelime.startswith("v1"):
            return kelime.strip("),.")
    return "bilinmiyor"


def _ice_aktar(path, tag):
    """Modern içe aktarma penceresini dene, olmazsa eski içe aktarıcı."""
    try:
        from aqt.import_export.importing import ImportDialog

        ImportDialog(mw, path=path)
        return True
    except Exception:
        pass
    try:
        from anki.importing.apkg import AnkiPackageImporter

        imp = AnkiPackageImporter(mw.col, path)
        imp.run()
        sayi = getattr(imp, "new", 0) + getattr(imp, "updated", 0)
        showInfo(f"TUS Open içe aktarıldı ({tag} güncellemesi).")
        return True
    except Exception:
        return False


def kontrol(sessiz=False):
    conf = mw.addonManager.getConfig(__name__)
    if sessiz and not conf.get("auto_check", True):
        return
    try:
        son = _son_suru()
    except Exception as e:
        if not sessiz:
            showInfo(f"Bağlantı hatası: {e}")
        return
    if not son:
        if not sessiz:
            showInfo("Sürüm bilgisi alınamadı.")
        return
    if son["tag"] == conf.get("installed_version", ""):
        if not sessiz:
            showInfo("TUS Open zaten güncel.")
        return
    if not son["url"]:
        if not sessiz:
            showInfo(f"Sürüm {son['tag']} var ama apkg dosyası yok.")
        return
    if sessiz:
        tooltip(f"TUS Open yeni sürüm: {son['tag']}")
        if not askUser(
            f"TUS Open yeni sürümü var: {son['tag']}\n"
            "Şimdi indirip içe aktarmak ister misiniz?"
        ):
            return
    elif not askUser(
        f"En son sürüm: {son['tag']}\n(şu an kurulu: {_kurulu_suru() or 'yok'})\n\n"
        "İndirip içe aktarmak ister misiniz? Zamanlama korunur."
    ):
        return
    tmp = tempfile.mktemp(suffix=".apkg")
    _download(son["url"], tmp)
    if _kurulu_suru() is None:
        showInfo(
            f"tusopen.apkg indirildi: {tmp}\n"
            "Anki ilk içe aktarımı sizin yapmanızı ister: Dosya ▸ İçe Aktar."
        )
        return
    try:
        from aqt.import_export.importing import ImportDialog

        ImportDialog(mw, path=tmp)
    except Exception:
        try:
            from anki.importing.apkg import AnkiPackageImporter

            imp = AnkiPackageImporter(mw.col, tmp)
            imp.run()
            showInfo(f"TUS Open güncellendi ({son['tag']}).")
        except Exception as e:
            showInfo(
                f"İçe aktarma penceresi açılamadı: {e}\n"
                f"Dosya burada: {tmp}\n"
                "Elle içe aktarın: Dosya ▸ İçe Aktar."
            )
        return
    conf["installed_version"] = son["tag"]
    mw.addonManager.writeConfig(__name__, conf)
    tooltip("TUS Open sürüm penceresi açıldı — İçe Aktar'a basın.")


def _menu_olustur():
    menu = QMenu("&TUS Open", mw)
    a1 = QAction("Güncellemeleri kontrol et", mw)
    a1.triggered.connect(lambda: kontrol(False))
    menu.addAction(a1)
    a2 = QAction("Kurulu sürüm", mw)
    a2.triggered.connect(
        lambda: showInfo(
            f"Kurulu deck sürümü: {_kurulu_suru() or 'yok — önce release apkg içe aktarın.'}"
        )
    )
    menu.addAction(a2)
    mw.form.menuTools.addMenu(menu)


def _profil_acildi():
    QTimer.singleShot(4000, lambda: kontrol(True))


_menu_olustur()
gui_hooks.profile_did_open.append(_profil_acildi)