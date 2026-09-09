from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping

QUALITY_THRESHOLD = 9.0

class Phase(str, Enum):
    BUILD = "BUILD"
    USE = "USE"
    POLISH = "POLISH"
    COMPLETE = "COMPLETE"

@dataclass(frozen=True)
class QualityMetric:
    name: str
    score: float
    required: bool = True
    evidence: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not 0 <= self.score <= 10:
            raise ValueError(f"{self.name}: score must be in [0, 10]")

    @property
    def verified(self) -> bool:
        return bool(self.evidence)

@dataclass(frozen=True)
class QualitySet:
    metrics: tuple[QualityMetric, ...]

    def required_metrics(self) -> tuple[QualityMetric, ...]:
        return tuple(m for m in self.metrics if m.required)

    def passes(self, threshold: float = QUALITY_THRESHOLD) -> bool:
        required = self.required_metrics()
        return bool(required) and all(m.score >= threshold and m.verified for m in required)

    def deficits(self, threshold: float = QUALITY_THRESHOLD) -> tuple[str, ...]:
        deficits: list[str] = []
        for m in self.required_metrics():
            if m.score < threshold:
                deficits.append(f"{m.name}:{m.score:.1f}")
            elif not m.verified:
                deficits.append(f"{m.name}:UNVERIFIED")
        return tuple(deficits)

    def floor(self) -> float:
        required = self.required_metrics()
        return min((m.score for m in required), default=0.0)

@dataclass(frozen=True)
class ActionCandidate:
    action_id: str
    description: str
    scores: Mapping[str, float] = field(default_factory=dict)
    changes_target_state: bool = False
    unblocks_mission: bool = False
    flags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name, score in self.scores.items():
            if not 0 <= score <= 10:
                raise ValueError(f"{self.action_id}.{name}: score must be in [0, 10]")

@dataclass(frozen=True)
class ImpactSignal:
    signal_id: str
    summary: str
    invalidates_actions: tuple[str, ...] = ()
    score_adjustments: Mapping[str, float] = field(default_factory=dict)

@dataclass(frozen=True)
class MissionSnapshot:
    system_quality: QualitySet
    result_quality: QualitySet
    completion_quality: QualitySet
    objective_achieved: bool
    actions: tuple[ActionCandidate, ...] = ()
    impacts: tuple[ImpactSignal, ...] = ()
    previous_phase: Phase | None = None

@dataclass(frozen=True)
class RankedAction:
    action_id: str
    score: float
    description: str

@dataclass(frozen=True)
class Decision:
    phase: Phase
    selected_action: str | None
    ranked_actions: tuple[RankedAction, ...]
    deficits: tuple[str, ...]
    strategy_adjusted: bool
    impact_trace: tuple[str, ...]
    rationale: str
    reevaluate_after: str = "EVERY_MATERIAL_STATE_CHANGE"
