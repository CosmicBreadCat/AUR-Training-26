from .base_item import LibraryItem

class Magazine(LibraryItem):
    def __init__(self, title: str, author: str):
        super().__init__()
        self._title = title
        self._author = author

    @property
    def loan_period(self) -> int:
        """Get loan period of item, type int, represents days"""
        return 14

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
