# STRUCTURE

## Current Canonical Layout

```text
APEX-IMPACT-ENGINE/
├── .github/workflows/ci.yml
├── LICENSE
├── AGENTS.md
├── README.md
├── FOUNDATION.md
├── MESH.md
├── STRUCTURE.md
├── GENIUS.yaml
├── ROLE.yaml                      # StrategyEvaluator identity
├── pyproject.toml
├── docs/
│   ├── QUALITY_GATES.md
│   ├── AMBITION.md
│   └── OPERATOR.md
├── examples/
│   ├── mission.json                 # USE over heartbeat
│   ├── mission_regression.json      # COMPLETE → BUILD
│   └── mission_ambition.json        # route change under pressure
├── src/apex_impact/
│   ├── engine.py                    # phase + selector + ambition
│   ├── model.py
│   ├── cli.py
│   └── runner.py
├── tests/test_engine.py
├── capabilities/
│   ├── STACK.yaml                   # hardened anatomy
│   └── GRAPH.yaml                   # nodes + edges
├── interfaces/
│   └── COMPOSITION.yaml             # mega-skills + Genius edges
├── persona/PERSONA.md
├── policy/
├── synthesis/
└── teaching/
```

## Runtime Responsibility

`model.py` defines qualified state.  
`engine.py` determines phase, ranks actions, applies ambition pressure.  
`runner.py` re-observes so material changes can advance or regress strategy.  
`cli.py` is the machine boundary for peers.

## Foundation Responsibility

Contracts, docs, and examples are part of completion quality. They must stay aligned with the live implementation. Stale foundation is a POLISH defect; weakened enforcement is a BUILD defect.
