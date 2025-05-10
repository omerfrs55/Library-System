# Smart Library Assistant - Akıllı Kütüphane Asistanı

## Project Overview - Proje Genel Bakış

The Smart Library Assistant is a console-based library management system for students and librarians. It allows book borrowing, returning, rating, and recommendations.

Akıllı Kütüphane Asistanı, öğrenciler ve kütüphaneciler için konsol tabanlı bir kütüphane yönetim sistemidir. Kitap ödünç alma, iade, puanlama ve öneri işlevleri sunar.

---

## Features - Özellikler

* User roles: Librarian and Student // Kullanıcı rolleri: Kütüphaneci ve Öğrenci
* Book borrowing and returning // Kitap ödünç alma ve iade
* Book rating after return // İade sonrası kitap puanlama
* Book recommendations by genre or rating // Tür veya puana göre kitap önerileri
* Student registration and book management // Öğrenci kaydı ve kitap yönetimi

---

## Installation - Kurulum

1. Clone the repository: // Depoyu klonlayın

```
git clone https://github.com/username/Library-System.git
```

2. Run the program: // Programı çalıştırın

```
python Library-System.py
```

---

## Usage - Kullanım

1. Choose your role: Librarian or Student

2. Follow the prompts to manage or borrow books

3. Rolünüzü seçin: Kütüphaneci veya Öğrenci

4. Kitapları yönetmek veya ödünç almak için yönlendirmeleri takip edin

---

## Functions - Fonksiyonlar

### getBook(userName)

Purpose: Borrow a book // Amaç: Kitap ödünç alma

#### Code Explanation - Kod Açıklaması

```python
clear()  # Clears the screen
books = readLines("books")  # Reads book list from file
```

1. `clear()`: Ekranı temizler.
2. `books = readLines("books")`: Kitap listesini dosyadan okur.

---

### deliverAbook()

Purpose: Return a book // Amaç: Kitap iadesi

#### Code Explanation - Kod Açıklaması

```python
clear()  # Clears the screen
ad = input("Your username: ")  # Takes username
```

1. `clear()`: Ekranı temizler.
2. `ad = input(...)`: Kullanıcı adını alır.

---

### librarianPanel()

Purpose: Manage books and students // Amaç: Kitap ve öğrenci yönetimi

#### Code Explanation - Kod Açıklaması

```python
clear()  # Clears the screen
print("\n🔐 Librarian Panel")  # Shows librarian panel title
```

1. `clear()`: Ekranı temizler.
2. `print(...)`: Kütüphaneci panel başlığını gösterir.

---

### readLines(file)

Purpose: Read data from a file // Amaç: Dosyadan veri okuma

#### Code Explanation - Kod Açıklaması

```python
with open(files[file], "r", encoding="utf-8") as f:
    return [line.strip() for line in f.readlines() if line.strip()]
```

1. Opens the file in read mode. // Dosyayı okuma modunda açar.
2. Reads and cleans each line. // Her satırı okur ve temizler.
3. Returns the list of cleaned lines. // Temizlenmiş satırların listesini döndürür.

---

### addToLine(file, data)

Purpose: Add data to a file // Amaç: Dosyaya veri ekleme

#### Code Explanation - Kod Açıklaması

```python
with open(files[file], "a", encoding="utf-8") as f:
    f.write(data + "\n")  # Adds data to the end
```

1. Opens the file in append mode. // Dosyayı ekleme modunda açar.
2. Adds the data at the end. // Veriyi sona ekler.

---

### userVerify(file, userName, password)

Purpose: Verify user credentials // Amaç: Kullanıcı bilgilerini doğrulama

#### Code Explanation - Kod Açıklaması

```python
for line in readLines(file):
    ad, pw = line.strip().split(",")
    if userName == ad and password == pw:
        return True
return False
```

1. Loops through users in the file. // Dosyadaki kullanıcıları döngüye alır.
2. Checks if the username and password match. // Kullanıcı adı ve şifre eşleşmesini kontrol eder.
3. Returns True if matched, False if not. // Eşleşirse True, değilse False döndürür.

---

### newBookID()

Purpose: Generate a unique book ID // Amaç: Benzersiz kitap ID oluşturma

#### Code Explanation - Kod Açıklaması

```python
books = readLines("books")
availableIDs = [int(book.split(",")[0]) for book in books]
return max(availableIDs, default=1000) + 1
```

1. Reads book IDs from the file. // Dosyadan kitap ID'lerini okur.
2. Finds the highest ID. // En yüksek ID'yi bulur.
3. Returns the next ID. // Sonraki ID'yi döndürür.

---

## License

MIT License

---
