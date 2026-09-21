# STRUCTURE

## Current Canonical Layout

```text
APEX-IMPACT-ENGINE/
├── .github/workflows/ci.yml          # Remote behavioral verification
├── .gitignore
├── LICENSE                           # MIT
├── AGENTS.md                         # Agent execution contract
├── README.md                         # Constellation entry + binding contract + ambition
├── FOUNDATION.md                     # Durable architectural + quality foundation
├── MESH.md                           # Peer + pipeline composition contracts
├── STRUCTURE.md                      # This file
├── GENIUS.yaml                       # Genius family contract
├── ROLE.yaml
├── pyproject.toml                    # Installable package + apex-impact CLI
├── docs/
│   ├── QUALITY_GATES.md              # Evidence-required scoring rules
│   ├── AMBITION.md                   # Executable ambition pressure contract
│   └── OPERATOR.md                   # Human/agent runbook for real missions
├── examples/
│   ├── mission.json                  # Ready-system → USE demonstration
│   └── mission_regression.json       # COMPLETE → BUILD under new failure evidence
├── src/apex_impact/
│   ├── __init__.py
│   ├── cli.py                        # Snapshot → decision CLI
│   ├── engine.py                     # Phase machine + impact-aware selector + ambition
│   ├── model.py                      # Evidence / quality / action / impact contracts
│   └── runner.py                     # Observe → evaluate → execute loop
├── tests/
│   └── test_engine.py                # Binding behavioral tests
├── capabilities/                    # Genius capability anatomy
├── interfaces/                      # Composition contracts
├── persona/
├── policy/
├── synthesis/
└── teaching/
```

## Runtime Responsibility

`model.py` defines qualified state.  
`engine.py` determines BUILD / USE / POLISH / COMPLETE from evidenced quality floors, ranks actions under live impacts, and applies bounded ambition pressure.  
`runner.py` repeatedly re-observes after execution so material changes can advance, regress, invalidate, or reprioritize strategy.  
`cli.py` provides a machine-consumable decision boundary for peers.

## Foundation Responsibility

README, FOUNDATION, MESH, QUALITY_GATES, AMBITION, OPERATOR, AGENTS, and LICENSE are part of the completion-quality surface. They do not substitute for execution. They must stay aligned with the implementation and current provider state.

## Invariant

Stale foundation documents are POLISH defects.  
Missing or weakened executable enforcement is a BUILD defect.  
Once the engine is evidenced ≥9 for its necessary purpose, further internal improvement must yield to using the engine against real GlacierEQ missions until result quality reaches ≥9.
