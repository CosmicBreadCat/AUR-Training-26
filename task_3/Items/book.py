from .base_item import LibraryItem

class Book(LibraryItem):
    def __init__(self, title: str, author: str, isbn_10: str = None):
        super().__init__()
        self._title = title
        self._author = author
        self._isbn_10 = isbn_10

    @property
    def loan_period(self) -> int:
        """Get loan period of item, type int, represents days"""
        return 21

    @property
    def title(self) -> str:
        """Get title of item, type str"""
        return self._title

    @title.setter
    def title(self, value: str):
        """Set title of item, type str"""
        self._title = value

    @property
    def author(self) -> str:
        """Get author of item, type str"""
        return self._author

    @author.setter
    def author(self, value: str):
        """Set author of item, type str"""
        self._author = value

    @property
    def isbn_10(self) -> str:
        """Get ISBN-10 id of item, type str"""
        return self._isbn_10

    @isbn_10.setter
    def isbn_10(self, value: str):
        """Set ISBN-10 id of item, type str"""
        self._isbn_10 = value

    def to_dict(self) -> dict:
        """Serialize this item's fields to a dict for persistence"""
        data = super().to_dict()
        data["isbn_10"] = self.isbn_10
        return data

    @staticmethod
    def validate_isbn_10(isbn: str) -> bool:
        """Validate an ISBN-10 checksum. Hyphens/spaces are ignored; the final check character may be 'X' (representing 10)."""
        isbn = isbn.replace("-", "").replace(" ", "")
        if len(isbn) != 10:
            return False
        total = 0
        for position, char in enumerate(isbn):
            if char.upper() == "X" and position == 9:
                digit = 10
            elif char.isdigit():
                digit = int(char)
            else:
                return False
            total += digit * (10 - position)
        return total % 11 == 0
