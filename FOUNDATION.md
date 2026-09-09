# FOUNDATION — APEX-IMPACT-ENGINE

This document is the durable architectural and quality foundation. It is intended to remain stable even as implementation details evolve.

## 1. Purpose

APEX-IMPACT-ENGINE is the live strategy evaluator for high-stakes missions. It answers, under continuous observation of material state:

> Given everything that has changed, what is the single highest-impact next action that advances the real objective while respecting the BUILD → USE → POLISH → COMPLETE regime?

It is deliberately narrow. It does not own capability libraries, entity synthesis, or long-running orchestration. Those live in peer systems (mega-skills, Genius-Mastery, aspen-grove-core, etc.). This engine owns **phase judgment + action selection under evidence discipline**.

## 2. Phase State Machine

```text
                  ┌───────────────┐
                  │     BUILD       │
                  │  (system ≥9)   │
                  └────────┬───────┘
                             │
                             ▼
                  ┌───────────────┐
                  │      USE        │
                  │ (results ≥9)    │
                  └────────┬───────┘
                             │
                             ▼
                  ┌───────────────┐
                  │    POLISH       │
                  │ (completion ≥9) │
                  └────────┬───────┘
                             │
                             ▼
                  ┌───────────────┐
                  │   COMPLETE      │
                  │ (all gates)     │
                  └────────┬───────┘
                             │
              (new failure evidence)
                             │
                             ▼
                        back to BUILD / USE
```

Regression is first-class. New material evidence can force COMPLETE → USE or COMPLETE → BUILD. There is no permanent “done.”

## 3. Evidence Discipline

Any quality claim ≥ 9.0 must carry:

- Explicit dimension name
- Numeric score
- One or more concrete evidence references (file path, test name, log URI, external result ID, etc.)
- Timestamp / observation context

Absence of evidence → status = `UNVERIFIED`.  
UNVERIFIED scores never satisfy a gate.

## 4. Action Selection Invariants

1. Only actions that change target state or genuinely unblock the mission are candidates.
2. Heartbeat / support / recency / easy-to-verify work is heavily down-weighted or blocked.
3. External leverage and operator impact dominate internal cleanliness when the system is already in USE or later.
4. The selector must be able to explain, for the chosen action, which quality dimensions or mission variables it advances.

## 5. Composition Rules (Constellation)

This engine is a **consumer and producer of state**, not a capability owner.

- It may *invoke* mega-skills / compound skills / pipelines as candidate actions.
- It may *emit* phase decisions and selected-action records that Genius-Mastery progress cycles or aspen-grove runtimes can consume.
- It must never silently own or fork the skill definitions that live in `mega-skills`.
- Peer discovery and mesh membership are declared in `MESH.md`.

## 6. Quality Philosophy (Self-Application)

The engine is required to apply its own standards to itself:

- System quality of the engine code/tests/docs must clear ≥9 with evidence before it is allowed to live in USE for high-stakes missions.
- Result quality is measured by real external outcomes (not internal activity).
- Completion quality includes third-party handoff, documentation, and durability of the gains.

## 7. Non-Goals

- Owning the mega-skill hierarchy or pipeline definitions
- Replacing Genius-Mastery entity synthesis or progress kernel
- Becoming a general-purpose agent runtime
- Optimizing for “looking busy” or high activity volume

## 8. Evolution Rule

Any change that weakens the evidence requirement, softens the anti-heartbeat bias, or allows unverified scores to satisfy gates is a **regression** and must be treated as a BUILD-blocking defect.
