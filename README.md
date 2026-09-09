# APEX-IMPACT-ENGINE

Executable strategy engine that continuously evaluates materially changed state and enforces:

**BUILD → USE → POLISH → COMPLETE**

## Binding Contract

- **BUILD**: Improve only purpose-critical system deficiencies until every required, evidenced quality dimension is ≥ 9.
- **USE**: Once the system is exceptional, stop improving the machinery and use it against the real mission until actual results are ≥ 9 and the objective is materially achieved.
- **POLISH**: Once excellent results exist, close residual completeness, presentation, durability, handoff, and finish quality until ≥ 9.
- **COMPLETE**: Only when system quality + result quality + completion quality independently clear evidenced 9+ gates. Then preserve the gain and move to the next mission.

The engine deliberately refuses to let several 10s hide an 8.9.

Quality scores above the threshold cannot pass without evidence references. A claimed 9.8 with no evidence becomes **UNVERIFIED**, not “exceptional.”

## Action Selection Philosophy

The selector rewards:

- operator impact
- external leverage
- actual result power
- blocker removal
- capability / evidence / opportunity gain
- compounding value
- urgency and readiness

It heavily penalizes:

- `heartbeat_only`
- `support_only`
- `recency_only`
- `duplicated_representation`
- `speculative_architecture`
- `easy_to_verify_only`

An action that neither changes target state nor genuinely unblocks the mission is not selectable.

## Current Status

- Local canonical path: `/Users/kcbflux/APEX_SYSTEM/ENGINES/APEX-IMPACT-ENGINE`
- Initial commit (local): `20348ddff2232da70483cf47db2e7653a0d424c1`
- 11 behavioral tests passing (strict 9+ gates, phase transitions, anti-heartbeat selection, dynamic invalidation)
- Remote created and initialized with this handoff document

## Next Required Action (Human)

Push the local source so the system quality gate becomes publicly evidenced:

```bash
cd /Users/kcbflux/APEX_SYSTEM/ENGINES/APEX-IMPACT-ENGINE
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/GlacierEQ/APEX-IMPACT-ENGINE.git
git branch -M main
git push -u origin main
```

After the push, the engine can be evaluated under its own rules by any third party.

## Design Invariants

- Strategy is live state, not a frozen plan.
- Material changes can invalidate previously selected actions, reprioritize, advance, or regress COMPLETE back to USE/BUILD.
- Continuous observe → evaluate → execute → observe loop.
- Real mission work always outranks heartbeat activity.

---

*This repository exists to make the strategy engine itself subject to the same rigorous, evidence-based standards it enforces on every mission.*
