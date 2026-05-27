import os
import json

class Book:
    """代表單一圖書實體的資料類別"""
    def __init__(self, title, isbn, status):
        self.title = title
        self.isbn = isbn
        self.status = status

    def to_dict(self):
        """將物件轉換為字典以便 JSON 序列化"""
        return {"title": self.title, "isbn": self.isbn, "status": self.status}

    @classmethod
    def from_dict(cls, data):
        """從字典還原為 Book 物件"""
        return cls(data.get("title", "Unknown"), 
                   data.get("isbn", "Unknown"), 
                   data.get("status", "Available"))

class LibraryManager:
    """負責圖書管理的核心邏輯與檔案操作"""
    def __init__(self, filename="lib_data.json"):
        self.filename = filename
        self.books = []
        self._load_data()

    def _load_data(self):
        """從 JSON 檔案載入資料"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.books = [Book.from_dict(item) for item in data]
            except (json.JSONDecodeError, IOError) as e:
                print(f"警告：無法讀取或解析資料檔，將以空資料庫啟動。錯誤訊息: {e}")
                self.books = []

    def save_data(self):
        """將目前資料庫存回 JSON 檔案"""
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump([book.to_dict() for book in self.books], f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"錯誤：無法儲存資料檔。錯誤訊息: {e}")

    def check_isbn_exists(self, isbn):
        """檢查 ISBN 是否已存在"""
        return any(book.isbn == isbn for book in self.books)

    def add_book(self, title, isbn, status):
        """新增圖書"""
        if self.check_isbn_exists(isbn):
            return False, "ISBN Exist"
        
        new_book = Book(title, isbn, status)
        self.books.append(new_book)
        return True, "Success"

    def borrow_book(self, isbn):
        """借閱圖書 (更新狀態)"""
        for book in self.books:
            if book.isbn == isbn:
                if book.status == "borrowed":
                     return False, "Already Borrowed"
                book.status = "borrowed"
                return True, "Updated"
        return False, "Book Not Found"

    def get_all_books(self):
        """獲取所有圖書資訊"""
        return self.books

def main():
    manager = LibraryManager()
    print("=== 圖書管理系統 v1.0 (Modernized) ===")
    
    while True:
        try:
            # 分割指令與參數
            op = input("> ").strip().split(" ", 1)
            command = op[0].lower()
            args = op[1] if len(op) > 1 else ""

            if command == "exit":
                manager.save_data()
                print("系統關閉")
                break

            elif command == "add":
                if args:
                    raw = args.split("/")
                    if len(raw) == 3:
                        success, msg = manager.add_book(raw[0], raw[1], raw[2])
                        print(msg)
                    else:
                        print("Format Error: Title/ISBN/Status")
                else:
                     print("Format Error: Please provide Title/ISBN/Status")

            elif command == "show":
                books = manager.get_all_books()
                if not books:
                    print("目前資料庫中沒有書籍。")
                for b in books:
                    print(f"書名: {b.title}, ISBN: {b.isbn}, 狀態: {b.status}")

            elif command == "borrow":
                if args:
                     success, msg = manager.borrow_book(args)
                     print(msg)
                else:
                     print("Format Error: Please provide ISBN")

            else:
                if command: # 避免使用者單純按下 Enter 時跳出 Unknown Command
                    print("Unknown Command")

        except KeyboardInterrupt:
             # 優雅地處理 Ctrl+C 結束
             print("\n強制中斷，嘗試儲存資料...")
             manager.save_data()
             print("系統關閉")
             break
        except Exception as e:
             # 捕捉未預期的錯誤，避免系統崩潰
             print(f"發生未預期的錯誤: {e}")

if __name__ == "__main__":
    main()