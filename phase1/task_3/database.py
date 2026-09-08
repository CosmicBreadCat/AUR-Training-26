import json
import os

from Items import LibraryItem

class Database:
    """Responsible only for saving/loading the LibraryItem collection to/from database.txt.

    Singleton: every part of the program that calls Database(...) gets back the
    same instance, so there is one shared view of the file's location/state.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, filepath: str = "database.txt"):
        if self._initialized:
            return
        self._filepath = filepath
        self._initialized = True

    def load(self) -> list:
        """Read database.txt and return a list of LibraryItem instances"""
        if not os.path.exists(self._filepath):
            return []
        items = []
        with open(self._filepath, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                items.append(LibraryItem.from_dict(json.loads(line)))
        return items

    def save(self, items: list) -> None:
        """Write a list of LibraryItem instances to database.txt, one JSON object per line"""
        with open(self._filepath, "w") as f:
            for item in items:
                f.write(json.dumps(item.to_dict()) + "\n")
