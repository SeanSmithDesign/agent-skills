---
name: orchestrator-boot
description: Run the orchestrator session-start check — task file, pending updates, project scaffolding, context reads, rehydration. Use on first activation of an orchestrator thread, or when Sean says "boot", "orchestrator boot", "start up", or "get up to speed on this project".
---

# Orchestrator Boot

Session-start sequence for an orchestrator thread. Run once, at first activation.

## 1. Task assignment

If a task-assignment env var (e.g. `GHOSTTIES_TASK_FILE`) points at a task file, read it. It is markdown with YAML frontmatter (title, status, goal, notes). Treat it as this session's work order: present the title and goal, confirm you're picking it up, then continue through the steps below with that as the focus.

## 2. Pending updates

**Never read `PENDING-UPDATES.md` in full at boot** — it is ~4.6k chars to produce a number. Count with grep:

```bash
grep -c 'status: pending' ~/.claude/PENDING-UPDATES.md
```

Surface only — apply nothing. Read the file itself only when the count is non-zero AND Sean wants to act on it.

- 0 → silent
- 1–2 → one line: "Orchestrator has N pending updates."
- 3–4 → same, plus "Run `/orchestrator:update` to review."
- 5+ → "Orchestrator has N pending updates. Backlog is building — recommend `/orchestrator:update` this session."

## 3. Project scaffolding

**Never read `SCAFFOLDING.md` in full at boot** — it is ~10k chars and you need one row. `ls` the project root, then grep only this project's row:

```bash
grep -i '<project-name>' ~/.claude/projects/SCAFFOLDING.md
```

Check for `CLAUDE.md` (required); `DESIGN.md` (required when `*.tsx`, `*.jsx`, `*.swift`, `*.html`, or `apps/*` are present); and the v2.2 grounding set `mission.md`, `brand.md`, `principles.md`. A project absent from the registry is v0 — stay silent unless `DESIGN.md` is missing on a UI project.

- 0 missing → silent
- 1 missing → one line naming the file and why it matters
- 2+ missing, or `DESIGN.md` missing on a UI project → name the inferred version and the gap, and point at `/orchestrator:scaffold`

## 4. Read existing context

**First, check `<memory-dir>/scope.md`.** This is the thread's locked objective, and it must be read before anything else here. If present, surface the Objective line and any unchecked Done-when boxes as part of step 7. If absent, say nothing and do not create one; scope.md is written by working threads, not by boot.

**Rehydration short-circuit — check this BEFORE reading anything.** The point of the short-circuit is to avoid expensive work; do not pay a large read to evaluate it.

```bash
F=<memory-dir>/ORCHESTRATOR.md
[ -f "$F" ] && find "$F" -mtime -7 | grep -q . && grep -qi 'architecture summary' "$F" && echo SHORTCIRCUIT
```

If `SHORTCIRCUIT`: read `ORCHESTRATOR.md` and `MEMORY.md` only, then go straight to step 7. Skip steps 5 and 6.

Otherwise read the fuller set: `MEMORY.md`, `mission.md`, all `agent-*.md`, `general-agent-context.md`, `ORCHESTRATOR.md`.

**Never read at boot in either case:** `ORCHESTRATOR-log.md` (decision-log archive), `INDEX.md`, `tease-capture.md`, `tier_overrides.md`, or any `ORCHESTRATOR-*.md` sibling. These are on-demand.

**If `ORCHESTRATOR.md` exceeds 20,000 chars, say so in step 7** — it has drifted past its cap and needs a prune. Measure with `wc -c`, never in lines: the lines are paragraphs, so a line count hides real growth.

## 5. Scaffold if bare

If no agent files exist: ask "What are you building and who is it for?" → write `mission.md`. Copy the matching `DESIGN.md` template for UI projects. Map the codebase with parallel `explore` agents. Scaffold agent files by lifecycle role — product, experience, craft, build, data, quality as the core set; marketing, content, growth, finance, support, ops added as those stages activate.

## 6. Build the mental model

Architecture (layers, data flow, key abstractions) · conventions · fragile areas and known coupling · test coverage and patterns · build and deploy pipeline.

## 7. Present

Summarize for confirmation before doing any work.
