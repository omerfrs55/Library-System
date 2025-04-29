# -*- coding: utf-8 -*-
import os  # İşletim sistemi ile ilgili işlemler için kullanılır
import time  # Bekleme ve zamanlama işlemleri için kullanılır
from datetime import datetime, timedelta  # Tarih ve zaman işlemleri için kullanılır

# Dosya yollarını belirtiyoruz. Her dosya verileri saklamak için kullanılır.
dosyalar = {
    "ogrenciler": "ogrenciler.txt",  # Öğrenci bilgileri
    "kitaplar": "kitaplar.txt",  # Kitap kayıtları
    "emanetler": "emanet_edilenler.txt",  # Emanet edilen kitaplar
    "teslimler": "teslim_edilenler.txt",  # Teslim edilen kitaplar
    "kutuphaneci": "kutuphaneci.txt" #Kütüphanecinin kullanıcı adı ve şifresi
}

# Yardımcı fonksiyonlar

def kitap_al(kullanici_adi):
    temizle()  # Ekranı temizler

    print("\n📖 Mevcut Kitaplar:\n")
    kitaplar = satirlari_oku("kitaplar")  # Kitaplar dosyasından veriler okunur

    if not kitaplar:  # Kitap listesi boşsa kullanıcıya bildirilir
        print("⚠️ Kitap listesi şu anda boş.")
        input("\nAna menüye dönmek için Enter'a basın...")
        return  # Fonksiyondan çıkılır

    for kitap in kitaplar:  # Kitaplar ekrana yazdırılır
        print(kitap)

    print("\n📥 Kitap Alma İşlemi")

    # Öğrenciden almak istediği kitap ID'si istenir
    kitap_id = input("Almak istediğiniz kitap ID'si: ")

    # Daha önce alınmış kitapları kontrol etmek için emanetler dosyası okunur
    emanetler = satirlari_oku("emanetler")

    # Aynı kitabın daha önce alınıp alınmadığını kontrol ederiz
    for satir in emanetler:
        ogrenci, kid, _, _ = satir.split(",")  # satır virgülle ayrılır
        if ogrenci == kullanici_adi and kid == kitap_id:
            print("\n⚠️ Bu kitabı zaten aldınız. Teslim etmeden tekrar alamazsınız.")
            input("\nAna menüye dönmek için Enter'a basın...")
            return  # Kitap alma işlemi iptal edilir

    # İstenilen kitap ID'sine sahip kitabı bulmak için arama yapılır
    secilen_kitap = None
    for kitap in kitaplar:
        parcalar = kitap.split(",")  # kitap verileri virgülle ayrılır
        if parcalar[0] == kitap_id:  # ID eşleşirse
            secilen_kitap = parcalar
            break  # kitap bulunduğunda döngüden çıkılır

    if not secilen_kitap:  # Eğer kitap bulunamazsa
        print("\n❌ Geçersiz kitap ID.")
        input("\nAna menüye dönmek için Enter'a basın...")
        return  # Fonksiyondan çıkılır

    # Kitap alma tarihi bugünün tarihi olarak alınır
    alis_tarihi = datetime.now().strftime("%Y-%m-%d")

    # Teslim tarihi kitap alındıktan 14 gün sonrası olarak hesaplanır
    teslim_tarihi = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

    # Kitap emanet kaydı oluşturulur: öğrenci adı, kitap ID, kitap adı, alış tarihi
    kayit = f"{kullanici_adi},{secilen_kitap[0]},{secilen_kitap[1]},{alis_tarihi}"
    satira_ekle("emanetler", kayit)  # emanet dosyasına kayıt eklenir

    # Kullanıcıya bilgi verilir
    print(f"\n✅ '{secilen_kitap[1]}' adlı kitap başarıyla alındı.")
    print(f"📅 Son teslim tarihi: {teslim_tarihi}")
    input("\nAna menüye dönmek için Enter'a basın...")

def temizle():
    os.system("cls" if os.name == "nt" else "clear")  # Windows için cls, diğerleri için clear ile ekranı temizler

def tarih_str():
    return datetime.now().strftime("%Y-%m-%d")  # Bugünün tarihini "yyyy-aa-gg" formatında döndürür

def dosya_var_mi():
    for dosya in dosyalar.values():
        if not os.path.exists(dosya):  # Eğer dosya yoksa oluştur
            open(dosya, "w", encoding="utf-8").close()

def satirlari_oku(dosya):
    with open(dosyalar[dosya], "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]  # Dosyadaki satırları temizleyip listeler

def satira_ekle(dosya, veri):
    with open(dosyalar[dosya], "a", encoding="utf-8") as f:
        f.write(veri + "\n")  # Dosyanın sonuna veri ekler

def satirlari_yaz(dosya, satirlar):
    with open(dosyalar[dosya], "w", encoding="utf-8") as f:
        f.write("\n".join(satirlar) + "\n")  # Dosyaya satırları yeniden yazar

# Kullanıcı adı ve şifre doğrulama işlemi (büyük küçük harf duyarlı)
def kullanici_dogrula(dosya, kullanici_adi, sifre):
    for satir in satirlari_oku(dosya):
        ad, pw = satir.split(",")
        if kullanici_adi == ad and sifre == pw:
            return True  # Kullanıcı bulunduysa True döndür
    return False

# Yeni kitap ID'si oluşturur (max veya str kullanılmadan)
def yeni_kitap_id():
    kitaplar = satirlari_oku("kitaplar")
    mevcut_idler = []
    for line in kitaplar:
        parcalar = line.split(",")
        if len(parcalar) > 0:
            id_kontrol = parcalar[0]
            if id_kontrol.isdigit():
                mevcut_idler.append(int(id_kontrol))
    yeni_id = 1001
    for id_num in mevcut_idler:
        if id_num >= yeni_id:
            yeni_id = id_num + 1
    return yeni_id  # En büyük ID bulunup 1 artırılır

# Kitap teslim işlemleri

def kitap_teslim_et():
    temizle()
    print("\n📚 Kitap Teslim Etme Ekranı")
    ad = input("Adınız: ")
    soyad = input("Soyadınız: ")
    ogr_adi = f"{ad} {soyad}"  # Ad ve soyadı birleştirerek öğrenci adı oluşturulur
    kitap_id = input("Teslim etmek istediğiniz kitap ID: ")
    bugun = datetime.now()  # Bugünün tarihi alınır

    emanetler = satirlari_oku("emanetler")
    yeni_emanetler = []
    teslim_edilen = False

    for satir in emanetler:
        ogr, kid, kitap_adi, alis_tarihi = satir.split(",")
        if ogr == ogr_adi and kid == kitap_id:
            teslim_edilen = True
            alis_dt = datetime.strptime(alis_tarihi, "%Y-%m-%d")
            fark = (bugun - alis_dt).days  # Kaç gün geçtiği hesaplanır
            gec_teslim = "GEÇ TESLİM" if fark > 14 else ""  # 14 günü geçtiyse "GEÇ TESLİM" yazılır
            teslim_kaydi = f"{ogr},{kid},{kitap_adi},{bugun.strftime('%Y-%m-%d')},{gec_teslim}"
            satira_ekle("teslimler", teslim_kaydi)  # Teslim kaydı dosyaya eklenir
        else:
            yeni_emanetler.append(satir)

    if teslim_edilen:
        satirlari_yaz("emanetler", yeni_emanetler)
        print("\n✅ Kitap teslim edildi!")
    else:
        print("\n⚠️ Bu kitap ID ile sizin adınıza kayıtlı emanet bulunamadı.")
    input("\nAna menüye dönmek için Enter'a basın...")

# Kütüphaneci paneli işlemleri

# Kütüphaneci paneli
def kutuphaneci_paneli():
    while True:
        temizle()  # Ekranı temizler
        print("\n🔐 Kütüphaneci Paneli")  # Kütüphaneci paneli başlığı
        print("1 - Kitap Ekle")  # Kitap ekleme seçeneği
        print("2 - Kitap Sil")  # Kitap silme seçeneği
        print("3 - Kitap Listesini Göster")  # Kitap listesini gösterme seçeneği
        print("4 - Emanet Edilen Kitapları Görüntüle")  # Emanet edilen kitapları gösterme seçeneği
        print("5 - Teslim Edilen Kitapları Görüntüle")  # Teslim edilen kitapları gösterme seçeneği
        print("6 - Öğrenci Kaydı Ekle")  # Öğrenci kaydetme seçeneği
        print("7 - Kayıtlı Öğrencileri Görüntüle")  # Kayıtlı öğrencileri gösterme seçeneği
        print("8 - Çıkış")  # Çıkış seçeneği
        secim = input("\nSeçiminiz: ")  # Kullanıcıdan seçim alır

        if secim == "1":
            kitap_adi = input("Kitap adı: ")  # Kitap adı girilir
            tur = input("Türü: ")  # Kitap türü girilir
            raf = input("Raf No: ")  # Kitap raf numarası girilir
            sira = input("Sıra No: ")  # Kitap sıra numarası girilir
            kitap_id = str(yeni_kitap_id())  # Yeni kitap ID'si oluşturulur
            kayit = f"{kitap_id},{kitap_adi},{tur},{raf},{sira}"  # Kitap bilgileri birleştirilir
            satira_ekle("kitaplar", kayit)  # Kitap bilgileri kitaplar.txt dosyasına eklenir
            print("\n✅ Kitap eklendi.")  # Başarılı ekleme mesajı
            input("Devam etmek için Enter...")  # Kullanıcıdan devam etmek için tuşlama beklenir

        elif secim == "2":
            kitaplar = satirlari_oku("kitaplar")  # Kitaplar.txt dosyasındaki kitaplar okunur
            if not kitaplar:  # Eğer kitaplar listesi boşsa
                print("\n⚠️ Kitap listesi boş.")  # Uyarı mesajı
            else:
                for k in kitaplar:  # Kitaplar listesi ekrana yazdırılır
                    print(k)
                silinecek_id = input("Silmek istediğiniz kitap ID: ")  # Silinecek kitap ID'si girilir
                kitaplar = [k for k in kitaplar if not k.startswith(silinecek_id + ",")]  # Silinecek kitap listeden çıkarılır
                satirlari_yaz("kitaplar", kitaplar)  # Güncellenmiş kitap listesi kitaplar.txt dosyasına yazılır
                print("\n✅ Kitap silindi.")  # Başarılı silme mesajı
            input("Devam etmek için Enter...")  # Kullanıcıdan devam etmek için tuşlama beklenir

        elif secim == "3":
            kitaplar = satirlari_oku("kitaplar")  # Kitaplar listesi okunur
            if not kitaplar:  # Eğer kitaplar listesi boşsa
                print("\n⚠️ Kitap listesi boş.")  # Uyarı mesajı
            else:
                for k in kitaplar:  # Kitaplar ekrana yazdırılır
                    print(k)
            input("Devam etmek için Enter...")  # Kullanıcıdan devam etmek için tuşlama beklenir

        elif secim == "4":
            emanetler = satirlari_oku("emanetler")  # Emanet kitaplar listesi okunur
            if not emanetler:  # Eğer emanetler listesi boşsa
                print("\n⚠️ Emanet edilen kitap bulunamadı.")  # Uyarı mesajı
            else:
                for e in emanetler:  # Emanet kitaplar ekrana yazdırılır
                    print(e)
            input("Devam etmek için Enter...")  # Kullanıcıdan devam etmek için tuşlama beklenir

        elif secim == "5":
            teslimler = satirlari_oku("teslimler")  # Teslim edilen kitaplar listesi okunur
            if not teslimler:  # Eğer teslimler listesi boşsa
                print("\n⚠️ Henüz teslim edilen kitap yok.")  # Uyarı mesajı
            else:
                for t in teslimler:  # Teslim edilen kitaplar ekrana yazdırılır
                    print(t)
            input("Devam etmek için Enter...")  # Kullanıcıdan devam etmek için tuşlama beklenir

        elif secim == "6":
            # Öğrenci kaydı eklemek
            ogrenci_adi = input("Öğrenci adı: ")  # Öğrenci adı girilir
            ogrenci_sifre = input("Öğrenci şifresi: ")  # Öğrenci şifresi girilir
            ogrenci_kaydi = f"{ogrenci_adi},{ogrenci_sifre}"  # Öğrenci bilgileri birleştirilir
            satira_ekle("ogrenciler", ogrenci_kaydi)  # Öğrenci bilgileri ogrenciler.txt dosyasına eklenir
            print("\n✅ Öğrenci kaydedildi.")  # Başarılı kayıt mesajı
            input("Devam etmek için Enter...")  # Kullanıcıdan devam etmek için tuşlama beklenir

        elif secim == "7":
            ogrenciler = satirlari_oku("ogrenciler")  # Kayıtlı öğrenciler dosyasını oku
            if not ogrenciler:  # Eğer öğrenci listesi boşsa
                print("\n⚠️ Öğrenci listesi boş.")  # Uyarı mesajı
            else:
                print("\nKayıtlı Öğrenciler:")  # Öğrenci listesi başlığı
                for ogrenci in ogrenciler:  # Öğrenciler listesi ekrana yazdırılır
                    print(ogrenci)
            input("Devam etmek için Enter...")  # Kullanıcıdan devam etmek için tuşlama beklenir

        elif secim == "8":
            break  # Panelden çıkış yapılır

        else:
            print("\n⚠️ Geçersiz seçim.")  # Geçersiz seçim uyarısı
            time.sleep(2)  # 2 saniye bekler ve kullanıcıyı tekrar menüye yönlendirir


# Ana programın başlangıç noktası
if __name__ == "__main__":
    dosya_var_mi()  # Gerekli dosyalar yoksa oluştur
    while True:
        temizle() # Önce ekranı temizle
        print("\n📚 Akıllı Kütüphane Asistanı", flush=True)
        print("1 - Kütüphaneci Girişi")
        print("2 - Öğrenci Girişi")
        print("3 - Çıkış")
        secim = input("\nSeçiminiz: ")

        if secim == "1":
            kullanici = input("Kütüphaneci adı: ")
            sifre = input("Şifre: ")
            if kullanici_dogrula("kutuphaneci", kullanici, sifre):
                kutuphaneci_paneli()
            else:
                print("\n❌ Hatalı giriş!")
                time.sleep(2)

        elif secim == "2":
            kullanici = input("Öğrenci adı: ")
            sifre = input("Şifre: ")
            if kullanici_dogrula("ogrenciler", kullanici, sifre):
                while True:
                    temizle()
                    print(f"\n👤 Hoşgeldin {kullanici}")
                    print("1 - Kitap Al")
                    print("2 - Kitap Teslim Et")
                    print("3 - Çıkış Yap")
                    secim_o = input("\nSeçiminiz: ")

                    if secim_o == "1":
                        kitap_al(kullanici)
                    elif secim_o == "2":
                        kitap_teslim_et()
                    elif secim_o == "3":
                        break
                    else:
                        print("\n⚠️ Geçersiz seçim.")
                        time.sleep(2)
            else:
                print("\n❌ Hatalı giriş!")
                time.sleep(2)

        elif secim == "3":
            print("\nÇıkılıyor...")
            time.sleep(1)
            break  # Programdan çıkış

        else:
            print("\n⚠️ Geçersiz seçim.")
            time.sleep(2)