from abc import ABC, abstractmethod
from datetime import date, timedelta
from .status_enum import ItemStatus

class LibraryItem(ABC):
    _registry: dict[str, type["LibraryItem"]] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        LibraryItem._registry[cls.__name__] = cls

    def __init__(self):
        self._item_status = ItemStatus.AVAILABLE
        self._due_date = None

    _RESERVED_DICT_KEYS = ("type", "status", "due_date")

    @classmethod
    def from_dict(cls, data: dict) -> "LibraryItem":
        """Build the correct concrete LibraryItem subclass from a dict, dispatched by its "type" field via the subclass registry"""
        if cls is not LibraryItem:
            fields = {key: value for key, value in data.items() if key not in cls._RESERVED_DICT_KEYS}
            item = cls(**fields)
            status = data.get("status")
            if status is not None:
                item._item_status = ItemStatus(status)
            due_date = data.get("due_date")
            item._due_date = date.fromisoformat(due_date) if due_date else None
            return item
        item_type = data["type"]
        try:
            item_cls = cls._registry[item_type]
        except KeyError:
            raise ValueError(f"Unknown item type: {item_type!r}")
        return item_cls.from_dict(data)

    def to_dict(self) -> dict:
        """Serialize this item's common fields to a dict for persistence"""
        return {
            "type": type(self).__name__,
            "title": self.title,
            "author": self.author,
            "status": self.item_status.value,
            "due_date": self._due_date.isoformat() if self._due_date else None,
        }

    @property
    @abstractmethod
    def loan_period(self) -> int:
        """Get loan period of item, type int, represents days"""

    @property
    def item_status(self) -> ItemStatus:
        """Get status of an item, type ItemStatus"""
        return self._item_status

    @property
    def due_date(self) -> date:
        """Get due date of item, type date, None if not checked out"""
        return self._due_date

    def checkout_item(self):
        """Mark item as checked out"""
        if self._item_status == ItemStatus.LOST:
            raise ValueError("Cannot checkout item, item is lost")
        if self._item_status == ItemStatus.CHECKED_OUT:
            raise ValueError("Cannot checkout item, item is already checked out")
        self._item_status = ItemStatus.CHECKED_OUT
        self._due_date = date.today() + timedelta(days=self.loan_period)

    def return_item(self):
        """Mark item as available"""
        if self._item_status == ItemStatus.AVAILABLE:
            raise ValueError("Cannot return item, item is already available")
        self._item_status = ItemStatus.AVAILABLE
        self._due_date = None


    def mark_item_lost(self):
        """Mark item as lost"""
        self._item_status = ItemStatus.LOST

    @property
    @abstractmethod
    def title(self) -> str:
        """Get title of item, type str"""

    @title.setter
    @abstractmethod
    def title(self, value: str):
        """Set title of item, type str"""

    @property
    @abstractmethod
    def author(self) -> str:
        """Get author of item, type str"""

    @author.setter
    @abstractmethod
    def author(self, value: str):
        """Set author of item, type str"""

    def __lt__(self, other: "LibraryItem") -> bool:
        return self.title < other.title

    def __repr__(self) -> str:
        return f"{type(self).__name__}(title={self.title!r}, author={self.author!r}, item_status={self.item_status!r})"

    def __str__(self) -> str:
        return f"{self.title} ({type(self).__name__}) — {self.item_status.value}"