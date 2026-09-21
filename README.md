# APEX-IMPACT-ENGINE

**Executable strategy engine** that continuously evaluates materially changed state and enforces the binding phase contract:

```text
BUILD → USE → POLISH → COMPLETE
```

This repository is a first-class node in the GlacierEQ constellation. It is designed to be discoverable by, and composable with:

- [mega-skills](https://github.com/GlacierEQ/mega-skills) (atomic / compound / mega skill hierarchy + deep-work pipelines)
- [Genius-Mastery](https://github.com/GlacierEQ/Genius-Mastery) (teacher-forge + family kernel)
- [aspen-grove-core](https://github.com/GlacierEQ/aspen-grove-core) (canonical spiral / memory / swarm boot)
- [apex-core](https://github.com/GlacierEQ/apex-core) and the broader APEX control surface

## Binding Contract (Non-Negotiable)

| Phase | Mandate |
|---|---|
| **BUILD** | Improve only purpose-critical system deficiencies until every required, evidenced quality dimension is ≥ 9. |
| **USE** | Once the system is exceptional, stop improving the machinery. Use it against the real mission until actual results are ≥ 9 and the objective is materially achieved. |
| **POLISH** | Close residual completeness, presentation, durability, handoff, and finish quality until ≥ 9. |
| **COMPLETE** | Only when **system quality + result quality + completion quality** independently clear evidenced 9+ gates. Then preserve the gain and move to the next mission. |

The engine refuses to let several 10s hide an 8.9. A claimed score without evidence references is **UNVERIFIED**, never “exceptional.”

## Action Selection Doctrine

**Rewards**
- Operator impact
- External leverage
- Actual result power
- Blocker removal
- Capability / evidence / opportunity gain
- Compounding value
- Urgency + readiness

**Penalizes / blocks**
- `heartbeat_only`
- `support_only`
- `recency_only`
- `duplicated_representation`
- `speculative_architecture`
- `easy_to_verify_only`

An action that neither changes target state nor genuinely unblocks the mission is not selectable.

## Ambition Runtime

Ambition is executable state, not motivational prose. When the same source-bearing mission_state_ref is observed again without verified movement, the engine accumulates bounded pressure. That pressure:

- raises the value of actions that change target state, unblock the mission, create external leverage, or produce actual result power;
- penalizes repeating the same action against an unchanged mission state;
- marks a material route change as required when another executable route exists;
- never makes heartbeat/status/summary work selectable;
- resets only when the mission-state reference actually changes or verified progress is explicitly recorded; and
- can persist across process restarts through APEX_AMBITION_STATE.

Ambition does not grant authority, rewrite the Operator mission, bypass provider boundaries, or manufacture progress. It increases execution pressure inside the already-authorized mission.

See [`docs/AMBITION.md`](docs/AMBITION.md) for the full contract.

```bash
export APEX_AMBITION_STATE=~/.apex/ambition-state.json
PYTHONPATH=src python -m apex_impact.cli --ambition-state "$APEX_AMBITION_STATE" examples/mission.json
```

## Constellation Position

```text
mega-skills (capability pyramids + pipelines)
        ↑
        │ composition / discovery
        ↓
APEX-IMPACT-ENGINE  ←→  Genius-Mastery (entity forge + progress kernel)
        ↑
        │ runtime / memory / swarm
        ↓
aspen-grove-core + apex-control-plane
```

This engine is the **live strategy evaluator** that decides *what* to do next under the BUILD/USE/POLISH/COMPLETE regime. Mega-skills supply the capability pyramids and executable deep-work pipelines; Genius-Mastery supplies entity synthesis and progress orchestration; this engine decides phase and selects the highest-impact next action against real state.

See:
- [`FOUNDATION.md`](FOUNDATION.md) — durable architectural and quality foundation
- [`MESH.md`](MESH.md) — peer + pipeline composition contracts
- [`interfaces/COMPOSITION.yaml`](interfaces/COMPOSITION.yaml) — machine-readable consume/produce edges
- [`docs/QUALITY_GATES.md`](docs/QUALITY_GATES.md) — evidence-required scoring rules
- [`docs/AMBITION.md`](docs/AMBITION.md) — executable ambition pressure
- [`docs/OPERATOR.md`](docs/OPERATOR.md) — human/agent runbook for real missions
- [`AGENTS.md`](AGENTS.md) — executable-agent behavioral contract
- [`src/apex_impact/`](src/apex_impact/) — phase machine, impact evaluator, selector, and execution loop

## Current Reality

- Remote executable source is live on canonical `main`.
- The engine implements evidence-required 9+ quality gates, reversible phase transitions, dynamic impact invalidation/reprioritization, anti-heartbeat action selection, ambition pressure, and observe → evaluate → execute → observe continuation.
- Genius contracts (`ROLE.yaml`, `capabilities/`, `interfaces/COMPOSITION.yaml`) are hardened for family discovery.
- `tests/test_engine.py` carries behavioral tests covering the binding phase and action-selection invariants.
- GitHub Actions CI executes the behavioral suite and verifies the example mission resolves to `USE` with real work selected over heartbeat.
- License: MIT.

## Use It

```bash
PYTHONPATH=src python -m apex_impact.cli examples/mission.json
PYTHONPATH=src python -m apex_impact.cli examples/mission_regression.json
PYTHONPATH=src python -m apex_impact.cli examples/mission_ambition.json
PYTHONPATH=src python -m unittest discover -s tests -v
```

| Example | Expected behavior |
|---------|-------------------|
| `examples/mission.json` | System ≥9, results < 9 → **USE** real work over heartbeat |
| `examples/mission_regression.json` | Prior COMPLETE + new failure evidence → regress to **BUILD** |
| `examples/mission_ambition.json` | Stalled mission state → prefer alternate route over repeated same path |

## Design Invariants

1. Strategy is live state, never a frozen plan.
2. Material changes can invalidate actions, reprioritize, advance, or regress COMPLETE → USE/BUILD.
3. Continuous observe → evaluate → execute → observe loop.
4. Real mission work always outranks heartbeat activity.
5. Evidence is mandatory for any claim ≥ 9.
6. The engine itself must remain subject to the same evidence and quality gates it enforces on missions.

---

*This repository exists so exceptional systems are built only as far as necessary, then used aggressively to produce exceptional results, then polished to exceptional completion.*
