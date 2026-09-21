# MESH — Peer Links & Composition Contracts

APEX-IMPACT-ENGINE is a mesh citizen. This file declares the known high-value peers and the intended composition edges.

## Primary Peers

| Peer | Role relative to this engine | Link |
|------|------------------------------|------|
| **mega-skills** | Capability hierarchy (atomic / compound / mega) + deep-work pipelines. Supplies candidate actions and executable pyramids. | https://github.com/GlacierEQ/mega-skills |
| **Genius-Mastery** | Teacher-forge + family kernel + progress orchestration. Consumes phase decisions; can synthesize entities that use this engine. | https://github.com/GlacierEQ/Genius-Mastery |
| **aspen-grove-core** | Canonical spiral / memory / swarm boot. Provides runtime and memory substrate on which the engine can observe state. | https://github.com/GlacierEQ/aspen-grove-core |
| **apex-core** | Master orchestration, config, test suites, security tools. | https://github.com/GlacierEQ/apex-core |
| **apex-control-plane** | Worker registry + capacity dispatch. | https://github.com/GlacierEQ/apex-control-plane |
| **monolith** | Library roadmap, domain map, control-plane documentation. | https://github.com/GlacierEQ/monolith |
| **pro-code** | Pro-code standards / APEX control surface. | https://github.com/GlacierEQ/pro-code |

## Deep-Work Pipeline Edges (from mega-skills)

These pipelines are treated as high-value candidate action sources or mission envelopes:

| Pipeline | Family | Typical use by this engine |
|----------|--------|----------------------------|
| `inception-to-deployment` | master | Full-span mission that must clear BUILD → USE → POLISH → COMPLETE |
| `control-plane` | control-plane | Always-on session / guarded operating loop |
| `memory-fleet` | memory-fleet | Recon + memory synthesis when observation surface is incomplete |
| `change-swe` | change-swe | Bounded repair when system quality drops below 9 |
| `cultivate-main` | change-swe | Safe merge of unique work into living main |
| `anthropic-applied-ai-readiness` | mission | Career / evidence backbone missions |

The engine ranks concrete executable steps; it does not redefine the pipeline DAGs.

## Intended Composition Edges

```text
mega-skills pipelines / mega pyramids
        │
        │  (candidate actions / capability targets)
        ▼
APEX-IMPACT-ENGINE  ──────►  phase decision + selected action + ambition pressure
        │                         │
        │                         │
        ▼                         ▼
aspen-grove-core / runtime     Genius-Mastery progress cycles
```

- This engine **selects** among actions that may themselves be mega-skills, compound skills, or pipeline steps.
- It **does not** redefine or fork those skills.
- Genius-Mastery may treat phase transitions and ambition pressure signals as durable progress events.
- aspen-grove-core (or equivalent) supplies the observation surface the engine continuously evaluates.

## Discovery Expectations

Any system that wants to treat this engine as a peer should:

1. Read `FOUNDATION.md` for the non-negotiable contracts.
2. Treat phase state, selected-action records, and ambition pressure as first-class signals.
3. Never bypass the evidence requirement when reporting quality scores into the engine.
4. Prefer feeding real mission snapshots over synthetic heartbeat traffic.

## Local Skill Linkage (operator session)

Relevant session-level skills that frequently compose with this engine:

- `elite-code-quality` — hierarchical hyper powerful code quality upgrade
- `skill-connector-router` — dynamic skill/connector routing
- `genius-lawyer-aggressive-litigation` — when legal/forensic pressure is required
- `postgres-sql` — when data-layer work appears

These are session-level; the durable mesh remains the GitHub peers above.

## Update Rule

When a new high-value peer is added or an existing edge changes semantics, update this file in the same change that introduces the dependency. Stale mesh declarations are treated as a documentation quality defect under POLISH.
