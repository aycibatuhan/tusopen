# TUS Open, Anki Güncelleme Eklentisi / Update Add-on

---

## Türkçe

Anki'nin **Araçlar ▸ TUS Open** menüsünden GitHub Releases sayfasındaki en son
`tusopen.apkg` dosyasını bulur; yeni sürüm varsa indirip içe aktarma penceresini
açar. Notlar kalıcı kimliklerle eşleştiği için **zamanlama (scheduling) korunur**.

### Kurulum

**Yöntem 1, AnkiWeb Add-on kodu (yakında)**
Eklenti AnkiWeb onay sürecindedir; kodu aldıktan sonra buraya yazılacaktır.
O zaman: Anki ▸ Araçlar ▸ Eklentiler ▸ **Get Add-ons** ▸ kodu gir.

**Yöntem 2, Elle kurulum (şu an aktif)**
1. GitHub Releases sayfasından `tusopen_guncelle.ankiaddon` dosyasını indir:
   https://github.com/aycibatuhan/tusopen/releases
2. Anki'de **Araçlar ▸ Eklentiler ▸ Install from file** → indirilen dosyayı seç
3. Anki'yi yeniden başlat
4. İlk kurulumda desteyi de indir: Releases sayfasındaki `tusopen.apkg` →
   çift tıkla ya da Anki ▸ Dosya ▸ İçe Aktar

### Nasıl çalışır
- Profil açılışında sessizce yeni sürüm kontrolü yapar
- Yeni sürüm çıktığında bildirir; onaylarsan indirip içe aktarma penceresini açar
- Not eşleştirme kalıcı kimlikler üzerinden yapıldığı için tekrar içe aktarımda
  çalışma ilerlemen (kart zamanlamaları) kaybolmaz

### Menü
Anki'de **Araçlar ▸ TUS Open**:
- **Güncellemeleri kontrol et**, elle kontrol
- **Kurulu sürüm**, destenin açıklamasından sürümü gösterir

### Ayarlar
`config.json`:
- `auto_check`, profil açılışında otomatik kontrol (varsayılan: açık)
- `installed_version`, eklentinin bildiği son sürüm (otomatik yönetilir)

### Sıkça sorulan

**Yeniden içe aktarımda ilerlemem silinir mi?**
Hayır. Kartlar kalıcı kimliklerle eşleşir; Anki değişen kartları günceller,
zamanlama durur. Yeni kartlar "yeni" olarak gelir.

**"Kurulu sürüm" neden "yok" diyor?**
Desteyi henüz içe aktarmadınız demektir, önce `tusopen.apkg`'yi kurun.

**Eklenti kişisel veri gönderiyor mu?**
Hayır. Yalnızca GitHub API'sine okuma isteği atar; herhangi bir hesap/kimlik
bilgisi gerekmez.

### Sorun bildirimi
https://github.com/aycibatuhan/tusopen/issues

---

## English

This add-on finds the latest `tusopen.apkg` on the GitHub Releases page from
Anki's **Tools ▸ TUS Open** menu; if a new version exists it downloads it and
opens the import dialog. Notes are matched by permanent IDs, so your
**scheduling is preserved**.

### Installation

**Method 1, AnkiWeb Add-on code (coming soon)**
The add-on is in AnkiWeb review; the code will be posted here once approved.
Then: Anki ▸ Tools ▸ Add-ons ▸ **Get Add-ons** ▸ enter the code.

**Method 2, Manual install (active now)**
1. Download `tusopen_guncelle.ankiaddon` from the Releases page:
   https://github.com/aycibatuhan/tusopen/releases
2. In Anki: **Tools ▸ Add-ons ▸ Install from file** → pick the downloaded file
3. Restart Anki
4. First time: also install the deck, `tusopen.apkg` from the Releases page →
   double-click or Anki ▸ File ▸ Import

### How it works
- Checks for a new release silently on profile startup
- When a new version exists, asks first, then downloads and opens the import dialog
- Notes are matched by permanent IDs, so re-importing never loses your
  review progress (card scheduling)

### Menu
In Anki: **Tools ▸ TUS Open**:
- **Güncellemeleri kontrol et**, manual update check
- **Kurulu sürüm**, shows the installed deck version

### Settings
`config.json`:
- `auto_check`, check on profile startup (default: on)
- `installed_version`, last version the add-on knows (managed automatically)

### FAQ

**Will re-importing wipe my progress?**
No. Cards are matched by permanent IDs; Anki updates changed cards and keeps
scheduling. New cards arrive as "new".

**Why does "Kurulu sürüm" say "yok"?**
You haven't imported the deck yet, install `tusopen.apkg` first.

**Does the add-on send personal data?**
No. It only makes read-only requests to the GitHub API; no account or identity
information is required.

### Reporting issues
https://github.com/aycibatuhan/tusopen/issues