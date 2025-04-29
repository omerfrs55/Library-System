import datetime

# Kullanıcı verileri (Users and passwords)
kutuphane_kullanicilari = {
    "admin": "1234"  # kütüphaneci (librarian)
}

ogrenciler = {
    "ayse": "2222",
    "mehmet": "3333"
}

kitaplar = []
kullanicilar = {}

def kitap_ekle():
    print("\n📘 Yeni Kitap Ekle")
    isim = input("Kitap adı: ")
    tur = input("Türü: ")
    sayfa = int(input("Sayfa sayısı: "))
    puan = float(input("Puan (1-10): "))
    sıra = input("Sıra (örn: A, B, C...): ")
    raf = int(input("Raf numarası: "))

    kitap = {
        "isim": isim,
        "tür": tur,
        "sayfa": sayfa,
        "puan": puan,
        "sıra": sıra,
        "raf": raf,
        "alındı": False
    }

    kitaplar.append(kitap)
    print("✅ Kitap eklendi.\n")

def kitaplari_goster():
    if not kitaplar:
        print("Kütüphanede kitap yok.\n")
        return

    print("\n📚 Tüm Kitaplar:")
    for i, k in enumerate(kitaplar, start=1):
        durum = "📕 Alındı" if k["alındı"] else "📗 Uygun"
        print(f"{i}. {k['isim']} | Tür: {k['tür']} | Puan: {k['puan']} | {durum} | Sıra: {k['sıra']} | Raf: {k['raf']}")
    print()

def kitap_oner():
    tur = input("Hangi türde kitap önerisi istersin?: ")
    uygunlar = [k for k in kitaplar if not k["alındı"] and k["tür"].lower() == tur.lower()]

    if not uygunlar:
        print("Bu türde uygun kitap bulunamadı.\n")
        return

    uygunlar.sort(key=lambda x: x["puan"], reverse=True)
    kitap = uygunlar[0]

    print(f"\n🎯 Önerilen kitap: {kitap['isim']} | Puan: {kitap['puan']}")
    print(f"📍 Konum: Sıra {kitap['sıra']} - Raf {kitap['raf']}\n")

def kitap_al(kullanici_adi):
    kitaplari_goster()
    secim = int(input("Almak istediğiniz kitabın numarası: "))

    if 1 <= secim <= len(kitaplar):
        kitap = kitaplar[secim - 1]

        if kitap["alındı"]:
            print("Bu kitap zaten alınmış.\n")
            return

        teslim_tarihi = datetime.date.today() + datetime.timedelta(weeks=2)
        kitap["alındı"] = True
        kullanicilar[kullanici_adi] = {
            "kitap": kitap["isim"],
            "teslim_tarihi": teslim_tarihi.strftime("%Y-%m-%d")
        }

        print(f"✅ '{kitap['isim']}' kitabı alındı.")
        print(f"📅 Son teslim tarihi: {teslim_tarihi.strftime('%Y-%m-%d')}\n")
    else:
        print("Geçersiz seçim.\n")

def kitap_takip():
    if not kullanicilar:
        print("Hiç kitap alınmamış.\n")
        return

    print("\n📋 Kitap Takip Listesi:")
    for kullanici, bilgi in kullanicilar.items():
        print(f"👤 {kullanici} → 📘 {bilgi['kitap']} | Teslim: {bilgi['teslim_tarihi']}")
    print()

def kitap_durum(kullanici_adi):
    if kullanici_adi in kullanicilar:
        bilgi = kullanicilar[kullanici_adi]
        print(f"\n📘 Şu an aldığınız kitap: {bilgi['kitap']}")
        print(f"📅 Teslim tarihi: {bilgi['teslim_tarihi']}\n")
    else:
        print("Henüz bir kitap almadınız.\n")

def ogrenci_ekle():
    print("\n👤 Yeni Öğrenci Kaydı")
    yeni_ad = input("Yeni öğrenci adı: ")
    if yeni_ad in ogrenciler:
        print("Bu kullanıcı zaten kayıtlı.\n")
        return
    sifre = input("Parola belirleyin: ")
    ogrenciler[yeni_ad] = sifre
    print("✅ Öğrenci kaydı yapıldı.\n")

def ogrenci_listesi():
    print("\n📋 Kayıtlı Öğrenciler:")
    for i, (isim, sifre) in enumerate(ogrenciler.items(), start=1):
        print(f"{i}. {isim} | Şifre: {sifre}")
    print()

def ogrenci_duzenle():
    ogrenci_listesi()
    ad = input("Düzenlemek istediğiniz öğrencinin adı: ")
    if ad not in ogrenciler:
        print("Bu isimde bir öğrenci yok.\n")
        return
    yeni_ad = input("Yeni isim (aynı kalacaksa aynı yazın): ")
    yeni_sifre = input("Yeni şifre (aynı kalacaksa aynı yazın): ")

    sifre = ogrenciler.pop(ad)
    ogrenciler[yeni_ad] = yeni_sifre
    print("✅ Bilgiler güncellendi.\n")

def kullanici_menu(kullanici_adi):
    while True:
        print(f"\n🧑 Kullanıcı: {kullanici_adi}")
        print("1. Kitapları Görüntüle")
        print("2. Kitap Önerisi Al")
        print("3. Kitap Al")
        print("4. Aldığım Kitabı Kontrol Et")
        print("5. Çıkış Yap")
        print("6. Programdan Tamamen Çık")

        secim = input("Seçiminiz: ")

        if secim == '1':
            kitaplari_goster()
        elif secim == '2':
            kitap_oner()
        elif secim == '3':
            kitap_al(kullanici_adi)
        elif secim == '4':
            kitap_durum(kullanici_adi)
        elif secim == '5':
            print("Çıkış yapılıyor...\n")
            break
        elif secim == '6':
            print("Programdan çıkılıyor...")
            exit()
        else:
            print("Geçersiz seçim.\n")

def giris_ekrani():
    while True:
        print("\n📚 Akıllı Kütüphane Asistanı")
        print("1. Kütüphaneci Girişi")
        print("2. Öğrenci Girişi")
        print("3. Çıkış")

        secim = input("Seçiminiz: ")

        if secim == '1':
            ad = input("Kütüphaneci adı: ")
            sifre = input("Parola: ")
            if kutuphane_kullanicilari.get(ad) == sifre:
                print("\n🛠️ Kütüphaneci Paneli")
                while True:
                    print("1. Kitap Ekle")
                    print("2. Kitapları Görüntüle")
                    print("3. Kitap Takibi")
                    print("4. Yeni Öğrenci Kaydı")
                    print("5. Öğrenci Listesi")
                    print("6. Öğrenci Bilgilerini Düzenle")
                    print("7. Geri Dön")
                    print("8. Programdan Çık")

                    alt_secim = input("Seçiminiz: ")
                    if alt_secim == '1':
                        kitap_ekle()
                    elif alt_secim == '2':
                        kitaplari_goster()
                    elif alt_secim == '3':
                        kitap_takip()
                    elif alt_secim == '4':
                        ogrenci_ekle()
                    elif alt_secim == '5':
                        ogrenci_listesi()
                    elif alt_secim == '6':
                        ogrenci_duzenle()
                    elif alt_secim == '7':
                        break
                    elif alt_secim == '8':
                        print("Programdan çıkılıyor...")
                        exit()
                    else:
                        print("Geçersiz seçim.\n")
            else:
                print("❌ Hatalı giriş.\n")

        elif secim == '2':
            ad = input("Kullanıcı adınız: ")
            sifre = input("Parolanız: ")
            if ad in ogrenciler and ogrenciler[ad] == sifre:
                kullanici_menu(ad)
            else:
                print("❌ Kullanıcı adı veya parola yanlış.\n")

        elif secim == '3':
            print("Programdan çıkılıyor...")
            break
        else:
            print("Geçersiz seçim.\n")

# Programı başlat
if __name__ == "__main__":
    giris_ekrani()
