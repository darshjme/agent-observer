"""ReactiveProperty: descriptor that wraps class attributes as Observable."""

from __future__ import annotations
from typing import Any
from .observable import Observable


_ATTR_PREFIX = "_reactive_prop_"


class ReactiveProperty:
    """Descriptor that stores an Observable per instance.

    Usage::

        class Agent:
            status = ReactiveProperty("idle")
            task   = ReactiveProperty(None)

        a = Agent()
        a.status  # → "idle"
        a.status = "running"
        sub_id = Agent.status.observable_for(a).subscribe(print)
    """

    def __init__(self, default: Any = None) -> None:
        self._default = default
        self._attr_name: str | None = None  # set via __set_name__ when possible

    def __set_name__(self, owner: type, name: str) -> None:
        self._attr_name = name

    # ------------------------------------------------------------------
    # Descriptor protocol
    # ------------------------------------------------------------------

    def _get_observable(self, instance: object) -> Observable:
        """Lazily create and cache the Observable on the instance."""
        key = _ATTR_PREFIX + (self._attr_name or str(id(self)))
        obs = instance.__dict__.get(key)
        if obs is None:
            obs = Observable(self._default)
            instance.__dict__[key] = obs
        return obs

    def __get__(self, instance: object | None, owner: type) -> Any:
        if instance is None:
            return self  # class-level access returns descriptor
        return self._get_observable(instance).get()

    def __set__(self, instance: object, value: Any) -> None:
        self._get_observable(instance).set(value)

    def observable_for(self, instance: object) -> Observable:
        """Return the underlying Observable for a specific instance."""
        return self._get_observable(instance)

    def __repr__(self) -> str:
        return f"ReactiveProperty(default={self._default!r})"
