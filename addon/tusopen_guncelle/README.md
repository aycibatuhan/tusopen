# TUS Open — Anki Güncelleme Eklentisi

Anki'nin **Araçlar ▸ TUS Open** menüsünden GitHub releases sayfasındaki en son
`tusopen.apkg` dosyasını bulur; yeni sürüm varsa indirip içe aktarma penceresini
açar. Notlar kalıcı kimliklerle eşleştiği için **zamanlama (scheduling) korunur**.

## Kurulum (elle)
1. `addon/tusopen_guncelle` klasörünü Anki eklenti klasörüne kopyalayın
   (Anki ▸ Araçlar ▸ Eklentiler ▸ Klasörü Göster).
2. Anki'yi yeniden başlatın — profil açılışında sessiz kontrol yapar.
3. İlk kurulumda: releases sayfasındaki `tusopen.apkg`'yi elle içe aktarın
   (eklenti sonraki güncellemeleri halleder).

## Ayarlar (config.json)
- `auto_check`: profil açılışında sessiz kontrol (varsayılan açık)
- `installed_version`: eklentinin bildiği son sürüm

## Not
İlk kurulumda deck hiç yoksa eklenti dosyayı indirir ve yolu gösterir;
Anki'nin içe aktarma penceresi sürüm farklarını güvenle yönetir.