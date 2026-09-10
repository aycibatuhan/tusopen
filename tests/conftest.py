from pathlib import Path

import pytest


@pytest.fixture
def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


@pytest.fixture
def tmp_content(tmp_path) -> Path:
    """Minimal content root with one script, fact and case."""
    root = tmp_path / "content"
    (root / "scripts" / "dahiliye").mkdir(parents=True)
    (root / "facts").mkdir()
    (root / "cases").mkdir()
    (root / "cases" / "case-test-01.yaml").write_text(
        "id: case-test-01\n"
        "version: 1\n"
        "status: draft\n"
        "author: testci\n"
        "sources: ['Özgün vaka']\n"
        "hastalik: test_hastalik\n"
        "baslik: Test vakası\n"
        "adimlar:\n"
        "  - tip: sunum\n"
        "    metin: 'Sunum metni. İkinci cümle.'\n"
        "  - tip: secim\n"
        "    soru: 'Ne yapılır?'\n"
        "    secenekler:\n"
        "      - metin: 'Doğru seçenek'\n"
        "        dogru: true\n"
        "        geri_bildirim: 'Doğru çünkü böyle.'\n"
        "      - metin: 'Yanlış seçenek'\n"
        "        dogru: false\n"
        "        geri_bildirim: 'Yanlış çünkü öyle.'\n"
        "  - tip: ozet\n"
        "    metin: 'Özet metni.'\n"
        "sozlu_sorular:\n"
        "  - 'Sözlü soru bir?'\n",
        encoding="utf-8")
    (root / "scripts" / "dahiliye" / "test_hastalik.yaml").write_text(
        "id: test_hastalik\n"
        "version: 1\n"
        "status: draft\n"
        "author: testci\n"
        "sources: ['test kaynak — metin özgün yazımdır']\n"
        "ad: Test Hastalığı\n"
        "taksonomi:\n"
        "  - [ktbt, dahiliye, dah_hepatoloji, dah_hep_wilson_hemokromatoz]\n"
        "tipik_hasta: 'Orta yaşta hastada bulgular. İkinci bulgu cümlesi.\n"
        "  Üçüncü bulgu cümlesi.'\n"
        "anahtar_bulgular:\n"
        "  - 'Birinci bulgu'\n"
        "  - 'İkinci bulgu'\n"
        "patofizyoloji: 'Mekanizma birinci cümle. Mekanizma ikinci cümle.'\n"
        "patognomonik: null\n"
        "ilk_tetkik: 'Tek cümlelik tetkik.'\n"
        "kesin_tani: 'Tanı birinci cümlesi burada yeterince uzun yazılmış durumdadır.\n"
        "  Tanı ikinci cümlesi burada yeterince uzun yazılmış durumdadır.\n"
        "  Tanı üçüncü cümlesi burada yeterince uzun yazılmış durumdadır.\n"
        "  Tanı dördüncü cümlesi burada yeterince uzun yazılmış durumdadır.\n"
        "  Tanı beşinci cümlesi burada yeterince uzun yazılmış durumdadır.\n"
        "  Tanı altıncı cümlesi burada yeterince uzun yazılmış durumdadır.\n"
        "  Tanı yedinci cümlesi burada yeterince uzun yazılmış durumdadır.'\n"
        "ilk_tedavi: 'Tedavi cümlesi.'\n"
        "klasik_komplikasyon: 'Komplikasyon cümlesi.'\n"
        "kart_uret: {bilgi: true, spot: true, vaka: true, ayirici: false, celdirici: false}\n",
        encoding="utf-8")
    (root / "facts" / "test_fakt.yaml").write_text(
        "id: test_fakt\n"
        "version: 1\n"
        "status: draft\n"
        "author: testci\n"
        "sources: ['test kaynak — metin özgün yazımdır']\n"
        "ad: Test Faktı\n"
        "taksonomi:\n"
        "  - [ttbt, anatomi, anat_genel, anat_genel_terminoloji]\n"
        "metin: 'İlk cümle cevabı burada. Açıklama ikinci cümle. Açıklama üçüncü.'\n",
        encoding="utf-8")
    return root
