from Items import Book, DVD, Magazine, LibraryItem
from database import Database
from library import Library

MENU = """
Library Management System
1) Add item
2) List all items
3) List available items
4) Checkout item
5) Return item
6) Mark item lost
7) Save
8) Exit
"""

def add_item(library: Library) -> None:
    item_type = input("Type (Book/DVD/Magazine): ").strip().lower()
    title = input("Title: ").strip()
    author = input("Author: ").strip()

    if item_type == "book":
        isbn_10 = input("ISBN-10 (optional): ").strip() or None
        if isbn_10 and not Book.validate_isbn_10(isbn_10):
            print(f"Warning: {isbn_10!r} does not look like a valid ISBN-10, saving it anyway")
        item = Book(title, author, isbn_10)
    elif item_type == "dvd":
        item = DVD(title, author)
    elif item_type == "magazine":
        item = Magazine(title, author)
    else:
        print(f"Unknown item type: {item_type!r}")
        return

    library.add_item(item)
    print(f"Added: {item}")

def list_items(items: list) -> None:
    if not items:
        print("(none)")
        return
    for item in sorted(items):
        due = f", due {item.due_date}" if item.due_date else ""
        print(f"- {item}{due}")

def checkout(library: Library) -> None:
    title = input("Title to checkout: ").strip()
    try:
        library.checkout(title)
        print(f"Checked out: {title}")
    except ValueError as e:
        print(f"Error: {e}")

def return_item(library: Library) -> None:
    title = input("Title to return: ").strip()
    try:
        library.return_item(title)
        print(f"Returned: {title}")
    except ValueError as e:
        print(f"Error: {e}")

def mark_lost(library: Library) -> None:
    title = input("Title to mark lost: ").strip()
    try:
        library.mark_lost(title)
        print(f"Marked lost: {title}")
    except ValueError as e:
        print(f"Error: {e}")

def main() -> None:
    library = Library(Database())
    library.load()

    actions = {
        "1": lambda: add_item(library),
        "2": lambda: list_items(library.list_items()),
        "3": lambda: list_items(library.list_available()),
        "4": lambda: checkout(library),
        "5": lambda: return_item(library),
        "6": lambda: mark_lost(library),
        "7": library.save,
    }

    while True:
        print(MENU)
        choice = input("Choose an option (input the number): ").strip()
        if choice == "8":
            library.save()
            print("Saved, goodbye.")
            break
        action = actions.get(choice)
        if action is None:
            print("Invalid option")
            continue
        action()

if __name__ == "__main__":
    main()
