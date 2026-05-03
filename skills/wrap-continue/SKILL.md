---
name: wrap-continue
description: Mid-task context reset — light capture, mandatory commit+push, hot-resume pickup prompt. Use when recycling a long-lived thread to free context while continuing the same work. NOT for end-of-day wrap — use /wrap for that.
license: MIT
metadata:
  version: 1.0.0
  category: workflow
  domain: session-management
  status: stable
  platforms: All
keywords:
  - wrap
  - continue
  - context
  - reset
  - checkpoint
  - token
  - compact
  - resume
---

# Wrap + Continue

Mid-task context reset. Light capture. Use when the session is being recycled to free context — the work is NOT done, you're resuming immediately in a fresh thread.

Triggered by: `/wrap-continue`, "wrap continue", "wrap and continue", "checkpoint", "context reset", "trim and continue".

If the session is actually done for the day, use `/wrap` instead — that runs full retrospective capture.

## Steps

### 1. Commit & Push (mandatory)

Check `git status`. Everything uncommitted is at risk when context clears. Commit all meaningful changes and push. This is not optional — if work exists that isn't committed, commit it now before anything else.

If nothing is uncommitted, note it and move on.

### 2. Light Capture (optional — only if non-obvious)

Save feedback, corrections, or decisions that surfaced this session and aren't yet in memory. Keep this short. The bar is: "would I lose this if context cleared right now?"

- New feedback → save to `.claude/projects/<path>/memory/feedback_*.md`
- New reference → save to `reference_*.md`
- Major architectural decision → update `ORCHESTRATOR.md` In-Flight Work section (orchestrator threads only)

Skip if nothing non-obvious came up. Don't run full retrospective — that's `/wrap`.

### 3. Hot-Resume Pickup Prompt

Generate a compact pickup prompt the user can paste at the start of the next thread to restore context exactly where work left off.

The pickup prompt must include:

- **What we're building** — one sentence on the project + task
- **Where we are** — current status, what just shipped (with commit SHA if applicable)
- **What's next** — the immediate next action (specific, not vague)
- **Key context** — anything non-obvious that the next thread won't know from the codebase (design decisions, constraints, open questions, gotchas)
- **Working directory** — the repo path so the next thread can orient immediately

Format the pickup prompt as a fenced code block so it's easy to copy.

## Output Format

```
  ╭─────────────────────────────────────────────────────────╮
  │  ↻  WRAP + CONTINUE                                     │
  ╰─────────────────────────────────────────────────────────╯

  ┌──────────┬──────────────────────────────────────────────┐
  │ Git      │ 2 commits pushed (abc1234..def5678)          │
  │ Capture  │ 1 feedback saved / skipped                   │
  │ Repo     │ Clean, up to date with origin                │
  └──────────┴──────────────────────────────────────────────┘
```

Then the pickup prompt in a fenced block:

```
## Pickup prompt (paste at start of next thread)

[project + task context]
[current status + last commit SHA]
[immediate next action]
[non-obvious context / constraints]
Working directory: ~/Code/[project]
```

## Judgment Calls

- **Nothing uncommitted?** Still generate the pickup prompt — that's the whole point.
- **Big mid-session correction?** Save it as feedback before clearing — future threads will thank you.
- **Orchestrator thread?** Update `ORCHESTRATOR.md` In-Flight Work if the next subagent wave is already planned.
- **User seems in a hurry?** Commit + push + pickup prompt only. Skip capture.
- Keep the whole flow under 5 exchanges. This is speed work, not ceremony.
