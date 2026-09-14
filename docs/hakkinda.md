# Hakkında: amaç, bağımsızlık, lisanslar

Bu belge README'den taşınan ayrıntıları içerir: projenin amacı, bağımsızlık
beyanı, lisans modeli, feragatnameler ve güncel durum.

## Amaç

Bu projenin amacı **aralıklı tekrar (spaced repetition) yöntemini TUS
adaylarına tanıtmak ve yaygınlaştırmaktır**: kanıta dayalı çalışma
tekniklerinin (aralıklı tekrar, aktif hatırlama, test-tekrar döngüsü) TUS
hazırlığında ne kadar etkili olduğunu göstermek ve bu yöntemi herkesin
ücretsiz kullanabilmesini sağlamak. Yöntemin bilimsel temelleri
[anki-ve-aralikli-tekrar.md](anki-ve-aralikli-tekrar.md) belgesinde kaynak
gösterilerek açıklanmıştır.

**Rekabet değil, bilinçlendirme hedeflenmektedir.** Piyasada aralıklı tekrar
temelli ücretli kaynaklar da vardır; bu proje hiçbirinin alternatifi ya da
rakibi olarak konumlanmaz. Hangi kaynağı kullanacağınız tamamen sizin
tercihinizdir; burada anlatılan yöntem mevcut çalışma düzeninizin yanında da
yürür.

## Bağımsızlık beyanı

Bu proje **TUS hazırlığı sunan herhangi bir dershane, kurs ya da yayıneviyle
hiçbir bağı, anlaşması, sponsorluğu veya izni olmadan bağımsız olarak
geliştirilmektedir** ve hiçbir kazanç amacı taşımamaktadır. İçerikler bu
kurumların ders kitaplarından, soru bankalarından veya eğitim
materyallerinden alınmamış, kopyalanmamış ya da uyarlanmamıştır; tamamı bu
projeye özgü yazımdır ve telif/ticari kaynaklara atıf yalnızca bilimsel
referans düzeyinde (kılavuz/ders kitabı adı) kullanılır.

Proje **ÖSYM ile de bağlantılı değildir.** TUS, TTBT ve KTBT ÖSYM'nin sınav
ve test adlarıdır; burada yalnızca tarayıcı (nomsal) olarak, neye hazırlık
sağlandığını anlatmak için kullanılır.

## Lisans modeli

Depoda **yalnızca kod, şema, taksonomi, etiket ve özgün-söz içerik** bulunur;
ÖSYM soru metni asla yer almaz (5846 sayılı FSEK kapsamında korunan eserler).

- Soru metni yalnızca yerel, asla commit edilmeyen önbellekte durur
  (`~/.tusopen/cache`). Kullanıcılar resmi PDF'leri osym.gov.tr'den kendileri
  indirir ya da kendi AİS kopyalarını `tusopen import` ile ekler (tam
  kitapçıklar ~2006-2021 için kamuya açıktır; 2022+ yalnızca %10 örneklem +
  cevap anahtarı yayımlanır).
- İçerik özgün sözlerle yazılır. Bazı taslaklar yapay zekâ desteğiyle
  üretilmiştir; öğeler adlı bir insan gözden geçiren (`reviewed_by`) onayından
  geçmeden `published` olmaz (bkz. [CONTRIBUTING.md](../CONTRIBUTING.md)).
- Lisanslar: kod Apache-2.0 ([LICENSE-CODE](../LICENSE-CODE)); içerik
  (scriptler, vakalar, walkthrough'lar, bilgi kartları) CC BY-SA 4.0
  ([LICENSE-CONTENT](../LICENSE-CONTENT)).
- `content/facts/media/` içindeki görseller üçüncü taraf Wikimedia eserleridir
  ve kendi serbest lisanslarına tabidir (CC0/PD/CC BY/CC BY-SA); görsel başına
  atıf [LICENSE-MANIFEST.md](../content/facts/media/LICENSE-MANIFEST.md)
  dosyasındadır ve çalışma materyallerinin içine gömülüdür.
- Ayrıştırma aşaması PyMuPDF (AGPL-3.0) kullanır; çalışma içeriği bundan
  etkilenmez.

Telif pozisyonunun tamamı ve kaldırma (takedown) prosedürü için
[PERMISSIONS.md](../PERMISSIONS.md) dosyasına bakın.

## Feragatnameler

- **Yalnızca eğitim amaçlıdır, tıbbi tavsiye değildir.** İçerik sınav
  hazırlığı içindir; klinik kararlar için kullanılmamalıdır.
- **Garanti yoktur.** Materyaller "olduğu gibi" sunulur; kullanımdan doğacak
  zararlardan yazarlar sorumlu değildir.
- **Taslak kalitesi (v0.4.0-alpha).** Tüm öğeler `draft` durumundadır: insan
  incelemesi bekleyen yapay zekâ destekli taslaklar. Hiçbiri henüz gözden
  geçiren onaylı değildir; kullanmadan önce bilgiyi bir ders kitabından
  doğrulayın ve hataları issue/PR ile bildirin.
- ÖSYM soru metni bu depoda hiçbir zaman yer almaz.

## Durum

- **İçerik**: 333 hastalık scripti, 5.736 bilgi kartı, 60 vaka, 9 walkthrough,
  tamamı `draft`. Bilgi kartları ve script spot kartları
  [fact-yazim-rehberi.md](fact-yazim-rehberi.md) belgesindeki tek-nokta spot
  kartı standardına uyar.
- **Deste (0.4.0-alpha)**: 10.117 not / 15.557 kart; vaka simülatörü 60 vaka.
- **Soru arşivi**: 54 oturum (2013-2026), 4.253 soru yerel olarak etiketlendi,
  4.292 meta veri stub'ı commit edildi (39 ÖSYM iptal sorusu `iptal` olarak).
- **Taksonomi**: 31 ders (8 TTBT + 23 KTBT), 393 konu, 2.601 alt konu;
  yapay zekâ desteğiyle oluşturuldu, v1 öncesi insan gözden geçirmesi bekliyor.
- **Altyapı**: 6 JSON Şeması, şema + çapraz referans doğrulayıcı, pytest
  takımı, ruff ve özgünlük denetimi CI'da
  ([validate.yml](../.github/workflows/validate.yml)).
- **Sırada**: insan inceleme turu, walkthrough ve çeldirici kart genişletmesi,
  boş derslerin kapsanması.