# Geliştirme: kurulum, üretim hattı, doğrulama

Bu belge projeyi kaynaktan kurup içerik üretmek/doğrulamak isteyenler içindir.
Yalnızca desteyi kullanmak istiyorsanız [README](../README.md) yeterli.

## Kurulum

```bash
python3 -m venv .venv
.venv/bin/pip install -e .

.venv/bin/tusopen --help
.venv/bin/tusopen validate          # şemalar + çapraz referanslar (cache gerekmez)
.venv/bin/tusopen export anki       # Anki destesini üret (site/anki/tusopen.apkg)
.venv/bin/tusopen export simulator  # vaka simülatörünü üret (site/simulator/)
```

Önbellek varsayılan olarak `~/.tusopen/cache` altındadır ve **asla commit
edilmez**. Soru arşivi işlemleri için:

```bash
.venv/bin/tusopen fetch              # resmi ÖSYM PDF'lerini indir
.venv/bin/tusopen parse --all        # PDF -> yerel JSON + content/ stub'ları
.venv/bin/tusopen validate --originality   # özgünlük denetimi (yerel cache ister)
.venv/bin/tusopen tag --dump <exam>  # soru etiketleme çalışma sayfası
.venv/bin/tusopen review --dump      # insan inceleme çalışma sayfası (CSV)
```

## Depo düzeni

```
taxonomy/taxonomy.json     konu taksonomisi: ders -> konu -> alt_konu (3 düzey, kalıcı kimlikler)
content/                   commit edilen içerik (meta veri stub'ları, özgün-söz dosyalar)
  questions/               oturum başına soru meta verisi (soru metni yok)
  scripts/ facts/ cases/ walkthroughs/   içerik türleri
schemas/                   her içerik türü için JSON Şeması
src/tusopen/               CLI üretim hattı (fetch, parse, stubs, tag, validate, review, export)
tests/                     pytest takımı
addon/                     Anki güncelleme eklentisi
docs/                      belgeler
~/.tusopen/cache/          yalnızca yerel: ham PDF'ler + ayrıştırılmış soru metni
```

`content/questions/<yil>/<donem>/<test>.yaml` dosyaları yalnızca meta veri
stub'larıdır (soru kimlikleri, cevap anahtarları, `iptal` bayrakları, boş
etiket alanları); katkıcılar taksonomi kimliklerini ve hastalık script
bağlantılarını oraya yazar.

## İçerik üretim hattı

1. Ders materyali (slayt/PDF) metne çevrilir.
2. Metinden özgün sözlerle bilgi kartı/script taslağı üretilir.
3. `tusopen validate` şema ve çapraz referansları denetler.
4. `tusopen validate --originality` ÖSYM arşivine karşı özgünlük denetler.
5. Kaynak materyale karşı örtüşme denetimi:
   `python3 local/tools/check_overlap.py <fact dosyaları>` (yerel araç;
   kaynak slayt metinleriyle 6-kelime pencere ve shingle örtüşmesini ölçer).
6. İnsan gözden geçirmesi: `tusopen review --dump` çalışma sayfası doldurulur,
   `tusopen review --apply` ile `reviewed_by` alanına işlenir.

## Doğrulama ve test

```bash
.venv/bin/tusopen validate            # şema + çapraz referans
.venv/bin/tusopen validate --originality
.venv/bin/python -m pytest -q
.venv/bin/ruff check src tests
```

CI her push/PR'da aynılarını çalıştırır
([.github/workflows/validate.yml](../.github/workflows/validate.yml)).

## Katkı

İçerik yazım kuralları, own-words politikası ve inceleme yaşam döngüsü için
[CONTRIBUTING.md](../CONTRIBUTING.md) belgesine bakın. Özetle: özgün sözler,
ÖSYM/yayınevi metni yok, yazardan başka bir insan gözden geçirir.