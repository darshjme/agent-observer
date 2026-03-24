"""Tests for ObserverGroup."""
import pytest
from agent_observer import Observable, ObserverGroup


def test_initial_subscription_count():
    g = ObserverGroup()
    assert g.subscription_count == 0


def test_watch_increases_count():
    obs = Observable(0)
    g = ObserverGroup()
    g.watch(obs, lambda v: None)
    assert g.subscription_count == 1


def test_watch_is_fluent():
    obs1, obs2 = Observable(), Observable()
    g = ObserverGroup()
    result = g.watch(obs1, lambda v: None).watch(obs2, lambda v: None)
    assert result is g
    assert g.subscription_count == 2


def test_watch_handler_called():
    obs = Observable(0)
    received = []
    ObserverGroup().watch(obs, received.append)
    obs.set(42)
    assert received == [42]


def test_unwatch_all_removes_all():
    obs1, obs2 = Observable(), Observable()
    g = ObserverGroup()
    g.watch(obs1, lambda v: None).watch(obs2, lambda v: None)
    g.unwatch_all()
    assert g.subscription_count == 0


def test_unwatch_all_stops_notifications():
    obs = Observable(0)
    received = []
    g = ObserverGroup().watch(obs, received.append)
    g.unwatch_all()
    obs.set(99)
    assert received == []


def test_watch_non_callable_raises():
    obs = Observable()
    g = ObserverGroup()
    with pytest.raises(TypeError):
        g.watch(obs, "not_callable")  # type: ignore
