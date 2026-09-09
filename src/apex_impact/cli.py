from __future__ import annotations

import argparse
import json
from pathlib import Path
from .engine import ImpactEngine
from .model import ActionCandidate, ImpactSignal, MissionSnapshot, Phase, QualityMetric, QualitySet

def _quality(data: dict) -> QualitySet:
    metrics = []
    for name, raw in data.items():
        if isinstance(raw, dict):
            metrics.append(QualityMetric(name, float(raw["score"]), bool(raw.get("required", True)), tuple(raw.get("evidence", ()))))
        else:
            metrics.append(QualityMetric(name, float(raw)))
    return QualitySet(tuple(metrics))

def _snapshot(data: dict) -> MissionSnapshot:
    actions = tuple(ActionCandidate(a["action_id"], a["description"], a.get("scores", {}),
        bool(a.get("changes_target_state", False)), bool(a.get("unblocks_mission", False)), tuple(a.get("flags", ())),
        bool(a.get("executable_now", True)), a.get("boundary_reason")) for a in data.get("actions", ()))
    impacts = tuple(ImpactSignal(i["signal_id"], i["summary"], tuple(i.get("invalidates_actions", ())), i.get("score_adjustments", {})) for i in data.get("impacts", ()))
    previous = data.get("previous_phase")
    return MissionSnapshot(_quality(data["system_quality"]), _quality(data["result_quality"]), _quality(data["completion_quality"]),
        bool(data.get("objective_achieved", False)), actions, impacts, Phase(previous) if previous else None)

def main() -> None:
    parser = argparse.ArgumentParser(description="Continuously evaluate impact and choose the correct evidenced 9+ phase/action.")
    parser.add_argument("snapshot", type=Path)
    args = parser.parse_args()
    decision = ImpactEngine().evaluate(_snapshot(json.loads(args.snapshot.read_text())))
    print(json.dumps({"phase": decision.phase.value, "selected_action": decision.selected_action,
        "ranked_actions": [r.__dict__ for r in decision.ranked_actions], "deficits": decision.deficits,
        "strategy_adjusted": decision.strategy_adjusted, "impact_trace": decision.impact_trace,
        "rationale": decision.rationale, "reevaluate_after": decision.reevaluate_after}, indent=2))

if __name__ == "__main__":
    main()
