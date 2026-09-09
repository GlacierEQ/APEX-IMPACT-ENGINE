from __future__ import annotations

from .model import Decision, MissionSnapshot, Phase, QUALITY_THRESHOLD, RankedAction

_PHASE_ORDER = {Phase.BUILD: 0, Phase.USE: 1, Phase.POLISH: 2, Phase.COMPLETE: 3}
BASE_WEIGHTS = {
    "operator_impact": 1.5, "urgency": 1.2, "blocker_relief": 1.3,
    "external_leverage": 1.3, "capability_gain": 1.2, "evidence_gain": 1.1,
    "opportunity_gain": 1.2, "compounding_value": 1.4, "readiness": 0.8,
    "prior_investment": 0.5, "result_power": 1.4, "completion_gain": 1.0,
}
PHASE_MULTIPLIERS = {
    Phase.BUILD: {"capability_gain": 1.8, "blocker_relief": 1.6, "compounding_value": 1.4},
    Phase.USE: {"operator_impact": 1.5, "external_leverage": 1.7, "result_power": 2.0, "opportunity_gain": 1.5},
    Phase.POLISH: {"completion_gain": 2.2, "operator_impact": 1.2, "external_leverage": 1.1},
    Phase.COMPLETE: {},
}
PENALTIES = {
    "recency_only": 8.0, "support_only": 7.0, "duplicated_representation": 8.0,
    "speculative_architecture": 5.0, "easy_to_verify_only": 5.0, "heartbeat_only": 10.0,
}

class ImpactEngine:
    def __init__(self, threshold: float = QUALITY_THRESHOLD) -> None:
        self.threshold = threshold

    def determine_phase(self, snapshot: MissionSnapshot) -> Phase:
        if not snapshot.system_quality.passes(self.threshold):
            return Phase.BUILD
        if not snapshot.result_quality.passes(self.threshold) or not snapshot.objective_achieved:
            return Phase.USE
        if not snapshot.completion_quality.passes(self.threshold):
            return Phase.POLISH
        return Phase.COMPLETE

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
        return round(score, 3)

    def rank_actions(self, snapshot: MissionSnapshot, phase: Phase) -> tuple[RankedAction, ...]:
        if phase is Phase.COMPLETE:
            return ()
        invalidated = {a for i in snapshot.impacts for a in i.invalidates_actions}
        ranked = [
            RankedAction(a.action_id, self._score_action(a, phase, snapshot), a.description)
            for a in snapshot.actions
            if (a.changes_target_state or a.unblocks_mission) and a.action_id not in invalidated
        ]
        ranked.sort(key=lambda a: (-a.score, a.action_id))
        return tuple(ranked)

    def evaluate(self, snapshot: MissionSnapshot) -> Decision:
        phase = self.determine_phase(snapshot)
        ranked = self.rank_actions(snapshot, phase)
        selected = ranked[0].action_id if ranked else None
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
        adjusted = bool(snapshot.impacts) or (snapshot.previous_phase is not None and snapshot.previous_phase != phase)
        if snapshot.previous_phase is not None and _PHASE_ORDER[phase] < _PHASE_ORDER[snapshot.previous_phase]:
            rationale = "New evidence invalidated a prior gate; regress to the necessary phase. " + rationale
        if impact_trace:
            rationale += " Strategy re-evaluated for material impacts: " + "; ".join(impact_trace)
        return Decision(phase, selected, ranked, deficits, adjusted, impact_trace, rationale)
