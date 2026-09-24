# CLAUDE.md — NOMAD

Persistent working instructions for Claude Code. The approved engineering specification in `docs/` takes precedence over this file. If the two disagree, fix this file; do not treat it as a second spec.

## Project

NOMAD is a portable, offline-first field computer. Principle: **assume the infrastructure is gone.**

Priorities, in order: function, reliability, serviceability, modularity, mechanical simplicity, manufacturability, offline capability, expandability, aesthetics. Never trade the first eight for appearance. Prefer a simple, robust mechanism over a clever one unless the complexity buys a substantial real benefit.

## Roles

- **Project owner:** the final decision-maker.
- **Engineering assistant:** architecture, requirements, tradeoffs.
- **Claude Code:** turns approved requirements into CAD, project files, docs and automation.

## Approval gate

Do not silently change: overall architecture, the solar concept, display orientation, keyboard/trackpad layout, battery location, major module placement, mechanism architecture, motors (none without approval), or subsystem scope. If a change seems necessary, explain the problem, propose alternatives with tradeoffs, and wait. Small, reversible changes that are consistent with the spec may be made autonomously.

## Current status

- Phase: V1 mechanical architecture. Prototype: **P0.1** (mechanical proof of concept).
- Phase 0 (workspace setup) is done. No Onshape document or geometry exists yet.
- Open decisions are listed in `docs/decisions.md`.

## Sources of truth

| What | Where |
|---|---|
| Parametric CAD | Onshape (master) |
| FeatureScript snapshots | `CAD/featurescript/` (copies of the Onshape Feature Studios; Onshape wins on conflict) |
| Exports (STEP/STL/3MF/drawings) | `CAD/exports/`, `CAD/drawings/`, or releases: derived, never authoritative |
| Specifications | `docs/` |
| Decisions | `docs/decisions.md` |
| Build/test history | `docs/build-log.md`, `prototypes/<rev>/` |
| Software | Local Git repo; GitHub `origin` is the remote and backup |

## Onshape MCP constraints

The connected Onshape MCP is **FeatureScript-only**. It can:
- create and list Feature Studios (given a document ID and workspace ID)
- read and write Feature Studio code
- test code in a scratch Part Studio
- search the FeatureScript docs

It **cannot** list or create documents, Part Studios, Variable Studios or Assemblies. It cannot insert features into a user Part Studio, read existing geometry, create mates, or export. Do not assume other operations exist.

- The project owner supplies document URLs, inserts custom features, and does exports.
- Every tool call spends the owner's Onshape API allocation: 2,500 requests per annual cycle. Test before writing, batch work, and check `get_api_usage` periodically.
- `put_featurescript` overwrites the entire Feature Studio: always `get_featurescript` first.
- Before any CAD change: inspect, understand dependencies and downstream effects, and never destroy working geometry for convenience.

## CAD conventions

- Model in three levels: **envelope**, then **interface** (holes, bosses, connectors, clearances), then **detail**. Add detail only where it affects fit, motion, strength, assembly, manufacturing, cable routing or cooling.
- Every uncertain dimension is a named parameter (UPPER_SNAKE_CASE, mm), never a hidden constant. Record each one in `docs/mechanical-spec.md` with its status (verified / provisional / TBD) and source.
- Use clear feature and part names. Name keep-out volumes `KEEPOUT_*` and envelopes `ENV_*`.
- Avoid giant monolithic feature histories. Split them into logical modules.
- Target FDM PETG. Watch wall thickness, overhangs, print orientation, supports, heat-set inserts and tolerances for repeated disassembly. Use metal for structural shafts and pins.
- Keep a small fastener family (M2.5, M3) with heat-set inserts for serviced joints. Match the fastening method to the joint: screws for structure, clips for frequent access, captive/quarter-turn fasteners for service panels, magnets and pins for covers.
- Every important cable gets an intentional path, with bend radius, strain relief and protection. Never route wires through gears. No slip rings in V1.
- The battery must stay removable and serviceable. Never block cooling airflow.

## Reporting

Report progress under: **COMPLETED / CURRENT MODEL / ASSUMPTIONS / PROBLEMS / NEXT ACTION / APPROVAL REQUIRED**.
Always say which of these a claim is: *modeled*, *simulated*, *inferred*, *physically tested* or *measured*. They are not equivalent. Physical testing is authoritative for fit and motion.

## Git

- Default branch: `main`. Remote: `origin` (GitHub).
- Commit messages are meaningful and prefixed with the revision, e.g. `P0.1: add solar cassette envelope`. Never use "update", "test" or "final2".
- Summarize changes before major commits. Push only with owner approval.
- Never delete files, rewrite history, force-push, remove branches or discard changes without explicit approval.
- Never commit secrets, tokens or personal information. `.claude/settings.local.json` is git-ignored.

## Revision naming

P0.1, then P0.1.x (sub-revisions), P0.2 (physical-measurement revision), P1 (functional chassis), P1.x, V1 (validated prototype). For each major change, record what changed, why, what problem it solved, and what tradeoff it introduced (in `docs/decisions.md` / `docs/build-log.md`).
