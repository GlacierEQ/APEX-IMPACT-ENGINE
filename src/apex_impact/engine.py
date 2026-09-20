from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from .model import Decision, MissionSnapshot, Phase, QUALITY_THRESHOLD, RankedAction

_PHASE_ORDER = {Phase.BUILD: 0, Phase.USE: 1, Phase.POLISH: 2, Phase.COMPLETE: 3}
BASE_WEIGHTS = {
    "operator_impact": 1.5,
    "urgency": 1.2,
    "blocker_relief": 1.3,
    "external_leverage": 1.3,
    "capability_gain": 1.2,
    "evidence_gain": 1.1,
    "opportunity_gain": 1.2,
    "compounding_value": 1.4,
    "readiness": 0.8,
    "prior_investment": 0.5,
    "result_power": 1.4,
    "completion_gain": 1.0,
}
PHASE_MULTIPLIERS = {
    Phase.BUILD: {"capability_gain": 1.8, "blocker_relief": 1.6, "compounding_value": 1.4},
    Phase.USE: {"operator_impact": 1.5, "external_leverage": 1.7, "result_power": 2.0, "opportunity_gain": 1.5},
    Phase.POLISH: {"completion_gain": 2.2, "operator_impact": 1.2, "external_leverage": 1.1},
    Phase.COMPLETE: {},
}
PENALTIES = {
    "recency_only": 8.0,
    "support_only": 7.0,
    "duplicated_representation": 8.0,
    "speculative_architecture": 5.0,
    "easy_to_verify_only": 5.0,
    "heartbeat_only": 10.0,
    "status_only": 12.0,
    "another_plan": 12.0,
    "another_summary": 12.0,
}
AMBITION_MAX_CYCLES = 5
AMBITION_ROUTE_CHANGE_CYCLES = 1
AMBITION_REPEAT_PENALTY = 18.0
AMBITION_STATE_DELTA_BONUS = 7.0
AMBITION_UNBLOCK_BONUS = 4.0


class ImpactEngine:
    """Stateful strategy engine with bounded, evidence-driven ambition.

    Ambition is pressure to advance the Operator's already-bound mission. It never
    grants authority, rewrites the mission, bypasses executable boundaries, or
    treats activity as progress. Repeated observations of the same mission state
    increase pressure toward actions that change target state, unblock execution,
    produce external leverage, or switch away from an ineffective repeated route.
    """

    def __init__(
        self,
        threshold: float = QUALITY_THRESHOLD,
        *,
        ambition_state_path: str | Path | None = None,
    ) -> None:
        self.threshold = threshold
        configured = ambition_state_path or os.getenv("APEX_AMBITION_STATE")
        self.ambition_state_path = Path(configured).expanduser() if configured else None
        self._last_mission_state_ref: str | None = None
        self._no_progress_cycles = 0
        self._last_selected_action: str | None = None
        self._repeated_action_cycles = 0
        self._load_ambition_state()

    def determine_phase(self, snapshot: MissionSnapshot) -> Phase:
        if not snapshot.system_quality.passes(self.threshold):
            return Phase.BUILD
        if not snapshot.result_quality.passes(self.threshold) or not snapshot.objective_achieved:
            return Phase.USE
        if not snapshot.completion_quality.passes(self.threshold):
            return Phase.POLISH
        return Phase.COMPLETE

    @property
    def no_progress_cycles(self) -> int:
        return self._no_progress_cycles

    @property
    def ambition_pressure(self) -> float:
        cycles = min(self._no_progress_cycles, AMBITION_MAX_CYCLES)
        repeated = min(self._repeated_action_cycles, AMBITION_MAX_CYCLES)
        return round(min(10.0, cycles * 1.8 + repeated * 0.8), 2)

    def ambition_state(self) -> dict[str, Any]:
        return {
            "schema": "glaciereq.apex.ambition-state.v1",
            "last_mission_state_ref": self._last_mission_state_ref,
            "no_progress_cycles": self._no_progress_cycles,
            "last_selected_action": self._last_selected_action,
            "repeated_action_cycles": self._repeated_action_cycles,
            "ambition_pressure": self.ambition_pressure,
        }

    def record_verified_progress(self, mission_state_ref: str) -> None:
        ref = mission_state_ref.strip()
        if not ref:
            raise ValueError("mission_state_ref must be non-empty")
        self._last_mission_state_ref = ref
        self._no_progress_cycles = 0
        self._repeated_action_cycles = 0
        self._save_ambition_state()

    def _observe_mission_state(self, snapshot: MissionSnapshot) -> None:
        ref = snapshot.mission_state_ref.strip() if isinstance(snapshot.mission_state_ref, str) else ""
        if not ref:
            return
        if self._last_mission_state_ref is None:
            self._last_mission_state_ref = ref
            self._no_progress_cycles = 0
        elif ref == self._last_mission_state_ref:
            self._no_progress_cycles += 1
        else:
            self._last_mission_state_ref = ref
            self._no_progress_cycles = 0
            self._repeated_action_cycles = 0

    def _score_action(self, action, phase: Phase, snapshot: MissionSnapshot) -> float:
        score = 0.0
        multipliers = PHASE_MULTIPLIERS[phase]
        for dimension, weight in BASE_WEIGHTS.items():
            value = float(action.scores.get(dimension, 0.0))
            score += value * weight * multipliers.get(dimension, 1.0)
        score += 12.0 if action.changes_target_state else (4.0 if action.unblocks_mission else -25.0)
        for flag in action.flags:
            score -= PENALTIES.get(flag, 0.0)
        for impact in snapshot.impacts:
            score += float(impact.score_adjustments.get(action.action_id, 0.0))

        cycles = min(self._no_progress_cycles, AMBITION_MAX_CYCLES)
        if cycles:
            if action.changes_target_state:
                score += AMBITION_STATE_DELTA_BONUS * cycles
            if action.unblocks_mission:
                score += AMBITION_UNBLOCK_BONUS * cycles
            score += float(action.scores.get("result_power", 0.0)) * 0.55 * cycles
            score += float(action.scores.get("external_leverage", 0.0)) * 0.45 * cycles
            score += float(action.scores.get("operator_impact", 0.0)) * 0.25 * cycles
            score += float(action.scores.get("urgency", 0.0)) * 0.20 * cycles
            if action.action_id == self._last_selected_action:
                score -= AMBITION_REPEAT_PENALTY * cycles
        return round(score, 3)

    def rank_actions(self, snapshot: MissionSnapshot, phase: Phase) -> tuple[RankedAction, ...]:
        if phase is Phase.COMPLETE:
            return ()
        invalidated = {a for i in snapshot.impacts for a in i.invalidates_actions}
        ranked = [
            RankedAction(a.action_id, self._score_action(a, phase, snapshot), a.description)
            for a in snapshot.actions
            if a.executable_now
            and (a.changes_target_state or a.unblocks_mission)
            and a.action_id not in invalidated
        ]
        ranked.sort(key=lambda a: (-a.score, a.action_id))
        return tuple(ranked)

    def evaluate(self, snapshot: MissionSnapshot) -> Decision:
        self._observe_mission_state(snapshot)
        phase = self.determine_phase(snapshot)
        if phase is Phase.COMPLETE:
            self._no_progress_cycles = 0
            self._repeated_action_cycles = 0

        ranked = self.rank_actions(snapshot, phase)
        selected = ranked[0].action_id if ranked else None

        alternatives = tuple(
            row for row in ranked if row.action_id != self._last_selected_action
        )
        route_change_required = bool(
            self._no_progress_cycles >= AMBITION_ROUTE_CHANGE_CYCLES
            and self._last_selected_action
            and alternatives
        )
        if route_change_required and selected == self._last_selected_action:
            selected = alternatives[0].action_id
            ranked = tuple(
                [next(row for row in ranked if row.action_id == selected)]
                + [row for row in ranked if row.action_id != selected]
            )

        prior_selected = self._last_selected_action
        if selected is not None:
            if selected == prior_selected and self._no_progress_cycles > 0:
                self._repeated_action_cycles += 1
            else:
                self._repeated_action_cycles = 0
            self._last_selected_action = selected

        if phase is Phase.BUILD:
            deficits = tuple(f"system.{d}" for d in snapshot.system_quality.deficits(self.threshold))
            rationale = "Improve only purpose-critical system deficiencies until every required, evidenced dimension is 9+."
        elif phase is Phase.USE:
            deficits = tuple(f"result.{d}" for d in snapshot.result_quality.deficits(self.threshold))
            if not snapshot.objective_achieved:
                deficits += ("result.objective_not_yet_achieved",)
            rationale = "System is exceptional enough: stop polishing machinery and use it for powerful mission progress until evidenced results are 9+."
        elif phase is Phase.POLISH:
            deficits = tuple(f"completion.{d}" for d in snapshot.completion_quality.deficits(self.threshold))
            rationale = "Excellent results exist: finish closure, presentation, handoff, durability, and residual defects to evidenced 9+ completion."
        else:
            deficits = ()
            rationale = "System, results, and completion independently clear evidenced 9+ gates: preserve gains and move to the next highest-value mission."

        impact_trace = tuple(f"{i.signal_id}: {i.summary}" for i in snapshot.impacts)
        adjusted = bool(snapshot.impacts) or (
            snapshot.previous_phase is not None and snapshot.previous_phase != phase
        )
        if snapshot.previous_phase is not None and _PHASE_ORDER[phase] < _PHASE_ORDER[snapshot.previous_phase]:
            rationale = "New evidence invalidated a prior gate; regress to the necessary phase. " + rationale
        if impact_trace:
            rationale += " Strategy re-evaluated for material impacts: " + "; ".join(impact_trace)
        if self._no_progress_cycles:
            rationale += (
                f" AMBITION pressure={self.ambition_pressure:.2f}/10 after "
                f"{self._no_progress_cycles} unchanged mission-state observation(s); "
                "activity is not credited as progress."
            )
        if route_change_required:
            rationale += " Repeated non-progress requires a materially different executable route."

        decision = Decision(
            phase,
            selected,
            ranked,
            deficits,
            adjusted or route_change_required or bool(self._no_progress_cycles),
            impact_trace,
            rationale,
            ambition_pressure=self.ambition_pressure,
            no_progress_cycles=self._no_progress_cycles,
            route_change_required=route_change_required,
            mission_state_ref=snapshot.mission_state_ref,
        )
        self._save_ambition_state()
        return decision

    def _load_ambition_state(self) -> None:
        path = self.ambition_state_path
        if path is None or not path.is_file():
            return
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return
        if not isinstance(payload, dict):
            return
        self._last_mission_state_ref = payload.get("last_mission_state_ref") or None
        self._no_progress_cycles = max(0, int(payload.get("no_progress_cycles", 0)))
        self._last_selected_action = payload.get("last_selected_action") or None
        self._repeated_action_cycles = max(0, int(payload.get("repeated_action_cycles", 0)))

    def _save_ambition_state(self) -> None:
        path = self.ambition_state_path
        if path is None:
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(json.dumps(self.ambition_state(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        tmp.replace(path)
