import sqlite3

# Database connection
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    issued_to INTEGER
)
""")

conn.commit()


# -----------------------------
# 1. Register Member
# -----------------------------
def register_member():
    print("\n--- Register Member ---")

    name = input("Enter member name: ")
    phone = input("Enter phone number: ")

    # VULNERABILITY 1:
    # Improper Input Validation
    # No validation is performed on name or phone.

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
    print("\n--- Add Book ---")

    title = input("Enter book title: ")
    author = input("Enter author name: ")

    if title == "":
        print("Book title cannot be empty.")

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

    keyword = input("Enter book title to search: ")

    # VULNERABILITY 2:
    # SQL Injection
    # User input is directly inserted into SQL query.

    query = f"SELECT * FROM books WHERE title LIKE '%{keyword}%'"

    try:
        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            for book in results:
                print(book)
        else:
            print("No books found.")

    except sqlite3.Error as e:
        print("Database error:", e)


# -----------------------------
# 4. Issue Book
# -----------------------------
def issue_book():
    print("\n--- Issue Book ---")

    member_id = input("Enter member ID: ")
    book_id = input("Enter book ID: ")

    # VULNERABILITY 3:
    # Missing Authentication
    # No login/authentication check is performed.

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
    print("\n--- Return Book ---")

    book_id = input("Enter book ID: ")

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

    days = input("Enter number of late days: ")

    try:
        days = int(days)
        fine = days * 5

        print("Fine amount: ₹", fine)

    except ValueError:
        print("Invalid number of days.")


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
        print("   LIBRARY MANAGEMENT SYSTEM")
        print("================================")

        print("1. Register Member")
        print("2. Add Book")
        print("3. Search Book")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. Calculate Fine")
        print("7. Display Books")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            register_member()

        elif choice == "2":
            add_book()

        elif choice == "3":
            search_book()

        elif choice == "4":
            issue_book()

        elif choice == "5":
            return_book()

        elif choice == "6":
            calculate_fine()

        elif choice == "7":
            display_books()

        elif choice == "8":
            print("Exiting application...")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()

conn.close()
