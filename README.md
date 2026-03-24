# agent-observer

**Observer pattern for reactive agent systems.** Decouple state changes from reactions — plug in logging, monitoring, cache invalidation, and UI updates without touching your agent code.

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## Installation

```bash
pip install agent-observer
```

---

## Quick Start — Reactive Agent Status Monitoring

```python
from agent_observer import Observable, ObservableDict, ReactiveProperty, ObserverGroup

# ── Define a reactive agent ──────────────────────────────────────────────────

class MonitoredAgent:
    status   = ReactiveProperty("idle")       # "idle" | "running" | "error" | "done"
    progress = ReactiveProperty(0)            # 0–100
    metadata = None                           # set in __init__

    def __init__(self, name: str):
        self.name = name
        self.metadata = ObservableDict({"name": name, "retries": 0})

# ── Create agents ─────────────────────────────────────────────────────────────

agent = MonitoredAgent("data-pipeline")

# ── Wire up observers ─────────────────────────────────────────────────────────

# 1. Logging subsystem
def log(msg):
    print(f"[LOG] {msg}")

# 2. Monitoring dashboard (standalone observable example)
health = Observable("green")
health.subscribe(lambda s: print(f"[DASHBOARD] health → {s}"))

# 3. ObserverGroup — manage all subscriptions together
group = (
    ObserverGroup()
    .watch(MonitoredAgent.status.observable_for(agent),
           lambda s: log(f"agent={agent.name} status={s}"))
    .watch(MonitoredAgent.progress.observable_for(agent),
           lambda p: log(f"agent={agent.name} progress={p}%"))
    .watch(agent.metadata,
           lambda e: log(f"metadata[{e['key']}] {e['action']} → {e['value']}"))
)

print(f"Active subscriptions: {group.subscription_count}")  # 3

# ── Simulate agent lifecycle ──────────────────────────────────────────────────

agent.status = "running"          # → [LOG] agent=data-pipeline status=running
agent.progress = 50               # → [LOG] agent=data-pipeline progress=50%
agent.metadata["retries"] = 1     # → [LOG] metadata[retries] set → 1
agent.progress = 100              # → [LOG] agent=data-pipeline progress=100%
agent.status = "done"             # → [LOG] agent=data-pipeline status=done
health.set("green")               # → [DASHBOARD] health → green

# ── Teardown ─────────────────────────────────────────────────────────────────

group.unwatch_all()               # removes all 3 subscriptions at once
print(f"Active subscriptions: {group.subscription_count}")  # 0
```

---

## Components

### `Observable`

A value container that notifies observers on change.

```python
counter = Observable(0)
sid = counter.subscribe(lambda v: print(f"count={v}"))

counter.set(1)        # → count=1
counter.value = 2     # → count=2  (property setter)
counter.get()         # → 2

counter.unsubscribe(sid)
print(counter.observer_count)  # → 0
```

### `ObservableDict`

A dictionary that emits `{"action", "key", "value"}` events.

```python
state = ObservableDict({"status": "init"})
state.subscribe(lambda e: print(e))

state["status"] = "active"
# → {"action": "set", "key": "status", "value": "active"}

del state["status"]
# → {"action": "delete", "key": "status", "value": "active"}
```

### `ReactiveProperty`

A descriptor that wraps class attributes as `Observable` instances.

```python
class Agent:
    status = ReactiveProperty("idle")

a = Agent()
a.status                       # → "idle"
a.status = "running"           # triggers observers

obs = Agent.status.observable_for(a)
obs.subscribe(lambda s: print(f"status changed to {s}"))
```

### `ObserverGroup`

Manages multiple subscriptions with a single teardown.

```python
group = (
    ObserverGroup()
    .watch(observable_a, handler_a)
    .watch(observable_b, handler_b)
)

print(group.subscription_count)  # → 2
group.unwatch_all()               # unsubscribes from everything
```

---

## Design Principles

- **Zero dependencies** — pure Python 3.10+, nothing to install beyond pytest for tests
- **Decoupled** — observers never import agent code; agents never know who listens
- **Composable** — mix Observables, ObservableDicts, and ReactiveProperties freely
- **Fluent API** — `ObserverGroup.watch()` chains for readable setup

---

## License

MIT © Darshankumar Joshi
