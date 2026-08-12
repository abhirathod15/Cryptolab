import sqlite3
import getpass

# Database connection
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    issued_to INTEGER
)
""")

conn.commit()


# -----------------------------
# Authentication
# -----------------------------

USERNAME = "admin"
PASSWORD = "admin123"

logged_in = False


def login():
    global logged_in

    print("\n--- Login ---")

    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")

    if username == USERNAME and password == PASSWORD:
        logged_in = True
        print("Login successful.")
    else:
        print("Invalid username or password.")


def require_login():
    if not logged_in:
        print("Authentication required. Please login first.")
        return False

    return True


# -----------------------------
# 1. Register Member
# -----------------------------

def register_member():

    if not require_login():
        return

    print("\n--- Register Member ---")

    name = input("Enter member name: ").strip()

    # Input validation
    if not name:
        print("Name cannot be empty.")
        return

    if len(name) > 50:
        print("Name must be 50 characters or less.")
        return

    phone = input("Enter phone number: ").strip()

    # Input validation
    if not phone.isdigit() or len(phone) != 10:
        print("Phone number must contain exactly 10 digits.")
        return

    cursor.execute(
        "INSERT INTO members (name, phone) VALUES (?, ?)",
        (name, phone)
    )

    conn.commit()

    print("Member registered successfully.")


# -----------------------------
# 2. Add Book
# -----------------------------

def add_book():

    if not require_login():
        return

    print("\n--- Add Book ---")

    title = input("Enter book title: ").strip()

    if not title:
        print("Book title cannot be empty.")
        return

    if len(title) > 100:
        print("Book title is too long.")
        return

    author = input("Enter author name: ").strip()

    if not author:
        print("Author name cannot be empty.")
        return

    if len(author) > 100:
        print("Author name is too long.")
        return

    cursor.execute(
        "INSERT INTO books (title, author, issued_to) VALUES (?, ?, NULL)",
        (title, author)
    )

    conn.commit()

    print("Book added successfully.")


# -----------------------------
# 3. Search Book
# -----------------------------

def search_book():

    print("\n--- Search Book ---")

    keyword = input("Enter book title to search: ").strip()

    # Input validation
    if not keyword:
        print("Search keyword cannot be empty.")
        return

    if len(keyword) > 100:
        print("Search keyword is too long.")
        return

    # FIX: SQL Injection
    # Parameterized query is used instead of string formatting.
    cursor.execute(
        "SELECT * FROM books WHERE title LIKE ?",
        ("%" + keyword + "%",)
    )

    results = cursor.fetchall()

    if results:
        for book in results:
            print(book)
    else:
        print("No books found.")


# -----------------------------
# 4. Issue Book
# -----------------------------

def issue_book():

    # FIX: Missing Authentication
    if not require_login():
        return

    print("\n--- Issue Book ---")

    member_id = input("Enter member ID: ").strip()

    if not member_id.isdigit():
        print("Member ID must be a number.")
        return

    member_id = int(member_id)

    book_id = input("Enter book ID: ").strip()

    if not book_id.isdigit():
        print("Book ID must be a number.")
        return

    book_id = int(book_id)

    # Check member
    cursor.execute(
        "SELECT id FROM members WHERE id = ?",
        (member_id,)
    )

    member = cursor.fetchone()

    if member is None:
        print("Member not found.")
        return

    # Check book
    cursor.execute(
        "SELECT issued_to FROM books WHERE id = ?",
        (book_id,)
    )

    book = cursor.fetchone()

    if book is None:
        print("Book not found.")
        return

    if book[0] is not None:
        print("Book is already issued.")
        return

    cursor.execute(
        "UPDATE books SET issued_to = ? WHERE id = ?",
        (member_id, book_id)
    )

    conn.commit()

    print("Book issued successfully.")


# -----------------------------
# 5. Return Book
# -----------------------------

def return_book():

    if not require_login():
        return

    print("\n--- Return Book ---")

    book_id = input("Enter book ID: ").strip()

    if not book_id.isdigit():
        print("Book ID must be a number.")
        return

    book_id = int(book_id)

    cursor.execute(
        "SELECT issued_to FROM books WHERE id = ?",
        (book_id,)
    )

    book = cursor.fetchone()

    if book is None:
        print("Book not found.")
        return

    if book[0] is None:
        print("Book is not currently issued.")
        return

    cursor.execute(
        "UPDATE books SET issued_to = NULL WHERE id = ?",
        (book_id,)
    )

    conn.commit()

    print("Book returned successfully.")


# -----------------------------
# 6. Calculate Fine
# -----------------------------

def calculate_fine():

    print("\n--- Fine Calculation ---")

    days = input("Enter number of late days: ").strip()

    if not days.isdigit():
        print("Number of days must be a positive integer.")
        return

    days = int(days)

    if days > 365:
        print("Invalid number of days.")
        return

    fine = days * 5

    print("Fine amount: ₹", fine)


# -----------------------------
# 7. Display Books
# -----------------------------

def display_books():

    print("\n--- All Books ---")

    cursor.execute("SELECT * FROM books")

    books = cursor.fetchall()

    if not books:
        print("No books available.")
        return

    for book in books:
        print(
            "ID:", book[0],
            "| Title:", book[1],
            "| Author:", book[2],
            "| Issued To:", book[3]
        )


# -----------------------------
# Main Menu
# -----------------------------

def main():

    while True:

        print("\n================================")
        print("   SECURE LIBRARY MANAGEMENT")
        print("================================")

        print("1. Login")
        print("2. Register Member")
        print("3. Add Book")
        print("4. Search Book")
        print("5. Issue Book")
        print("6. Return Book")
        print("7. Calculate Fine")
        print("8. Display Books")
        print("9. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            login()

        elif choice == "2":
            register_member()

        elif choice == "3":
            add_book()

        elif choice == "4":
            search_book()

        elif choice == "5":
            issue_book()

        elif choice == "6":
            return_book()

        elif choice == "7":
            calculate_fine()

        elif choice == "8":
            display_books()

        elif choice == "9":
            print("Exiting application...")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()

conn.close()
