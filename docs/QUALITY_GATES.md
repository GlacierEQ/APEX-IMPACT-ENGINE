# QUALITY GATES

These rules are binding for both the engine itself and any mission it evaluates.

## Gate Threshold

Every required quality dimension must reach **≥ 9.0** with valid evidence before the corresponding phase gate can open.

A score of 8.9 (or lower) blocks advancement regardless of how many other dimensions are 10.0.

## Required Dimensions (Minimum Set)

| Dimension | Applies to | Description |
|-----------|------------|-------------|
| System Quality | BUILD | Code, tests, architecture, observability, security of the system under evaluation |
| Result Quality | USE | Measurable external / mission outcomes produced by using the system |
| Completion Quality | POLISH | Handoff readiness, documentation, durability, residual polish, third-party evaluability |

Additional mission-specific dimensions may be declared, but they cannot replace the three above.

## Evidence Requirements

For any claim ≥ 9.0 the following must be present and resolvable:

```yaml
dimension: system_quality
score: 9.4
evidence:
  - type: test
    ref: tests/test_phase_transitions.py::test_complete_to_build_regression
  - type: file
    ref: src/selector/action_scorer.py
  - type: external
    ref: https://example.com/result/12345
observed_at: 2026-09-09T00:00:00Z
```

Missing, unresolvable, or obviously stale evidence → status becomes `UNVERIFIED`.

`UNVERIFIED` scores never satisfy a gate.

## Anti-Patterns Explicitly Forbidden

- Averaging multiple dimensions to hide a weak one
- Using activity volume or recency as a proxy for result quality
- Accepting self-attestation without external or test evidence when the claim is material
- Advancing phase while any required dimension is UNVERIFIED or < 9.0

## Self-Application

When the engine evaluates *itself* (or is evaluated by the constellation):

1. System quality must be evidenced by the test suite + source structure + this documentation set.
2. Result quality must eventually be evidenced by real missions that used the engine and produced measurable outcomes.
3. Completion quality includes the presence of FOUNDATION.md, MESH.md, this file, and a clean third-party clone/run path.

## Change Control

Any modification that lowers the threshold, weakens evidence requirements, or introduces a bypass is a **BUILD-blocking regression** and must be treated as a defect until corrected and re-evidenced.
