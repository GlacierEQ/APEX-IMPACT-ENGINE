# AMBITION — Executable Pressure, Not Motivation

Ambition inside APEX-IMPACT-ENGINE is **bounded, evidence-driven execution pressure**. It is never motivational prose and never grants new authority.

## Core Rule

When the same `mission_state_ref` is observed again **without verified movement**, the engine accumulates pressure. That pressure:

- raises the relative value of actions that change target state, unblock the mission, create external leverage, or produce actual result power;
- heavily penalizes repeating the same action against an unchanged mission state;
- can force a material route change when another executable route exists;
- never makes heartbeat / status / summary work selectable;
- resets only when the mission-state reference actually changes **or** verified progress is explicitly recorded;
- can persist across process restarts via `APEX_AMBITION_STATE`.

## What Ambition Is Not Allowed To Do

- Grant authority the Operator has not already given
- Rewrite the bound mission
- Bypass provider or executable boundaries
- Treat activity volume, recency, or status updates as progress
- Manufacture evidence or scores

## Persistence

```bash
export APEX_AMBITION_STATE=~/.apex/ambition-state.json
PYTHONPATH=src python -m apex_impact.cli --ambition-state "$APEX_AMBITION_STATE" examples/mission.json
```

The state file is a simple JSON receipt of:

- last observed mission_state_ref
- consecutive no-progress cycles
- last selected action
- repeated-action cycles
- current ambition_pressure (0–10 scale)

## Interaction with Phase Gates

Ambition operates **inside** the current phase. It does not override BUILD / USE / POLISH / COMPLETE determination. It only changes which *executable* action is preferred when the mission state has not moved.

## Self-Application

If the engine is run repeatedly against its own repository state with no material change, ambition pressure must rise and eventually prefer route changes that produce real evidence (tests green, real mission results, durable handoff improvements) over internal status work.
