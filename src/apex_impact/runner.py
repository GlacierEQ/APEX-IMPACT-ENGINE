from __future__ import annotations

from collections.abc import Callable
from .engine import ImpactEngine
from .model import Decision, MissionSnapshot, Phase

def run_until_boundary(
    observe: Callable[[], MissionSnapshot],
    execute: Callable[[Decision], None],
    *,
    max_steps: int = 100,
    engine: ImpactEngine | None = None,
) -> Decision:
    """Observe -> evaluate impacts -> act -> observe again. Never heartbeat instead of using ready capability."""
    engine = engine or ImpactEngine()
    last: Decision | None = None
    for _ in range(max_steps):
        snapshot = observe()
        last = engine.evaluate(snapshot)
        if last.phase is Phase.COMPLETE or last.selected_action is None:
            return last
        execute(last)
    if last is None:
        raise RuntimeError("no evaluation occurred")
    raise RuntimeError("max_steps reached before a genuine boundary or 9+ completion")
