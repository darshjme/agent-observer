"""agent-observer: Observer pattern for reactive agent systems."""

from .observable import Observable
from .observable_dict import ObservableDict
from .reactive_property import ReactiveProperty
from .observer_group import ObserverGroup

__all__ = ["Observable", "ObservableDict", "ReactiveProperty", "ObserverGroup"]
__version__ = "1.0.0"
