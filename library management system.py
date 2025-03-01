import os
import datetime
import shutil
import matplotlib.pyplot as plt

# File paths
BOOKS_FILE = "books.txt"
MEMBERS_FILE = "members.txt"
TRANSACTIONS_FILE = "transactions.txt"
USERS_FILE = "users.txt"
EBOOKS_DIR = "ebooks"

# Ensure eBooks directory exists
if not os.path.exists(EBOOKS_DIR):
    os.makedirs(EBOOKS_DIR)

# Utility function to load data
def load_data(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as file:
        return [line.strip().split(",") for line in file.readlines()]

# Utility function to save data
def save_data(filename, data):
    with open(filename, "w") as file:
        for record in data:
            file.write(",".join(record) + "\n")

# Admin & User Login System
class User:
    current_user = None  # To track logged-in user

    @staticmethod
    def register():
        users = load_data(USERS_FILE)
        username = input("Enter new username: ")

        for user in users:
            if user[0] == username:
                print("Username already exists! Try a different one.")
                return
        
        password = input("Enter new password: ")
        role = input("Enter role (admin/user): ").lower()

        if role not in ["admin", "user"]:
            print("Invalid role! Choose either 'admin' or 'user'.")
            return
        
        users.append([username, password, role])
        save_data(USERS_FILE, users)
        print("User registered successfully!")

    @staticmethod
    def login():
        users = load_data(USERS_FILE)
        username = input("Enter username: ")
        password = input("Enter password: ")

        for user in users:
            if user[0] == username and user[1] == password:
                print(f"Login successful! Welcome, {username}.")
                User.current_user = user  # Save logged-in user
                return user[2]  # Return role (admin/user)
        
        print("Invalid credentials!")
        return None

    @staticmethod
    def logout():
        print("Logging out...")
        User.current_user = None

# Book Management
class Book:
    @staticmethod
    def add_book():
        books = load_data(BOOKS_FILE)
        book_id = str(len(books) + 1)
        title = input("Enter book title: ")
        author = input("Enter author: ")
        copies = input("Enter number of copies: ")
        books.append([book_id, title, author, copies])
        save_data(BOOKS_FILE, books)
        print("Book added successfully!")

    @staticmethod
    def view_books():
        books = load_data(BOOKS_FILE)
        print("\nAvailable Books:")
        for book in books:
            print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Copies: {book[3]}")

    @staticmethod
    def remove_book():
        books = load_data(BOOKS_FILE)
        book_id = input("Enter Book ID to remove: ")
        books = [book for book in books if book[0] != book_id]
        save_data(BOOKS_FILE, books)
        print("Book removed successfully!")

# Member Management
class Member:
    @staticmethod
    def add_member():
        members = load_data(MEMBERS_FILE)
        member_id = str(len(members) + 1)
        name = input("Enter member name: ")
        members.append([member_id, name])
        save_data(MEMBERS_FILE, members)
        print("Member added successfully!")

    @staticmethod
    def view_members():
        members = load_data(MEMBERS_FILE)
        print("\nRegistered Members:")
        for member in members:
            print(f"ID: {member[0]}, Name: {member[1]}")

# Borrow & Return Management
class Transaction:
    @staticmethod
    def issue_book():
        books = load_data(BOOKS_FILE)
        transactions = load_data(TRANSACTIONS_FILE)

        book_id = input("Enter Book ID: ")
        member_id = input("Enter Member ID: ")

        for book in books:
            if book[0] == book_id and int(book[3]) > 0:
                book[3] = str(int(book[3]) - 1)
                issue_date = datetime.date.today()
                due_date = issue_date + datetime.timedelta(days=14)
                transactions.append([member_id, book_id, str(issue_date), str(due_date), "Not Returned"])
                save_data(BOOKS_FILE, books)
                save_data(TRANSACTIONS_FILE, transactions)
                print(f"Book issued successfully! Due date: {due_date}")
                return

        print("Book not available.")

    @staticmethod
    def return_book():
        transactions = load_data(TRANSACTIONS_FILE)
        books = load_data(BOOKS_FILE)

        member_id = input("Enter Member ID: ")
        book_id = input("Enter Book ID: ")

        for transaction in transactions:
            if transaction[0] == member_id and transaction[1] == book_id and transaction[4] == "Not Returned":
                return_date = datetime.date.today()
                due_date = datetime.date.fromisoformat(transaction[3])
                fine = max((return_date - due_date).days, 0) * 2  # $2 per late day
                transaction[4] = f"Returned on {return_date} (Fine: ${fine})"
                
                for book in books:
                    if book[0] == book_id:
                        book[3] = str(int(book[3]) + 1)
                
                save_data(BOOKS_FILE, books)
                save_data(TRANSACTIONS_FILE, transactions)
                print(f"Book returned successfully! Fine: ${fine}")
                return

        print("No matching record found.")

# Graphical Reports (Matplotlib)
class Reports:
    @staticmethod
    def most_borrowed_books():
        transactions = load_data(TRANSACTIONS_FILE)
        book_counts = {}
        for transaction in transactions:
            book_counts[transaction[1]] = book_counts.get(transaction[1], 0) + 1

        # Bar chart
        plt.bar(book_counts.keys(), book_counts.values())
        plt.xlabel("Book ID")
        plt.ylabel("Times Borrowed")
        plt.title("Most Borrowed Books")
        plt.show()

# E-Book Management
class EBook:
    @staticmethod
    def list_ebooks():
        print("\nAvailable E-Books:")
        for ebook in os.listdir(EBOOKS_DIR):
            print(ebook)

# Main Menu
def main():
    while True:
        print("\nLibrary Management System")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        
        choice = input("Enter choice: ")

        if choice == "1":
            User.register()
        elif choice == "2":
            role = User.login()
            if role:
                while User.current_user:
                    print("\nLibrary Menu")
                    print("1. View Books")
                    print("2. Issue Book")
                    print("3. Return Book")
                    print("4. Most Borrowed Books Report")
                    print("5. List E-Books")
                    print("6. Logout")

                    if role == "admin":
                        print("7. Add Book")
                        print("8. Remove Book")
                        print("9. Add Member")

                    option = input("Enter choice: ")

                    if option == "1":
                        Book.view_books()
                    elif option == "2":
                        Transaction.issue_book()
                    elif option == "3":
                        Transaction.return_book()
                    elif option == "4":
                        Reports.most_borrowed_books()
                    elif option == "5":
                        EBook.list_ebooks()
                    elif option == "6":
                        User.logout()
                        break
                    elif role == "admin" and option == "7":
                        Book.add_book()
                    elif role == "admin" and option == "8":
                        Book.remove_book()
                    elif role == "admin" and option == "9":
                        Member.add_member()
                    else:
                        print("Invalid choice!")

if _name_ == "_main_":
    main()