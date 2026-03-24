"""Tests for Observable."""
import pytest
from agent_observer import Observable


def test_default_value_is_none():
    obs = Observable()
    assert obs.get() is None


def test_initial_value_stored():
    obs = Observable(42)
    assert obs.get() == 42


def test_value_property_reads():
    obs = Observable("hello")
    assert obs.value == "hello"


def test_value_property_sets():
    obs = Observable(0)
    obs.value = 99
    assert obs.get() == 99


def test_set_updates_value():
    obs = Observable(1)
    obs.set(2)
    assert obs.get() == 2


def test_observer_called_on_set():
    obs = Observable(0)
    received = []
    obs.subscribe(received.append)
    obs.set(7)
    assert received == [7]


def test_subscribe_returns_string_id():
    obs = Observable()
    sid = obs.subscribe(lambda v: None)
    assert isinstance(sid, str) and len(sid) > 0


def test_observer_count():
    obs = Observable()
    assert obs.observer_count == 0
    obs.subscribe(lambda v: None)
    assert obs.observer_count == 1
    obs.subscribe(lambda v: None)
    assert obs.observer_count == 2


def test_unsubscribe_removes_observer():
    obs = Observable()
    sid = obs.subscribe(lambda v: None)
    obs.unsubscribe(sid)
    assert obs.observer_count == 0


def test_unsubscribe_unknown_id_raises():
    obs = Observable()
    with pytest.raises(KeyError):
        obs.unsubscribe("nonexistent-id")


def test_multiple_observers_all_called():
    obs = Observable()
    calls = []
    obs.subscribe(lambda v: calls.append(("a", v)))
    obs.subscribe(lambda v: calls.append(("b", v)))
    obs.set("x")
    assert ("a", "x") in calls
    assert ("b", "x") in calls


def test_subscribe_non_callable_raises():
    obs = Observable()
    with pytest.raises(TypeError):
        obs.subscribe("not_callable")  # type: ignore


def test_observer_not_called_after_unsubscribe():
    obs = Observable(0)
    received = []
    sid = obs.subscribe(received.append)
    obs.unsubscribe(sid)
    obs.set(999)
    assert received == []
