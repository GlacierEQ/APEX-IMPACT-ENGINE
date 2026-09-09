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

## Intended Composition Edges

```text
mega-skills pipelines / mega pyramids
        │
        │  (candidate actions / capability targets)
        ▼
APEX-IMPACT-ENGINE  ──────►  phase decision + selected action
        │                         │
        │                         │
        ▼                         ▼
aspen-grove-core / runtime     Genius-Mastery progress cycles
```

- This engine **selects** among actions that may themselves be mega-skills, compound skills, or pipeline steps.
- It **does not** redefine or fork those skills.
- Genius-Mastery may treat phase transitions emitted by this engine as durable progress events.
- aspen-grove-core (or equivalent) supplies the observation surface the engine continuously evaluates.

## Discovery Expectations

Any system that wants to treat this engine as a peer should:

1. Read `FOUNDATION.md` for the non-negotiable contracts.
2. Treat phase state and selected-action records as first-class signals.
3. Never bypass the evidence requirement when reporting quality scores into the engine.

## Local Skill Linkage (this session)

In the current operator environment the following skills are already loaded and relevant:

- `elite-code-quality` — hierarchical hyper powerful code quality upgrade (used to build this foundation)
- `skill-connector-router` — dynamic skill/connector routing
- `genius-lawyer-aggressive-litigation` — available when legal/forensic pressure is required
- `postgres-sql` — when data-layer work appears

These are session-level; the durable mesh remains the GitHub peers above.

## Update Rule

When a new high-value peer is added or an existing edge changes semantics, update this file in the same change that introduces the dependency. Stale mesh declarations are treated as a documentation quality defect under POLISH.
