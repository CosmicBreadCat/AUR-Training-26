from Items import ItemStatus, LibraryItem
from database import Database

class Library:
    """Manages the LibraryItem collection and checkouts. Does not read or write files itself."""

    def __init__(self, database: Database = None):
        self._database = database if database is not None else Database()
        self._items: list[LibraryItem] = []

    def add_item(self, item: LibraryItem) -> None:
        """Add a LibraryItem to the collection"""
        self._items.append(item)

    def checkout(self, title: str) -> None:
        """Find an item by title and check it out"""
        item = self._get_by_title(title)
        item.checkout_item()

    def return_item(self, title: str) -> None:
        """Find an item by title and return it"""
        item = self._get_by_title(title)
        item.return_item()

    def mark_lost(self, title: str) -> None:
        """Find an item by title and mark it lost"""
        item = self._get_by_title(title)
        item.mark_item_lost()

    def find_by_title(self, title: str) -> LibraryItem | None:
        """Find and return an item by title, or None if not found"""
        for item in self._items:
            if item.title == title:
                return item
        return None

    def list_items(self) -> list:
        """Return all items in the collection"""
        return list(self._items)

    def list_available(self) -> list:
        """Return all items currently available"""
        return [item for item in self._items if item.item_status == ItemStatus.AVAILABLE]

    def save(self) -> None:
        """Persist the collection via the Database instance"""
        self._database.save(self._items)

    def load(self) -> None:
        """Load the collection via the Database instance"""
        self._items = self._database.load()

    def _get_by_title(self, title: str) -> LibraryItem:
        item = self.find_by_title(title)
        if item is None:
            raise ValueError(f"No item found with title: {title!r}")
        return item
