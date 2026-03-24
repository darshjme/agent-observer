"""Tests for ObservableDict."""
import pytest
from agent_observer import ObservableDict


def test_empty_init():
    d = ObservableDict()
    assert len(d) == 0


def test_initial_dict():
    d = ObservableDict({"a": 1})
    assert d["a"] == 1


def test_setitem_stores_value():
    d = ObservableDict()
    d["key"] = "val"
    assert d["key"] == "val"


def test_setitem_notifies_set_action():
    d = ObservableDict()
    events = []
    d.subscribe(events.append)
    d["x"] = 10
    assert events == [{"action": "set", "key": "x", "value": 10}]


def test_delitem_notifies_delete_action():
    d = ObservableDict({"y": 20})
    events = []
    d.subscribe(events.append)
    del d["y"]
    assert events == [{"action": "delete", "key": "y", "value": 20}]


def test_delitem_unknown_key_raises():
    d = ObservableDict()
    with pytest.raises(KeyError):
        del d["missing"]


def test_observer_count_tracks_subscribers():
    d = ObservableDict()
    assert d.observer_count == 0
    sid = d.subscribe(lambda e: None)
    assert d.observer_count == 1
    d.unsubscribe(sid)
    assert d.observer_count == 0


def test_keys_values_items():
    d = ObservableDict({"a": 1, "b": 2})
    assert set(d.keys()) == {"a", "b"}
    assert set(d.values()) == {1, 2}
    assert set(d.items()) == {("a", 1), ("b", 2)}


def test_contains():
    d = ObservableDict({"k": "v"})
    assert "k" in d
    assert "missing" not in d
