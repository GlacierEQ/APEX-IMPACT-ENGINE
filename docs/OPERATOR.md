# OPERATOR RUNBOOK

How to use APEX-IMPACT-ENGINE against real missions.

## Quick Start

```bash
git clone https://github.com/GlacierEQ/APEX-IMPACT-ENGINE.git
cd APEX-IMPACT-ENGINE
PYTHONPATH=src python -m apex_impact.cli examples/mission.json
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Real Mission Loop

1. **Prepare a mission snapshot** (JSON) that contains:
   - current quality scores with evidence for system / result / completion
   - `objective_achieved` boolean
   - candidate actions with scores, flags, and `changes_target_state` / `unblocks_mission`
   - optional `impacts` that can invalidate or re-score actions
   - optional `previous_phase` and `mission_state_ref`

2. **Run the engine**

```bash
export APEX_AMBITION_STATE=~/.apex/ambition-state.json
PYTHONPATH=src python -m apex_impact.cli --ambition-state "$APEX_AMBITION_STATE" path/to/mission.json
```

3. **Act on the decision**
   - The selected action is the only recommended next step.
   - Heartbeat / support / status-only actions will be suppressed or heavily penalized.
   - If ambition pressure is rising, prefer actions that actually move the mission state.

4. **Record verified progress**
   - When real external movement occurs, update the mission snapshot (new evidence, new scores, new `mission_state_ref`).
   - Optionally call `record_verified_progress` so ambition pressure resets cleanly.

5. **Re-observe**
   - Feed the updated snapshot back into the engine.
   - Material new evidence can regress COMPLETE → USE or COMPLETE → BUILD. Do not protect the old phase label.

## Composition with Mega-Skills & Pipelines

Candidate actions may be (or may invoke):

- Atomic or Compound Skills from `GlacierEQ/mega-skills`
- Steps inside a deep-work pipeline (`inception-to-deployment`, `control-plane`, `change-swe`, etc.)
- Genius-Mastery progress codes / synthesis operations

The engine does **not** own those definitions. It only ranks which of the currently executable candidates has the highest real impact under the current phase and ambition pressure.

## Quality Self-Check Before High-Stakes USE

Before trusting the engine on a high-stakes mission:

- [ ] `python -m unittest discover -s tests -v` is green
- [ ] Example mission resolves to USE and selects the real-work action over heartbeat
- [ ] FOUNDATION.md, MESH.md, QUALITY_GATES.md, and AGENTS.md still match implementation
- [ ] Any claimed system quality ≥ 9 has resolvable evidence

If any of the above fail, the engine itself is still in BUILD.
