# STRUCTURE

## Current Foundation (remote)

```text
APEX-IMPACT-ENGINE/
├── README.md              # Constellation-aware entry point + binding contract
├── FOUNDATION.md          # Durable architectural + quality foundation
├── MESH.md                # Peer links and composition contracts
├── STRUCTURE.md           # This file
├── docs/
│   └── QUALITY_GATES.md   # Evidence-required scoring rules
└── (source pending push from local canonical path)
```

## Expected Layout After Local Source Lands

The local tree at `/Users/kcbflux/APEX_SYSTEM/ENGINES/APEX-IMPACT-ENGINE` is expected to map roughly to:

```text
APEX-IMPACT-ENGINE/
├── README.md
├── FOUNDATION.md
├── MESH.md
├── STRUCTURE.md
├── docs/
│   ├── QUALITY_GATES.md
│   └── …
├── src/                   # Core engine (phase machine, selector, observation loop)
├── tests/                 # 11+ behavioral tests (already green locally)
├── pyproject.toml / requirements / setup
└── …
```

Exact package layout will be finalized when the source is pushed and the elite-code-quality pass is run against the real tree.

## Invariant

The foundation documents (README, FOUNDATION, MESH, QUALITY_GATES) are part of the completion-quality surface. They must remain accurate as the implementation evolves. Stale foundation docs are POLISH defects.
