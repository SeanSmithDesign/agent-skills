---
name: wrap
description: End-of-session wrap-up — heavy capture, retrospective only. Use when done for the day (or longer). Runs reconciliation, commits, ticket tracker, memories, orchestrator state, session notes, long-term notes. No pickup prompt — use /wrap-continue for that.
license: MIT
metadata:
  version: 2.0.0
  category: workflow
  domain: session-management
  status: stable
  platforms: All
keywords:
  - wrap
  - session
  - end
  - ship
  - done
  - cleanup
  - notes
  - commit
  - push
---

# Wrap Session

End-of-session wrap-up. Heavy capture. Use when the session is finished and the next pickup may be hours or days away.

Triggered by: `/wrap`, "wrap it up", "wrap up", "done for now", "end session".

If you're recycling context mid-task and continuing the same work, use `/wrap-continue` instead.

Suggests what's worth saving before closing. Every step is optional — assess what's relevant and skip what isn't. Don't force a push or commit if nothing meaningful changed.

## Suggested Steps

The sequence follows an Information Lifecycle (L1 → L2 → L3): reconcile first (orchestrator threads only), then code so commits have SHAs, then hot memory, then the session log, then long-term threads. Each layer references the one below it.

### 1. Plan Reconciliation (orchestrator threads only)

Verify every subagent delegated this session delivered what was asked. Run BEFORE commits — the reconciliation result shapes everything downstream.

**How to verify:**

- `git log` for recent commits → confirm each delegation produced a commit (and a push)
- Re-read each delegation prompt → check "Verification" and "After Completion" sections. Did the subagent run tests? Commit? Push?
- Compare against plan or ticket scope → any requirement silently dropped?
- Check for uncommitted work in the tree — subagents sometimes leave staged/unstaged changes

**Two paths when a gap is found:**

- **Fix now** — small gaps (missing commit, unstaged file, one failing test): spawn a focused follow-up subagent. Wait for it to finish, then continue the wrap.
- **Defer** — larger gaps (missing feature, broken behavior, architectural rework): add to `ORCHESTRATOR.md` under **In-Flight Work**. Flag it in the final summary.

Skip entirely on non-orchestrator threads.

### 2. Commit & Push code (if dirty)

Check `git status`. If there are uncommitted code changes worth keeping, suggest a commit + push. If the tree is clean or changes are trivial, skip.

First code step so every downstream artifact (ticket tracker, session notes, long-term notes) can reference real commit SHAs.

### 3. Ticket Tracker (if tickets were worked)

If the session completed or changed the status of any tracked tickets, suggest updating them. Check MEMORY.md or CLAUDE.md for the project's issue tracker. Match commits against known ticket IDs.

Skip if the project doesn't use a ticket tracker or no tickets were relevant.

### 4. Memories (L1 — if new learnings surfaced)

Save feedback, decisions, or references that future sessions should know about. Don't save things derivable from code or git history. Update `MEMORY.md` index for new entries.

Done before session notes so notes can reference saved memory files. Skip if nothing non-obvious was learned.

### 5. Orchestrator State (orchestrator threads — mandatory if any delegation or decision happened)

Update `ORCHESTRATOR.md` in `.claude/projects/<path>/memory/` with architecture changes, decisions, fragile areas, recent delegations. Keep under 300 lines. Prune stale Decision Log and Recent Delegations entries.

If step 1 deferred any gaps as follow-up tasks, record them in **In-Flight Work** here.

**This update is mandatory if ANY of the following are true:**

- Any subagent was delegated this session (whether it succeeded or failed)
- Any architectural decision was made
- Any in-flight work was added or completed
- Step 1 deferred any gaps (they must land in ORCHESTRATOR.md)
- The session produced commits (code shipped that should be reflected in context)

Skip ONLY if not an orchestrator thread, AND no subagents were delegated, AND no decisions were made, AND no in-flight work changed.

> **Gotcha:** A session that ends cleanly after shipping a milestone still needs ORCHESTRATOR.md updated — clean endings are not an excuse to skip. The skip is only valid for pure-research or pure-chat sessions where nothing changed.

### 6. Session Notes (L2 — if meaningful work happened)

Append to `docs/SESSION_NOTES.md` if the session produced commits, decisions, or learnings worth recording. Include commit SHAs from step 2, ticket IDs touched from step 3, references to memory files saved in step 4, and any deferred gaps from step 1.

Quick chat sessions or minor tweaks don't need notes.

### 7. Long-Term Notes (L3 — if project state changed significantly)

Update the project's thread in your long-term notes system with current state, what's next, open questions. This is the narrative arc — summarize the session notes from step 6, don't duplicate them.

Skip for small sessions that don't change the project's trajectory.

**Don't run Session Notes AND Long-Term Notes for the same session.** Pick one:

- **Coding-only projects** → Session Notes (git-searchable, co-located with code)
- **Cross-domain or life projects** → Long-Term Notes (broadly searchable, broader context)

### 8. Final Commit & Push (if steps above created docs)

Commit any session notes, memory updates, orchestrator state, or long-term note changes created in steps 4–7. Push. Separate commit from step 2 so code and documentation commits are distinct in history.

## Output Format

After completing selected steps, present the wrap summary box and table.

```
                                               _____
                                              |     |
  ╭───────────────────────────────────────────[_____]───────────────────────────────────────────╮
  │                             ┌────────────────────────────────────────────────────────────┐  │
  │                             │                                                            │  │
  │   · · · · · · · · · · · ·   │                                                            │  │
  │   · · · · · · · · · · · ·   │               ________ ______ _______ ______               │  │
  │  · ◉ ◉ ◉ ◉ ◉ ◉ ◉ ◉ ◉ ◉ ◉ ·  │              |  |  |  |   __ \   _   |   __ \              │  │
  │  ·◉ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ◉·  │              |  |  |  |      <       |    __/              │  │
  │  ·◉ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ◉·  │              |________|___|__|___|___|___|                 │  │
  │  ·◉ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ◉·  │                                                            │  │
  │  ·◉ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ◉·  │                      _______ _______                       │  │
  │  ·◉ ○ ○ ○ ○ ○ ● ○ ○ ○ ○ ◉·  │                     |_     _|_     _|                      │  │
  │  ·◉ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ◉·  │                      _|   |_  |   |                        │  │
  │  ·◉ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ◉·  │                     |_______| |___|                        │  │
  │  ·◉ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ◉·  │                                                            │  │
  │  ·◉ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ◉·  │                       _______ ______                       │  │
  │  · ◉ ◉ ◉ ◉ ◉ ◉ ◉ ◉ ◉ ◉ ◉ ·  │                      |   |   |   __ \                      │  │
  │   · · · · · · · · · · · ·   │                      |   |   |    __/                      │  │
  │   · · · · · · · · · · · ·   │                      |_______|___|                         │  │
  │                             │                                                            │  │
  │                             │                                                            │  │
  │                             └────────────────────────────────────────────────────────────┘  │
  ╰─────────────────────────────────────────────────────────────────────────────────────────────╯


  ┌────────────────┬──────────────────────────────────────────────────────────────────────────┐
  │ Area           │ Status                                                                   │
  ├────────────────┼──────────────────────────────────────────────────────────────────────────┤
  │ Reconciliation │ 4/4 delegations verified; 1 deferred → ORCHESTRATOR.md                   │
  │ Git            │ 3 commits pushed (abc1234..def5678)                                      │
  │ Tickets        │ PRJ-12, PRJ-15 → Done                                                    │
  │ Memories       │ 1 feedback saved                                                         │
  │ Orchestrator   │ Updated                                                                  │
  │ Session Notes  │ Updated                                                                  │
  │ Long-Term      │ Skipped — captured in session notes                                      │
  │ Repo           │ Clean, up to date with origin                                            │
  └────────────────┴──────────────────────────────────────────────────────────────────────────┘
```

The table sits inside the same fenced block as the box so both render as monospace and share a single character grid. Pad every Status cell with trailing spaces so the closing `│` lands at the exact same column as the box's right edge.

Adapt rows to what's relevant. Skip rows for steps that didn't run. The Reconciliation row only appears on orchestrator threads.

## Judgment Calls

- **Short session, no code changes?** Skip everything except maybe a memory if something useful came up.
- **Big session, lots of code?** Run reconciliation (if orchestrator), commits, plus whichever capture artifacts are load-bearing. Don't run every step just because the session was long.
- **Exploratory session, no conclusions?** Maybe just session notes for context if you'll pick it up later.
- **User seems in a hurry?** Commit + push only, skip the rest.
- **Orchestrator thread, gap found in reconciliation?** Fix-now for small gaps. Defer to ORCHESTRATOR.md for larger gaps. Never silently skip a gap.
- **Orchestrator thread, everything clean?** Reconciliation row should say "N/N delegations verified."
- Don't commit empty or trivial session notes just to check a box.
- Don't force-push or push to branches without asking.
