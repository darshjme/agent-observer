"""Tests for ReactiveProperty."""
import pytest
from agent_observer import ReactiveProperty, Observable


class Agent:
    status = ReactiveProperty("idle")
    task = ReactiveProperty(None)


def test_default_value():
    a = Agent()
    assert a.status == "idle"


def test_set_value():
    a = Agent()
    a.status = "running"
    assert a.status == "running"


def test_instances_independent():
    a1 = Agent()
    a2 = Agent()
    a1.status = "busy"
    assert a2.status == "idle"


def test_observable_for_returns_observable():
    a = Agent()
    obs = Agent.status.observable_for(a)
    assert isinstance(obs, Observable)


def test_observable_for_notifies_on_set():
    a = Agent()
    received = []
    Agent.status.observable_for(a).subscribe(received.append)
    a.status = "done"
    assert received == ["done"]


def test_class_level_access_returns_descriptor():
    assert isinstance(Agent.status, ReactiveProperty)


def test_none_default():
    a = Agent()
    assert a.task is None
