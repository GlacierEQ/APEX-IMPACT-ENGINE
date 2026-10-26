# SOURCE-BACKED PHASE AND QUALITY CONTRACT

This contract applies to APEX-IMPACT-ENGINE and the missions it evaluates. The binding requirement is **truthful evidence and actual mission progress**, never a universal numeric rating.

## Source-specific phase conditions

| Phase | Condition | Required action |
|---|---|---|
| BUILD | Neither referenced system evidence nor an independently executable target-changing/unblocking action is available | Recover working capability, source references, or an executable alternate route |
| USE | Capability has referenced evidence **or** an independent mission action is executable; objective remains outstanding | Execute actual mission work |
| POLISH | Objective is achieved and required result references are present, but completion references are missing | Resolve only the missing completion proof |
| COMPLETE | Objective is achieved and required result and completion evidence references are present | Preserve success and its receipts; move to the next authorized objective |

A declared metric's `score` can guide prioritization, but **8.9 is not a global stop condition**. The engine accepts evidence-reference presence as a structural phase signal. Actual source provenance and provider-side verification must be checked separately whenever a material claim depends on them.

## Required evidence domains

| Domain | Examples of source facts | What it proves |
|---|---|---|
| System | Relevant passing behavioral tests, verified accessible tool, working capability receipt | Capability for the specific operation |
| Result | Source-native provider receipt, material state change, docket entry, GitHub commit | The particular outcome claimed |
| Completion | Handoff receipt, complete artifact readback, documented closure of the requested deliverable | The particular completion claim |

Additional mission-specific dimensions may be declared. Missing references to required result or completion metrics are reported as `UNVERIFIED`, scoped to the named metric. Evidence-reference presence does not prove that a URL, receipt or test actually says what a claim alleges.

## Positive and negative evidence

1. **Solution precedence:** A successful recovery with a verified readback supersedes the earlier failed attempt as current state. Retain both chronologically.
2. **No automatic regression:** An unrelated provider failure does not reopen a completed objective, remove a working capability or create a universal execution gate.
3. **Real losses matter:** If the objective is no longer achieved or required evidence is genuinely missing, reopen only that corresponding outcome or handoff step.
4. **Alternative route:** One failed connector call initiates materially different authorized routes. Continue independent executable work without re-requesting already satisfied prerequisites.
5. **Provider facts control:** Projected task statuses, stale memory and subjective quality numbers cannot overwrite a source-native receipt.

## Anti-patterns

- Averaging high scores to hide genuinely missing required evidence
- Enforcing `>= 9` as an invented prerequisite to use functioning capabilities
- Converting transient errors into permanent prohibitions
- Treating activity count, heartbeat or status reports as results
- Treating a repository instruction edit as deployment or provider-verified behavior
- Claiming completed results based solely on an uninspected evidence-reference string

## Engine self-verification

Before claiming the implementation is tested, run its actual behavioral suite and inspect output. Before claiming integration, review dependent interfaces and the changed head. Before claiming deployed/operational, obtain the corresponding runtime/provider receipt.

## Change control

Preserve source history, source-specific confidence, security and provider permissions. Updates that erase verified progress, invent proof, or reintroduce arbitrary score-based execution gates are defects. The source-native reconciliation and the highest-value executable mission objective remain the governing behavior.
