"""Observable: a value that notifies observers when it changes."""

from __future__ import annotations
import uuid
from typing import Any, Callable


class Observable:
    """A value container that notifies subscribed observers on change."""

    def __init__(self, value: Any = None) -> None:
        self._value = value
        self._observers: dict[str, Callable] = {}

    # ------------------------------------------------------------------
    # Value access
    # ------------------------------------------------------------------

    def get(self) -> Any:
        """Return the current value."""
        return self._value

    def set(self, value: Any) -> None:
        """Update the value and notify all observers."""
        self._value = value
        self._notify(value)

    @property
    def value(self) -> Any:
        """Property alias for get()."""
        return self.get()

    @value.setter
    def value(self, new_value: Any) -> None:
        self.set(new_value)

    # ------------------------------------------------------------------
    # Observer management
    # ------------------------------------------------------------------

    def subscribe(self, observer: Callable) -> str:
        """Register an observer callable. Returns a subscription_id."""
        if not callable(observer):
            raise TypeError("observer must be callable")
        subscription_id = str(uuid.uuid4())
        self._observers[subscription_id] = observer
        return subscription_id

    def unsubscribe(self, subscription_id: str) -> None:
        """Remove an observer by its subscription_id."""
        if subscription_id not in self._observers:
            raise KeyError(f"Unknown subscription_id: {subscription_id!r}")
        del self._observers[subscription_id]

    @property
    def observer_count(self) -> int:
        """Return the number of active observers."""
        return len(self._observers)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _notify(self, payload: Any) -> None:
        for observer in list(self._observers.values()):
            observer(payload)

    def __repr__(self) -> str:
        return f"Observable(value={self._value!r}, observers={self.observer_count})"
