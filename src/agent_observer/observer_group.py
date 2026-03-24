"""ObserverGroup: subscribe to multiple observables at once."""

from __future__ import annotations
from typing import Callable, Any
from .observable import Observable


class ObserverGroup:
    """Manages a collection of subscriptions across multiple Observables.

    Supports a fluent interface::

        group = (
            ObserverGroup()
            .watch(agent.status_obs, log_status)
            .watch(agent.task_obs, invalidate_cache)
        )
        # ... later:
        group.unwatch_all()
    """

    def __init__(self) -> None:
        # list of (observable, subscription_id) pairs
        self._subscriptions: list[tuple[Any, str]] = []

    def watch(self, observable: Any, handler: Callable) -> "ObserverGroup":
        """Subscribe *handler* to *observable*; returns self for chaining."""
        if not callable(handler):
            raise TypeError("handler must be callable")
        sub_id = observable.subscribe(handler)
        self._subscriptions.append((observable, sub_id))
        return self

    def unwatch_all(self) -> None:
        """Unsubscribe from all observed observables."""
        for observable, sub_id in self._subscriptions:
            try:
                observable.unsubscribe(sub_id)
            except (KeyError, Exception):
                pass  # already removed — safe to ignore
        self._subscriptions.clear()

    @property
    def subscription_count(self) -> int:
        """Return the number of active subscriptions."""
        return len(self._subscriptions)

    def __repr__(self) -> str:
        return f"ObserverGroup(subscriptions={self.subscription_count})"
