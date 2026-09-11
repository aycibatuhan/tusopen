# TUS Open — Anki Güncelleme Eklentisi

Anki'nin **Araçlar ▸ TUS Open** menüsünden GitHub Releases sayfasındaki en son
`tusopen.apkg` dosyasını bulur; yeni sürüm varsa indirip içe aktarma penceresini
açar. Notlar kalıcı kimliklerle eşleştiği için **zamanlama (scheduling) korunur**.

## Kurulum

### Yöntem 1 — AnkiWeb Add-on kodu (yakında)
Eklenti AnkiWeb onay sürecindedir; kodu aldıktan sonra buraya yazılacaktır.
O zaman: Anki ▸ Araçlar ▸ Eklentiler ▸ **Get Add-ons** ▸ kodu gir.

### Yöntem 2 — Elle kurulum (şu an aktif)
1. GitHub Releases sayfasından `tusopen_guncelle.ankiaddon` dosyasını indir:
   https://github.com/aycibatuhan/tusopen/releases
2. Anki'de **Araçlar ▸ Eklentiler ▸ Install from file** → indirilen dosyayı seç
3. Anki'yi yeniden başlat
4. İlk kurulumda desteyi de indir: Releases sayfasındaki `tusopen.apkg` →
   çift tıkla ya da Anki ▸ Dosya ▸ İçe Aktar

## Nasıl çalışır
- Profil açılışında sessizce yeni sürüm kontrolü yapar
- Yeni sürüm çıktığında bildirir; onaylarsan indirip içe aktarma penceresini açar
- Not eşleştirme kalıcı kimlikler üzerinden yapıldığı için tekrar içe aktarımda
  çalışma ilerlemen (kart zamanlamaları) kaybolmaz

## Menü
Anki'de **Araçlar ▸ TUS Open**:
- **Güncellemeleri kontrol et** — elle kontrol
- **Kurulu sürüm** — destenin açıklamasından sürümü gösterir

## Ayarlar
`config.json`:
- `auto_check` — profil açılışında otomatik kontrol (varsayılan: açık)
- `installed_version` — eklentinin bildiği son sürüm (otomatik yönetilir)

## Sıkça sorulan

**Yeniden içe aktarımda ilerlemem silinir mi?**
Hayır. Kartlar kalıcı kimliklerle eşleşir; Anki değişen kartları günceller,
zamanlama durur. Yeni kartlar "yeni" olarak gelir.

**"Kurulu sürüm" neden "yok" diyor?**
Desteyi henüz içe aktarmadınız demektir — önce `tusopen.apkg`'yi kurun.

**Eklenti kişisel veri gönderiyor mu?**
Hayır. Yalnızca GitHub API'sine okuma isteği atar; herhangi bir hesap/kimlik
bilgisi gerekmez.

## Sorun bildirimi
https://github.com/aycibatuhan/tusopen/issues