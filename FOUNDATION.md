# FOUNDATION — APEX-IMPACT-ENGINE

This document is the durable architectural and quality foundation. It is intended to remain stable even as implementation details evolve.

## 1. Purpose

APEX-IMPACT-ENGINE is the live strategy evaluator for high-stakes missions. It answers, under continuous observation of material state:

> Given everything that has changed, what is the single highest-impact next action that advances the real objective while respecting the BUILD → USE → POLISH → COMPLETE regime?

It is deliberately narrow. It does not own capability libraries, entity synthesis, or long-running orchestration. Those live in peer systems (mega-skills, Genius-Mastery, aspen-grove-core, etc.). This engine owns **phase judgment + action selection under evidence discipline**.

## 2. Phase State Machine

```text
           ┌────────────────────────────────────────────────┐
           │ BUILD: no referenced system readiness          │
           │ AND no independent executable mission action  │
           └───────────────────────┬────────────────────────┘
                                   │ evidence reference OR executable action
                                   ▼
           ┌────────────────────────────────────────────────┐
           │ USE: objective outstanding; act on real work   │
           └───────────────────────┬────────────────────────┘
                                   │ objective achieved AND result references
                                   ▼
           ┌────────────────────────────────────────────────┐
           │ POLISH: only specific handoff proof is missing │
           └───────────────────────┬────────────────────────┘
                                   │ completion references present
                                   ▼
           ┌────────────────────────────────────────────────┐
           │ COMPLETE: preserve objective and handoff gains │
           └────────────────────────────────────────────────┘
```

**No quality-score gate.** Numeric assessments help prioritize investment; they never become a global prohibition on execution. A failed tool attempt is history about that attempt, not a phase rollback. The engine may reopen USE when the objective is actually no longer achieved, or POLISH when completion evidence is genuinely missing. It must preserve independent verified gains.


## 3. Evidence Discipline

- Keep source-native references for material mission, result, and completion claims: provider IDs, commits, hashes, actual test runs, and acknowledgments.
- Evidence-reference presence is the minimum data-model signal, not independent authentication; validate the actual referenced source before claiming provider verification.
- An unreferenced required result or handoff metric is `UNVERIFIED` and cannot be treated as completed proof, regardless of its score.
- A verified success remains authoritative over an earlier superseded failed attempt. Historical errors remain inspectable but do not silently become active blockers.
- On a real contradiction, scope correction to the affected claim, preserve unrelated finished milestones, and keep executable alternatives available.
- Source-specific factual uncertainty does not imply mission-wide denial. A score below 9/10 is advisory, not a universal gate.


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

The engine must meet the same evidence discipline it expects of missions:

- Behavioral claims are substantiated by focused and full-suite tests of the actual changed head, plus inspectable CI output.
- Operational claims require the applicable provider-native readback; passing tests alone is not deployment or mission success.
- Mission quality is assessed against the Operator's objective, not an invented threshold. Retain working capabilities while improving measured shortcomings.
- Handoff quality includes accurate documentation, durable references, recoverability, and explicit residual gaps.


## 7. Non-Goals

- Owning the mega-skill hierarchy or pipeline definitions
- Replacing Genius-Mastery entity synthesis or progress kernel
- Becoming a general-purpose agent runtime
- Optimizing for “looking busy” or high activity volume

## 8. Evolution Rule

Any change that fabricates source evidence, treats status reports as completed work, erases a verified success, hides a material contradiction, or blocks executable actions behind invented numeric gates is a regression. Fix only the affected fact or implementation and preserve previously verified functionality. Failed connector calls trigger valid alternate routes; they do not establish permanent incapacity.

