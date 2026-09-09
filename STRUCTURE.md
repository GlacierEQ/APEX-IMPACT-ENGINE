# STRUCTURE

## Current Canonical Layout

```text
APEX-IMPACT-ENGINE/
├── .github/workflows/ci.yml      # Remote behavioral verification
├── .gitignore
├── AGENTS.md                     # Agent execution contract
├── README.md                     # Constellation-aware entry point + binding contract
├── FOUNDATION.md                 # Durable architectural + quality foundation
├── MESH.md                       # Peer links and composition contracts
├── STRUCTURE.md                  # This file
├── docs/
│   └── QUALITY_GATES.md          # Evidence-required scoring rules
├── examples/
│   └── mission.json              # Ready-system → USE demonstration
├── src/apex_impact/
│   ├── __init__.py
│   ├── cli.py                    # Snapshot → decision CLI
│   ├── engine.py                 # Phase machine + impact-aware action selector
│   ├── model.py                  # Evidence/quality/action/impact contracts
│   └── runner.py                 # Observe → evaluate → execute continuation loop
├── tests/
│   └── test_engine.py            # 11 binding behavioral tests
└── pyproject.toml                # Installable package + `apex-impact` CLI
```

## Runtime Responsibility

`model.py` defines qualified state. `engine.py` determines BUILD / USE / POLISH / COMPLETE from evidenced quality floors and ranks actions under live impacts. `runner.py` repeatedly re-observes after execution so material changes can advance, regress, invalidate, or reprioritize strategy. `cli.py` provides a machine-consumable decision boundary for peers.

## Foundation Responsibility

README, FOUNDATION, MESH, QUALITY_GATES, and AGENTS are part of the completion-quality surface, but they do not substitute for execution. They must stay aligned with the implementation and current provider state.

## Invariant

Stale foundation documents are POLISH defects. Missing or weakened executable enforcement is a BUILD defect. Once the engine is evidenced ≥9 for its necessary purpose, further internal improvement must yield to using the engine against real GlacierEQ missions until result quality reaches ≥9.
