# Anki ve Aralıklı Tekrar: Yeni Başlayanlar İçin Rehber

Bu rehber, TUS Open destesini ilk kez kullanacak olan ve Anki ya da
"aralıklı tekrar" kavramlarını hiç duymamış tıp öğrencileri için hazırlandı.
Amaç, sizi bir "Anki ustası" yapmak değil; sistemin mantığını anlamak ve
desteyi ilk günden doğru kullanmaya başlamak.

---

## 1. Anki nedir?

**Anki**, bilgisayar ve telefonunuzda çalışan, ücretsiz ve açık kaynaklı bir
*flashcard* (bilgi kartı) programıdır [1]. Temel fikir çok basit: Her kartın
bir **ön yüzü** (soru) ve bir **arka yüzü** (cevap) vardır.

Örnek bir kart:

- **Ön yüz:** "Kronik böbrek yetmezliğinde en sık görülen cilt bulgusu nedir?"
- **Arka yüz:** "Generalize pruritus (kaşıntı)"

Kartı gösterdiğinizde Anki önce soruyu gösterir, cevabı kafanızda
oluşturmanızı bekler, sonra da gerçek cevabı gösterir. Kendi cevabınızla
karşılaştırıp ne kadar iyi bildiğinizi Anki'ye söylersiniz (birazdan
göreceğiz) ve Anki bu kartı bir daha ne zaman göstermesi gerektiğine karar
verir.

### Neden flashcard? Neden sadece kitap okumayalım?

Bir kitabı ya da dersi **tekrar tekrar okumak** size "bunu biliyorum" hissi
verir — çünkü metin gözünüze tanıdık gelir. Ama TUS'ta karşınıza soru çıkar
ve sizden o bilgiyi **hatırlamanızı**, yani hafızanızdan dışarı çıkarmanızı
ister. Tanıdıklık ile hatırlama aynı şey değildir.

Flashcard'lar bizi tam tersini yapmaya zorlar: Cevap açık değilken cevabı
kafanızdan **üretmenizi** ister. Bu tekniğe *aktif hatırlama* (active recall)
denir ve pasif okumaya göre kalıcı öğrenmede çok daha etkilidir [5], [6].
Kısacası: Okurken kendinize "bunu biliyor muyum?" diye soran Anki'dir;
okurken kitap size cevabı sürekli fısıldar, Anki fısıldamaz.

### Hangi cihazlarda çalışır?

- **Bilgisayar (Windows, macOS, Linux):** Ücretsiz — [1]
- **Android (AnkiDroid):** Ücretsiz — [1]
- **iPhone/iPad (AnkiMobile):** Tek seferlik ücretli; bu ücret Anki'nin
  geliştirilmesini finanse eder (SSS'de açıklıyoruz) — [1]
- **AnkiWeb:** Tüm cihazlar arasında kartlarınızı ücretsiz senkronize eden
  Anki'nin bulut servisi [2]

Telefonunuzdan ve bilgisayarınızdan aynı hesapla AnkiWeb'e bağlanırsanız,
kartlarınız ve tekrar geçmişiniz her yerde güncel kalır.

---

## 2. Aralıklı tekrar (spaced repetition) nedir?

### Unutma eğrisi

1885'te Hermann Ebbinghaus, kendi üzerinde yaptığı deneylerle hafızanın
çalışma biçimini ilk kez bilimsel olarak ölçtü [3]. Bulduğu tablo bugün
*unutma eğrisi* olarak bilinir: Yeni öğrenilen bir bilgi, öğrenildikten
sonraki ilk günlerde çok hızlı unutulur; hatırlamayı başardığınız her tekrar
ise eğrisi "düzleştirir", yani bilgi hafızada daha uzun süre kalır.

Bunun pratik sonucu şu: **Bir bilgiyi tam unutmak üzereyken tekrar etmek,
onun en verimli tekrar anıdır.** Çok erken tekrar ederseniz (zaten hatırlıyorsunuz)
vakit kaybedersiniz; çok geç tekrar ederseniz bilgiyi neredeyse sıfırdan öğrenirsiniz.

### Anki bunu nasıl kullanır?

Anki, her kart için tekrar zamanını sizin adınıza optimize eder. Mekanizma şöyle:

1. Bir kart gösterilir, cevabı kafanızda oluşturursunuz.
2. Cevabı görürsünüz ve ne kadar hatırladığınızı **dört düğmeden** biriyle
   Anki'ye bildirirsiniz:
   - **Geri çekil (Again):** "Hatırlamadım." Kart kısa süre sonra tekrar gelir.
   - **Zor (Hard):** "Zorlukla hatırladım." Kısa bir aradan sonra gelir.
   - **İyi (Good):** "Normal bir şekilde hatırladım." Standart aralık.
   - **Kolay (Easy):** "Bunu ezbere biliyorum." Uzun bir aradan sonra gelir.
3. Anki, kartı her başarılı tekrarınızda **giderek büyüyen aralıklarla**
   gösterir. Örneğin düzgün cevapladığınız bir kart önce 1 gün sonra,
   sonra 3 gün, 1 hafta, 2 hafta, 1 ay... diye zamanlanır. Bir kartı ne kadar
   uzun süredir hatırlıyorsanız, bir sonraki tekrar aralığı o kadar uzar.

Kısacası Anki'nin tek amacı şudur: **Unutmak üzere olduğunuz kartı tam da
o anda karşınıza getirmek.** Bildiğiniz kartlara zaman harcamaz, zor
geldiğiniz kartlara ise daha sık döner. Bu "aralıklarla tekrar" yaklaşımının
etkisi, yüzlerce deneyi bir araya getiren meta-analizlerle (birçok çalışmanın
istatistiksel olarak birleştirilmesiyle hazırlanan araştırma türü) defalarca
doğrulanmıştır: Öğrenmeyi tek seferde yoğun yapmak (ezberci "son gece"
çalışması) yerine zamana yaymak, uzun süreli hatırlamada belirgin şekilde
daha iyidir [4].

---

## 3. Bilimsel dayanağı var mı?

Evet, bu alanın köklü bir araştırma geçmişi var. Başlıca bulgular:

- **Aralıklı tekrar (spacing effect / distributed practice):** Cepeda ve
  arkadaşları 2006'da 317 deneyi birleştiren bir meta-analiz yayımladı;
  sonuç netti: Öğrenmeyi zamana yaymak, tek oturumda toplamakla kıyaslanamayacak
  kadar daha kalıcı hatırlama sağlıyor. Ayrıca kritik bir detay: Tekrar
  aralığını ne kadar genişletebileceğiniz, bilgiyi ne kadar uzun süre
  hatırlamak istediğinize bağlı — uzun vadeli hedefler (TUS gibi) için
  daha geniş aralıklar daha iyi sonuç veriyor [4].

- **Test etkisi (testing effect / retrieval practice):** Roediger ve Karpicke
  2006'da gösterdiler ki, aynı sürede metni tekrar tekrar okuyan öğrenciler
  ilk testte iyi görünse de, bir hafta sonra en çok hatırlayanlar kendini
  *test eden* öğrenciler oldu [5]. Karpicke ve Roediger bunu 2008'de
  *Science* dergisinde bir adım öteye taşıdı: Bir bilgiye doğru cevap
  verdikten sonra o bilgiyi daha fazla **test etmemek** (sadece tekrar
  okumak), hatırlamayı dramatik biçimde düşürüyordu. Yani kalıcı öğrenmenin
  anahtarı doğru cevabı vermekten değil, hatırlama *alıştırmasını*
  sürdürmekten geçiyordu [6]. Flashcard kullanmak tam da budur.

- **Tıp eğitiminde kanıtı var mı?** Var. Maye ve Hurley'in 2026 tarihli
  sistematik derlemesi ve meta-analizi, tıp eğitiminde aralıklı tekrarın
  (Anki dahil) standart çalışma yöntemlerine kıyasla objektif sınav
  performansında anlamlı bir iyileşme sağladığını gösterdi: 21.415 öğrenciyi
  kapsayan analizde etki büyüklüğü belirgin şekilde lehte bulundu [7].
  Tıp fakültesi öğrencileriyle yapılan kohort çalışmalarında da Anki
  kullanımı ve akademik performans arasında pozitif bir ilişki rapor
  edilmiştir; özellikle **erken başlayan ve düzenli kullanan** öğrencilerde
  sınav sonuçlarının daha yüksek olduğu gözlenmiştir [8].

Uygar bir özet: Anki bir "hile" ya da trend değil; onlarca yıldır
doğrulanmış iki temel öğrenme ilkesini (aralıklı tekrar + aktif hatırlama)
sizin için otomatikleştiren bir araçtır [2], [4], [5], [6].

---

## 4. TUS Open destesini nasıl kullanmalıyım?

### Günlük rutin

En iyi rutin, her gün sürdürebildiğiniz rutindir. Önerdiğimiz başlangıç:

- **Günde 20-30 yeni kart** açın (Anki'de "yeni kart" = daha önce hiç
  görmediğiniz kart). Bu, destenin tamamını yavaş ama sağlam bir şekilde
  işlemenizi sağlar.
- **Günde 15-20 dakika** tekrar yapın. Yeni kartlar dahil günlük yükünüz
  genelde bu süreyi aşmaz.
- **Her gün çalışın, en azından 10 dakika.** Aralıklı tekrarın gücü
  düzenlilikten gelir: Günde 20 dakikalık 60 gün, 200 dakikalık 6 günden
  çok daha etkilidir. Tek büyük seansla "şok çalışma" yapmak, unutma
  eğrisine karşı kaybedilen bir savaştır [3], [4].

Yeni kart sayısını kendinize göre ayarlayın: Zamanınız kısıtlıysa 10'a
düşürün; sınav takvimi ve günlük tekrar yükü gözeterek artırın. Unutmayın:
Açtığınız her yeni kart, ileride her gün tekrar listesine bir "borç" ekler.
Şimdiği 100 kart, önümüzdeki haftalardaki her günün yükü demektir — bu
yüzden akşam kafasıyla "bugün 300 kart açayım" tuzağına düşmeyin.

### Etiketlerle konuya göre filtreleme

Destedeki her kart, ders hiyerarşisini izleyen etiketlerle gelir:

```text
TUS_v1::Ders::Kardiyoloji::İskemik kalp hastalıkları
TUS_v1::Ders::Farmakoloji::Antibiyotikler
```

Anki'nin kart tarayıcısında (Browse) `tag:` aramasıyla belirli bir dersi
veya konuyu filtreleyebilirsiniz. Örneğin yalnızca Kardiyoloji kartlarını
görmek istiyorsanız `tag:TUS_v1::Ders::Kardiyoloji` yazmanız yeterli.
Bu, sınav öncesi belirli bir konuya odaklanmak ya da zayıf hissettiğiniz
bir dersi ağırlıklandırmak için kullanışlıdır.

### "Sıklık" rozetini kullanın

Bazı kartlarda **"Son 20 sınavda N kez"** şeklinde bir rozet görürsünüz.
Bu, kartın konusunun gerçek TUS sınavlarının son 20 oturumunda kaç soruda
karşınıza çıktığını gösterir:

- **N yüksekse** (örn. 15+): Bu konu sınavın "ekmeği" demektir. Kaçırırsanız
  puan kaybı büyüktür — bu kartları asla atlarken düşünmeyin bile.
- **N düşükse:** Konu yine değerlidir ama zamanınız kısıtlıysa öncelik
  sıralamanızda daha aşağıda durabilir.

### Kart tipleri

Destede üç temel kart tipi vardır:

- **Bilgi:** Doğrudan bilgi kartları. "En sık görülen ... nedir?" tarzı.
  Konunun temel taşlarını oluşturur.
- **Vaka:** Kısa hasta öyküsü sunan klinik senaryo kartları. TUS'ta soruların
  büyük bölümü vaka formatında geldiği için, bilgiyi "hasta karşısında"
  kullanmayı alıştırır.
- **Ayırıcı:** Birbirine benzeyen hastalıkları, ilaçları ya da bulguları
  **ayırt etmeyi** test eden kartlar. "X'i Y'den ayıran en belirgin bulgu
  nedir?" tarzı. TUS'ta çeldiricilerle savaşmanın en büyük silahı budur.

### Altın kurallar

1. **Gün atlamayın.** Arada bir gün kaçarsa paniklemeyin, ertesi gün devam
   edin — ama bunu alışkanlık yapmayın. Anki'nin görev listesi ertelenen
   tekrarlarla şişer ve motivasyon düşer.
2. **"Geri çekil"i dürüst kullanın.** Cevabı "falan filan bir şeydi" diye
   hatırlıyorsanız bu "İyi" değildir. Kendinizi kandırırsanız, Anki kartı
   çok erken uzun aralığa bırakır ve sınavda kaybedersiniz. Zorluk duygunuz
   algoritmaya girdi (input) — temiz girdi, temiz sonuç verir.
3. **Hatalı kartları askıya alın.** Bir kartta içerik hatası bulursanız,
   onu tekrar etmeye devam etmeyin: Kart tarayıcısında seçip askıya alın
   (Suspend) ve depoya bir issue açın. Hatalı bilgiyi yüzlerce kez tekrar
   etmek, onu çok iyi öğrenmenize neden olur — istemediğimiz şey tam olarak bu.
4. **Sınav öncesi "Özel Çalışma" kullanın.** Anki'nin Custom Study /
   Özel Çalışma özelliğiyle belirli bir etiketin kartlarını normal programın
   dışına çıkıp yoğun tekrar edebilirsiniz. Örneğin sınavdan bir hafta önce
   `tag:TUS_v1::Ders::Çocuk Sağlığı` filtresiyle özel bir çalışma oturumu
   açabilirsiniz. Ancak bunu destek olarak kullanın; günlük rutinin yerine değil.
5. **Anlamadan kart açmayın.** Bilmediğiniz bir konunun kartlarını ezberlemeye
   çalışmak, Almanca bilmeyen birinin Almanca tarih kitabını ezberlemesi
   gibidir [9]. Önce konuyu bir kaynaktan okuyun, sonra kartlarla pekiştirin.
   Kartlar bilgiyi *tutmaya* yarar; *ilk kez anlamaya* değil.

---

## 5. SSS

**iOS uygulaması (AnkiMobile) neden ücretli?**
Anki'nin bilgisayar sürümü, AnkiWeb ve Android sürümü (AnkiDroid) ücretsizdir.
Yalnızca resmî iPhone/iPad uygulaması AnkiMobile tek seferlik bir ücretle
satılır; çünkü Anki'nin sunucuları ve geliştirilmesi maliyetlidir ve bu
uygulama, projenin ana gelir kaynağıdır [1]. Apple, uygulama içi satışlarda
geliştiriciden komisyon aldığı için Android'de olan ücretsiz model iOS'ta
sürdürülemez. Ücreti ödeyemiyorsanız AnkiWeb'i mobil tarayıcıdan kullanabilir
ya da kartlarınızı AnkiDroid ile senkronize edebilirsiniz.

**Her gün kaç yeni kart açmalıyım?**
Başlangıç için günde 20-30 yeni kart idealdir. Kural şu: Yeni kart sayısını
belirlerken, o kartların yaratacağı **gelecekteki tekrar yükünü** hesaba katın.
Günde 30 yeni kart + gelen tekrarlar genelde 20-30 dakikaya denk gelir ve
sürdürülebilirdir. Günlük yükünüz dayanılmaz hale geldiyse yeni kart sayısını
geçici olarak düşürün; tekrarları asla devre dışı bırakmayın.

**Kartı yanlış bilmek kötü mü?**
Hayır — tam tersine, sistemin çalışma şekli budur. "Geri çekil" dediğiniz
kart kısa süre sonra tekrar gelir; bu, algoritmanın tam olarak yapması
gereken işi yapması demektir [4], [6]. Yanlış bildiğiniz her kart, zamanınızın
tam da doğru yere harcandığının işaretidir. Yanlış bilmekten utanıp "İyi"ye
basmak ise asıl kayıptır: Kart unutulma sınırında kalmaya devam eder.

**TUS'a X ay kaldı, geç mi?**
Geç değil. Aralıklı tekrar her zaman diliminde çalışır; ne kadar süre
kaldığınız, yalnızca nasıl kullanacağınıza etki eder. Süreniz uzunsa tüm
desteyi günlük rutinle işleyebilirsiniz; kısa ise sıklık rozeti yüksek olan
konulara öncelik verin ve günde 10-15 yeni kartla bile başlayın. En kötü
seçenek, "geç olduğu için hiç başlamamak"tır: Bugün açtığınız 10 kart,
sınav günü hatırlayacağınız 10 kart demektir.

---

## Kaynaklar

1. Anki. *Anki — powerful, intelligent flashcards* (resmî site; sürümler,
   platformlar ve fiyatlandırma bilgisi). https://apps.ankiweb.net/
2. Anki. *Anki Manual* (resmî kullanım kılavuzu). https://docs.ankiweb.net/
3. Ebbinghaus, H. (1885). *Memory: A contribution to experimental psychology*
   (Über das Gedächtnis; H. A. Ruger ve C. E. Bussenius çevirisi, 1913).
   New York: Teachers College, Columbia University.
   https://archive.org/details/memorycontributi00ebbiuoft
4. Cepeda, N. J., Pashler, H., Vul, E., Wixted, J. T., ve Rohrer, D. (2006).
   Distributed practice in verbal recall tasks: A review and quantitative
   synthesis. *Psychological Bulletin, 132*(3), 354-380.
   https://doi.org/10.1037/0033-2909.132.3.354
5. Roediger, H. L., ve Karpicke, J. D. (2006). Test-enhanced learning:
   Taking memory tests improves long-term retention. *Psychological
   Science, 17*(3), 249-255.
   https://doi.org/10.1111/j.1467-9280.2006.01693.x
6. Karpicke, J. D., ve Roediger, H. L. (2008). The critical importance of
   retrieval for learning. *Science, 319*(5865), 966-968.
   https://doi.org/10.1126/science.1152408
7. Maye, J. A., ve Hurley, F. (2026). The effectiveness of spaced repetition
   in medical education: A systematic review and meta-analysis.
   *The Clinical Teacher, 23*(2), e70353.
   https://doi.org/10.1111/tct.70353
8. Gilbert, M. M., Frommeyer, T. C., Brittain, G. V., Stewart, N. A.,
   Turner, T. M., Stolfi, A., ve Parmelee, D. (2023). A cohort study
   assessing the impact of Anki as a spaced repetition tool on academic
   performance in medical school. *Medical Science Educator, 33*(4),
   955-962. https://doi.org/10.1007/s40670-023-01826-8
9. Wozniak, P. A. (1999). *Effective learning: Twenty rules of formulating
   knowledge*. SuperMemo.
   https://www.supermemo.com/en/blog/twenty-rules-of-formulating-knowledge
