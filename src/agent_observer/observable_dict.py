"""ObservableDict: a dict that notifies observers on set/delete."""

from __future__ import annotations
import uuid
from typing import Any, Callable, Iterator


class ObservableDict:
    """A dictionary that emits change events to subscribed observers."""

    def __init__(self, initial: dict | None = None) -> None:
        self._data: dict = dict(initial) if initial else {}
        self._observers: dict[str, Callable] = {}

    # ------------------------------------------------------------------
    # dict interface
    # ------------------------------------------------------------------

    def __setitem__(self, key: Any, value: Any) -> None:
        self._data[key] = value
        self._notify({"action": "set", "key": key, "value": value})

    def __delitem__(self, key: Any) -> None:
        value = self._data[key]          # raises KeyError naturally
        del self._data[key]
        self._notify({"action": "delete", "key": key, "value": value})

    def __getitem__(self, key: Any) -> Any:
        return self._data[key]

    def __contains__(self, key: Any) -> bool:
        return key in self._data

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator:
        return iter(self._data)

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def get(self, key: Any, default: Any = None) -> Any:
        return self._data.get(key, default)

    # ------------------------------------------------------------------
    # Observer management (same interface as Observable)
    # ------------------------------------------------------------------

    def subscribe(self, observer: Callable) -> str:
        if not callable(observer):
            raise TypeError("observer must be callable")
        subscription_id = str(uuid.uuid4())
        self._observers[subscription_id] = observer
        return subscription_id

    def unsubscribe(self, subscription_id: str) -> None:
        if subscription_id not in self._observers:
            raise KeyError(f"Unknown subscription_id: {subscription_id!r}")
        del self._observers[subscription_id]

    @property
    def observer_count(self) -> int:
        return len(self._observers)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _notify(self, payload: dict) -> None:
        for observer in list(self._observers.values()):
            observer(payload)

    def __repr__(self) -> str:
        return f"ObservableDict({self._data!r}, observers={self.observer_count})"
