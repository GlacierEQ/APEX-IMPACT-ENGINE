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

| Phase     | Mandate |
|-----------|---------|
| **BUILD** | Improve only purpose-critical system deficiencies until every required, evidenced quality dimension is ≥ 9. |
| **USE**   | Once the system is exceptional, stop improving the machinery. Use it against the real mission until actual results are ≥ 9 and the objective is materially achieved. |
| **POLISH**| Close residual completeness, presentation, durability, handoff, and finish quality until ≥ 9. |
| **COMPLETE** | Only when **system quality + result quality + completion quality** independently clear evidenced 9+ gates. Then preserve the gain and move to the next mission. |

The engine refuses to let several 10s hide an 8.9.  
A claimed score without evidence references is **UNVERIFIED**, never “exceptional.”

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
- [`MESH.md`](MESH.md) — peer links and composition contracts
- [`docs/QUALITY_GATES.md`](docs/QUALITY_GATES.md) — evidence-required scoring rules

## Current Reality

- Local canonical path: `/Users/kcbflux/APEX_SYSTEM/ENGINES/APEX-IMPACT-ENGINE`
- Local head (pre-push): `20348ddff2232da70483cf47db2e7653a0d424c1`
- 11 behavioral tests already green (strict 9+ gates, phase transitions, anti-heartbeat selection, dynamic invalidation, regression from COMPLETE)
- Remote foundation now live; source push still required for full system-quality evidence

## Immediate Operator Action

```bash
cd /Users/kcbflux/APEX_SYSTEM/ENGINES/APEX-IMPACT-ENGINE
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/GlacierEQ/APEX-IMPACT-ENGINE.git
git branch -M main
git push -u origin main
```

After the push, the engine becomes evaluable under its own rules by any third party and by the rest of the constellation.

## Design Invariants

1. Strategy is live state, never a frozen plan.
2. Material changes can invalidate actions, reprioritize, advance, or regress COMPLETE → USE/BUILD.
3. Continuous observe → evaluate → execute → observe loop.
4. Real mission work always outranks heartbeat activity.
5. Evidence is mandatory for any claim ≥ 9.

---

*This repository exists so the strategy engine itself is subject to the same rigorous, evidence-based standards it enforces on every mission.*
