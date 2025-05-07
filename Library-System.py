# -*- coding: utf-8 -*-
import os  # Used for operations related to the operating system // İşletim sistemi ile ilgili işlemler için kullanırız
import time  # Used for waiting and timing operations // Bekleme ve zamanlama işlemleri için kullanırız
from datetime import datetime, timedelta  # Used for date and time operations // Tarih ve zaman işlemleri için kullanırız

# We specify the file paths. Each file is used to store data. // Dosya yollarını belirtiyoruz. Her dosya verilerimizi saklamak için kullanıyoruz
files = {
    "students": "students.txt",  # Student information // Öğrenci bilgileri
    "books": "books.txt",  # Book records // Kitap kayıtları
    "entrust": "entrust.txt",  # Books entrusted // Emanet edilen kitaplar
    "delivered": "delivered.txt",  # Delivered books // Teslim edilen kitaplar
    "librarian": "librarian.txt", #Librarian's username and password // Kütüphanecinin kullanıcı adı ve şifresi
    "score": "scores.txt" #book scores for recommendation // kitap puanları öneri için
}

# Our auxiliary functions // Yardımcı fonksiyonlarımız

def getBook(userName):
    clear()  # Cleans the screen // Ekranı temizler

    print("\n📖 Available Books:\n")
    books = readLines("books")  # Data is read from the books file // Kitaplar dosyasından veriler okunur

    if not books:  # If the book list is empty, the user is notified // Kitap listesi boşsa kullanıcıya bildirilir
        print("⚠️ The book list is currently empty.")
        input("\nPress Enter to return to the main menu...")
        return  # The function is exited // Fonksiyondan çıkılır

        # Check if the user already has a book // Kullanıcının zaten kitabı var mı kontrolü
    entrust = readLines("entrust")
    for line in entrust:
        student, _, _, _ = line.split(",")
        if student == userName:
            print("\n⚠️ You have already got a book. You must return the current book first.")
            input("\nPress Enter to return to the main menu...")
            return

    for book in books:  # Books are printed on the screen // Kitaplar ekrana yazdırılır
        print(book)

    print("\n📥 Book Getting Process")

    # The student is asked for the book ID he/she wants to get. // Öğrenciden almak istediği kitap ID'si istenir
    bookID = input("Book ID you want to get: ")

    # The relics file is read to check previously acquired books // Daha önce alınmış kitapları kontrol etmek için emanetler dosyası okunur
    entrust = readLines("entrust")

    # We check if the same book has been purchased before // Aynı kitabın daha önce alınıp alınmadığını kontrol ederiz
    for line in entrust:
        student, kid, _, _ = line.split(",")  # line separated by commas // satır virgülle ayrılır
        if student == userName and kid == bookID:
            print("\n⚠️ You've already got this book. You can't get it again without returning it.")
            input("\nPress Enter to return to the main menu...")
            return  # Book purchase is cancelled // Kitap alma işlemi iptal edilir

    # A search is performed to find the book with the desired book ID // İstenilen kitap ID'sine sahip kitabı bulmak için arama yapılır
    chosenBook = None
    for book in books:
        pieces = book.split(",")  # book data is separated by commas // kitap verileri virgülle ayrılır
        if pieces[0] == bookID:  # If ID matches // ID eşleşirse
            chosenBook = pieces
            break  # When the book is found the loop is exited // kitap bulunduğunda döngüden çıkılır

    if not chosenBook:  # If the book is not found // Eğer kitap bulunamazsa
        print("\n❌ Invalid book ID.")
        input("\nPress Enter to return to the main menu...")
        return  # The function is exited // Fonksiyondan çıkılır

    # The book purchase date is taken as today's date // Kitap alma tarihi bugünün tarihi olarak alınır
    gettingDate = datetime.now().strftime("%Y-%m-%d")

    # Delivery date is calculated as "14" days after the book is received. // Teslim tarihi kitap alındıktan "14" gün sonrası olarak hesaplanır
    deadline = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

    # Book deposit record is created: student username, book ID, book name, purchase date // Kitap emanet kaydı oluşturulur: öğrenci kullanıcı adı, kitap ID, kitap adı, alış tarihi
    registry = f"{userName},{chosenBook[0]},{chosenBook[1]},{gettingDate}"
    addToLine("entrust", registry)  # Record added to escrow file // emanet dosyasına kayıt eklenir

    # The user is informed // Kullanıcıya bilgi verilir
    print(f"\n✅ '{chosenBook[1]}' ")
    print(f"📅 Deadline: {deadline}")
    input("\nPress Enter to return to the main menu...")

def clear():
    os.system("cls" if os.name == "nt" else "clear")  # Clears the screen with cls for Windows and clear for others // Windows için cls, diğerleri için clear ile ekranı temizler

def tarih_str():
    return datetime.now().strftime("%Y-%m-%d")  # Returns today's date in "yyyy-mm-dd" format // Bugünün tarihini "yyyy-aa-gg" formatında döndürür

def isFileExistent(): # dosya var mi ?
    for file in files.values():
        if not os.path.exists(file):  # If file does not exist, create it // Eğer dosya yoksa oluştur
            open(file, "w", encoding="utf-8").close()

def readLines(file):
    with open(files[file], "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]  # Clears and lists lines in a file // Dosyadaki satırları temizleyip listeler

def addToLine(file, data):
    with open(files[file], "a", encoding="utf-8") as f:
        f.write(data + "\n")  # Appends data to the end of the file // Dosyanın sonuna veri ekler

def writeLines(file, lines):
    with open(files[file], "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")  # Rewrites lines to file // Dosyaya satırları yeniden yazar

# Username and password verification process (case sensitive) // Kullanıcı adı ve şifre doğrulama işlemi (büyük küçük harf duyarlı)
def userVerify(file, userName, password):
    for line in readLines(file):
        ad, pw = line.split(",")
           # Comparison ignoring spaces and case insensitive // Boşlukları yok sayarak ve büyük/küçük harf duyarsız karşılaştırma
        if (userName.replace(" ", "").lower() == userName.replace(" ", "").lower()
            and password == pw):
            return True
    return False


# Creates new book ID // Yeni kitap ID'si oluşturur
def newBookID():
    books = readLines("books")
    availableIDs = []
    for line in books:
        pieces = line.split(",")
        if len(pieces) > 0:
            idCheck = pieces[0]
            if idCheck.isdigit():
                availableIDs.append(int(idCheck))
    newID = 1001
    for id_num in availableIDs:
        if id_num >= newID:
            newID = id_num + 1
    return newID  # The largest ID is found and increased by 1

# Book delivery procedures // Kitap teslim işlemleri
# Adding rating system to book return function // Kitap teslim fonksiyonuna puanlama sistemini ekliyoruz
def deliverAbook():
    clear()
    print("\n📚 Book Delivery Screen")
    ad = input("Your username: ")
    stuName = f"{ad}"
    bookID = input("Book ID you want to deliver: ")
    today = datetime.now()

    entrust = readLines("entrust")
    newEntrust = []
    delivered = False

    for line in entrust:
        stu, kid, bookName, gettingDate = line.split(",")
        if stu == stuName and kid == bookID:
            delivered = True
            alis_dt = datetime.strptime(gettingDate, "%Y-%m-%d")
            fark = (today - alis_dt).days
            lateDelivery = "LATE DELIVERY" if fark > 14 else ""
            deliveryRecord = f"{stu},{kid},{bookName},{today.strftime('%Y-%m-%d')},{lateDelivery}"
            addToLine("delivered", deliveryRecord)

            # Find book category // Kitap kategorisini bul
            books = readLines("books")
            category = "Unknown"
            for book in books:
                parts = book.split(",")
                if parts[0] == kid and len(parts) >= 3:
                    category = parts[2]
                    break

            # Get rating between 1-10 // 1-10 arası puan al
            print(f"\n📝 '{bookName}' rate the book")
            while True:
                try:
                    score = int(input("Give a score of 1-10 (1=Very Bad, 10=Very Good): "))
                    if 1 <= score <= 10:
                        scoreRecord = f"{kid},{bookName},{stuName},{score},{category}"
                        addToLine("score", scoreRecord)
                        print("\n✅ Your score has been saved!")
                        break
                    else:
                        print("⚠️ Please enter a value between 1-10!")
                except ValueError:
                    print("⚠️ Invalid entry! Please enter a number.")
        else:
            newEntrust.append(line)

    if delivered:
        writeLines("entrust", newEntrust)
        print("\n✅ The book has been delivered!")
    else:
        print("\n⚠️ No entrust was found registered in your name with this book ID.")
    input("\nPress Enter to return to the main menu...")

# Read and calculate book ratings // Kitap puanlarını okur ve hesaplar
# Function to read book ratings // Kitap puanlarını okuyan fonksiyon
def readBookScores():
    score = readLines("score")
    scores = {}

    for line in score:
        if line:
            parts = line.split(",")
            if len(parts) >= 4:  # At least 4 info required // En az 4 bilgi olmalı
                kid = parts[0]
                bookName = parts[1]
                score = parts[3]
                category = parts[4] if len(parts) > 4 else "Unknown"

                if kid not in scores:
                    scores[kid] = {
                        'bookName': bookName,
                        'category': category,
                        'totalScore': 0,
                        'numberOfPoints': 0,
                        'average': 0
                    }

                # Rating calculations Puan hesaplamaları
                scores[kid]['totalScore'] += int(score)
                scores[kid]['numberOfPoints'] += 1
                scores[kid]['average'] = scores[kid]['totalScore'] / scores[kid]['numberOfPoints']

    return scores

# Find categories of books student read // Öğrencinin okuduğu kitapların kategorilerini bul
def student_reading_history(student_name):
    entrust = readLines("entrust")
    delivered = readLines("delivered")
    books = readLines("books")

    # Book ID - category mapping // Kitap ID - kategori eşleştirme
    bookCategories = {}
    for book in books:
        parts = book.split(",")
        if len(parts) >= 3:  # ID, Name, Category // ID, Ad, Kategori
            bookCategories[parts[0]] = parts[2]

    readCategories = set()

    # Check borrowed and returned books // Emanet ve teslim edilen kitapları kontrol et
    for registry in entrust + delivered:
        if student_name in registry:
            bookID = registry.split(",")[1]
            if bookID in bookCategories:
                readCategories.add(bookCategories[bookID])

    return list(readCategories)


# Book recommendation function // Kitap öneri fonksiyonu
def showBookSuggestions(userName):
    clear()
    print("\n📊 Book Recommendations")

    score = readBookScores()
    if not score:
        print("\n⚠️ Not enough ratings have been made yet.")
        input("\nPress Enter to return to the main menu...")
        return

    # Filtering options // Filtreleme seçenekleri
    print("\n🔍 Filtering Options:")
    print("1 - Score + Genre (The highest rated of the genres you read)")
    print("2 - Only Score (Highest scores in all books)")
    print("3 - All Books (All books including Unrated)")
    print("4 - Genre Selection (All books in a certain genre)")

    choice = input("\nYour filtering choice (1-4): ")

    if choice == "1":  # Points + Type // Puan + Tür
        readCategories = student_reading_history(userName)

        if not readCategories:
            print("\n⚠️ You don't have any reading history yet.")
            input("\nPress Enter to return to the main menu...")
            return

        print("\n🚀 Highest rated books in the genres you read:")

        # Group books by categories // Kitapları kategorilere göre grupla
        booksCategorized = {}
        for kid, book in score.items():
            category = book['category']
            if category not in booksCategorized:
                booksCategorized[category] = []
            booksCategorized[category].append(book)

        for category in readCategories:
            if category in booksCategorized:
                # Sorting with Bubble Sort // Bubble Sort ile sıralama
                books = booksCategorized[category]
                n = len(books)
                swapDone = True

                for i in range(n-1):
                    if not swapDone:
                        break
                    swapDone = False

                    for k in range(0, n-i-1):
                        if books[k]['average'] < books[k+1]['average']:
                            books[k], books[k+1] = books[k+1], books[k]
                            swapDone = True

                print(f"\n📚 {category} Category:")
                for i in range(min(3, len(books))):
                    book = books[i]
                    print(f"{i+1}. {book['bookName']} - ⭐ {book['average']:.1f}")

    elif choice == "2":  # Just Points // Sadece Puan
        print("\n🌟 Highest Rated in All Books:")

        allBooks = list(score.values())

        # Sorting with Bubble Sort // Bubble Sort ile sıralama
        n = len(allBooks)
        swapDone = True

        for i in range(n-1):
            if not swapDone:
                break
            swapDone = False

            for k in range(0, n-i-1):
                if allBooks[k]['average'] < allBooks[k+1]['average']:
                    allBooks[k], allBooks[k+1] = allBooks[k+1], allBooks[k]
                    swapDone = True

        for i in range(min(10, len(allBooks))):
            book = allBooks[i]
            print(f"{i+1}. {book['bookName']} - ⭐ {book['average']:.1f} - {book['category']}")

    elif choice == "3":  # All Books // Tüm Kitaplar
        print("\n📚 All Books (Including Unrated):")

        allBooks = readLines("books")
        ratedBooks = [book['bookName'] for book in score.values()]

        for i, book in enumerate(allBooks, 1):
            parts = book.split(",")
            bookName = parts[1] if len(parts) > 1 else "Unknown"
            durum = "⭐ With Points" if bookName in ratedBooks else "📖 Without Points"
            print(f"{i}. {bookName} - {durum}")

    elif choice == "4":  # Type Selection // Tür Seçimi
        print("\n📂 Mevcut Türler:")

        # List all types // Tüm türleri listele
        books = readLines("books")
        allKinds = set()

        for book in books:
            parts = book.split(",")
            if len(parts) > 2:
                allKinds.add(parts[2])

        for i, kind in enumerate(sorted(allKinds), 1):
            print(f"{i}. {kind}")

        kindSelection = input("\nType number you want to display: ")

        try:
            kindSelection = int(kindSelection)
            chosenKind = sorted(allKinds)[kindSelection-1]

            print(f"\n📚 {chosenKind} books in Kinds:")

            # Show rated books // Puanlı kitapları göster
            ratedBooks = []
            for kid, book in score.items():
                if book['category'] == chosenKind:
                    ratedBooks.append(book)

            if ratedBooks:
                print("\n⭐ Books with Points:")
                for i, book in enumerate(ratedBooks, 1):
                    print(f"{i}. {book['bookName']} - ⭐ {book['avarage']:.1f}")

            # Show unrated books // Puansız kitapları göster
            scorelessBooks = []
            for book in books:
                parts = book.split(",")
                if len(parts) > 2 and parts[2] == chosenKind:
                    bookName = parts[1]
                    if not any(k['bookName'] == bookName for k in ratedBooks):
                        scorelessBooks.append(bookName)

            if scorelessBooks:
                print("\n📖 Books without scores:")
                for i, book in enumerate(scorelessBooks, 1):
                    print(f"{i}. {book}")

            if not ratedBooks and not scorelessBooks:
                print("\n⚠️ No books found in this genre.")

        except (ValueError, IndexError):
            print("\n⚠️ Invalid type selection!")

    else:
        print("\n⚠️ Invalid selection!")

    input("\nPress Enter to return to the main menu...")
# Librarian panel operations //Kütüphaneci paneli işlemleri

# Librarian panel // Kütüphaneci paneli
def librarianPanel():
    while True:
        clear()  # Cleans the screen // Ekranı temizler
        print("\n🔐 Librarian Panel")  # Librarian panel title // Kütüphaneci paneli başlığı
        print("1 - Add Book")  # Option to add books // Kitap ekleme seçeneği
        print("2 - Delete Book")  # Book delete option // Kitap silme seçeneği
        print("3 - Show Book List")  # Option to show book list // Kitap listesini gösterme seçeneği
        print("4 - View Entrusted Books")  # Option to show deposited books // Emanet edilen kitapları gösterme seçeneği
        print("5 - View Delivered Books")  # Option to show delivered books // Teslim edilen kitapları gösterme seçeneği
        print("6 - Add Student Registration")  # Student enrollment option // Öğrenci kaydetme seçeneği
        print("7 - View Registered Students")  # Option to show registered students // Kayıtlı öğrencileri gösterme seçeneği
        print("8 - View Book Rating Statistics")  # Newly added option // Yeni eklenen seçenek
        print("9 - Exit")
        choice = input("\nYour choice: ")  # Takes selection from user // Kullanıcıdan seçim alır

        if choice == "1":
            bookName = input("Book name: ")  # Enter the book name // Kitap adı girilir
            kind = input("Kind: ")  # Enter the book type // Kitap türünü girilir
            raf = input("Shelf No: ")  # Enter the book shelf number // Kitap raf numarası girilir
            sira = input("Sequence Number: ")  # Kitap sıra numarası girilir // Book serial number is entered
            bookID = str(newBookID())  # New book ID is created // Yeni kitap ID'si oluşturulur
            registry = f"{bookID},{bookName},{kind},{raf},{sira}"  # Book information is combined // Kitap bilgileri birleştirilir
            addToLine("books", registry)  # Book information is added to the books.txt file // Kitap bilgileri books.txt dosyasına eklenir
            print("\n✅ The book has been added.")  # Successful insertion message // Başarılı ekleme mesajı
            input("Press Enter to continue...")  # The user is expected to press to continue. // Kullanıcıdan devam etmek için tuşlama beklenir

        elif choice == "2":
            books = readLines("books")  # The books in the Kitaplar.txt file are read // Kitaplar.txt dosyasındaki books okunur
            if not books:  # If the books list is empty // Eğer books listesi boşsa
                print("\n⚠️ The book list is empty.")  # Warning message // Uyarı mesajı
            else:
                for k in books:  # The list of books is printed on the screen // Kitaplar listesi ekrana yazdırılır
                    print(k)
                deleted_id = input("Book ID you want to delete: ")  # The ID of the book to be deleted is entered // Silinecek kitap ID'si girilir
                books = [k for k in books if not k.startswith(deleted_id + ",")]  # The book to be deleted is removed from the list // Silinecek kitap listeden çıkarılır
                writeLines("books", books)  # The updated book list is written to the books.txt file // Güncellenmiş kitap listesi books.txt dosyasına yazılır
                print("\n✅ The book was deleted.")
            input("Press Enter to continue...")  # The user is expected to press Enter key to continue // Kullanıcıdan devam etmek için tuşlama beklenir

        elif choice == "3":
            books = readLines("books")  # List of books to read // Kitaplar listesi okunur
            if not books:  # If the books list is empty // Eğer books listesi boşsa
                print("\n⚠️ The book list is empty.")
            else:
                for k in books:  # Books are printed on the screen // Kitaplar ekrana yazdırılır
                    print(k)
            input("Press Enter to continue...")  # The user is expected to press Enter key to continue // Kullanıcıdan devam etmek için tuşlama beklenir

        elif choice == "4":
            entrust = readLines("entrust")  # The list of entrusted books is read // Emanet books listesi okunur
            if not entrust:  # If the list of relics is empty // Eğer emanetler listesi boşsa
                print("\n⚠️ The entrusted book was not found.")
            else:
                for e in entrust:  # The entrusted books are printed on the screen // Emanet books ekrana yazdırılır
                    print(e)
            input("Press Enter to continue...")  # The user is expected to press Enter key to continue // Kullanıcıdan devam etmek için tuşlama beklenir

        elif choice == "5":
            delivered = readLines("delivered")  # The list of "books" delivered is read // Teslim edilen books listesi okunur
            if not delivered:  # If the list of checked out books is empty // Eğer teslimler listesi boşsa
                print("\n⚠️ No books have been delivered yet.")
            else:
                for t in delivered:  # Delivered "books" are printed on the screen // Teslim edilen books ekrana yazdırılır
                    print(t)
            input("Press Enter to continue...")  # The user is expected to press Enter key to continue // Kullanıcıdan devam etmek için tuşlama beklenir

        elif choice == "6":
            # Add a student record // Öğrenci kaydı eklemek
            student_name = input("Student username: ")  # Enter the student username // Öğrenci kullanıcı adı girilir
            student_password = input("Student password: ")  # Student password is entered // Öğrenci şifresi girilir
            student_record = f"{student_name},{student_password}"  # Student information is combined // Öğrenci bilgileri birleştirilir
            addToLine("students", student_record)  # Student information is added to the students.txt file // Öğrenci bilgileri students.txt dosyasına eklenir
            print("\n✅ The student was registered.")
            input("Press Enter to continue...")  # The user is expected to press Enter key to continue // Kullanıcıdan devam etmek için tuşlama beklenir

        elif choice == "7":
            students = readLines("students")  # Read the registered students file // Kayıtlı öğrenciler dosyasını oku
            if not students:  # If the student list is empty // Eğer öğrenci listesi boşsa
                print("\n⚠️ The student list is empty.")
            else:
                print("\nRegistered Students:")  # Student list title // Öğrenci listesi başlığı
                for student in students:  # The list of students is printed on the screen // Öğrenciler listesi ekrana yazdırılır
                    print(student)
            input("Press Enter to continue...")  # The user is expected to press Enter key to continue // Kullanıcıdan devam etmek için tuşlama beklenir

        elif choice == "8":
            clear()
            print("\n📈 Book Score Statistics")
            score = readBookScores()
            if not score:
                print("\n⚠️ No ratings have been made yet.")
            else:
                allBooks = list(score.values())
                allBooks.sort(key=lambda x: x['average'], reverse=True)

                print("\nRank | Book Name | Average | Number of Points | Category")
                print("-" * 60)
                for i, book in enumerate(allBooks, 1):
                    print(f"{i:4} | {book['bookName'][:25]:25} | {book['average']:7.1f} | {book['numberOfPoints']:10} | {book['category']}")
            input("\nPress Enter to continue...")

        elif choice == "9":
            break  # Exit from the panel // Panelden çıkış yapılır

        else:
            print("\n⚠️ Invalid selection.")
            time.sleep(2)  # Waits for 2 seconds and directs the user back to the menu // 2 saniye bekler ve kullanıcıyı tekrar menüye yönlendirir


# Starting point of the main program // Ana programın başlangıç noktası
if __name__ == "__main__":
    isFileExistent()  # Create required files if they do not exist // Gerekli dosyalar yoksa oluştur
    while True:
        clear() # Clean the screen first // Önce ekranı temizle
        print("\n📚 Smart Library Assistant", flush=True) #flush=True prints the output to the screen immediately // flush=True çıktının hemen ekrana yazdırılmasını sağlar
        print("1 - Librarian Login")
        print("2 - Student Login")
        print("3 - Exit")
        choice = input("\nYour choice: ")

        if choice == "1":
            user = input("Librarian name: ")
            password = input("Password: ")
            if userVerify("librarian", user, password):
                librarianPanel()
            else:
                if userVerify("students", user, password):
                    print("\n❌ This user is registered only as a student, not a librarian!")
                else:
                    print("\n❌ Incorrect login!")
                time.sleep(2)

        elif choice == "2":
            user = input("Student username: ")
            password = input("Password: ")
            if userVerify("students", user, password):

                # When the student is logged in, inside the while True loop: // Öğrenci girişi yapıldığında while True döngüsü içinde:
             while True:
                clear()
                print(f"\n👤 Welcome {user}")
                print("1 - Get a Book")
                print("2 - Deliver Books")
                print("3 - View Book Recommendations")
                print("4 - Log Out")
                choice_o = input("\nYour choice: ")

                if choice_o == "1":
                 getBook(user)
                elif choice_o == "2":
                    deliverAbook()
                elif choice_o == "3":
                    showBookSuggestions(user)
                elif choice_o == "4":
                    break
                else:
                    print("\n⚠️ Invalid selection.")
                    time.sleep(2)
            else:
               print("\n❌ Incorrect entry!")
               time.sleep(2)

        elif choice == "3":
            print("\nExiting...")
            time.sleep(1)
            break  # Exit the program // Programdan çıkış

        else:
            print("\n⚠️ Invalid selection.")
            time.sleep(2)
