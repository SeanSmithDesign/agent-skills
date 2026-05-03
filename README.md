# agent-skills

Skills I use to run Claude Code as a designer. Not a framework — a process snapshot.

---

## What's here

Two families. Six skills. All opinionated.

### Wrap family — session hygiene

Every Claude Code session ends the same two ways: you're done for the day, or you're not done but the context window is getting expensive. These are different situations that need different behavior.

**`/wrap`** — End-of-session. Heavy capture. Runs in this order: plan reconciliation (if orchestrator), commit and push, ticket tracker, memories, orchestrator state, session notes, long-term notes. The goal is to leave nothing on the table — every decision, every commit SHA, every deferred task captured before the thread closes.

**`/wrap-continue`** — Mid-task context reset. Light capture. Commit and push (mandatory), save anything you'd lose if context cleared, generate a hot-resume pickup prompt. The goal is to close the thread and start the next one with a precise handoff — not to summarize everything, just to preserve the thread.

The distinction matters. Running the heavy end-of-day flow on a continue wastes the tokens you were trying to save. Running the light continue flow on an end-of-day loses capture. Two skills, two modes.

### GH cleanup family — repo hygiene

Repos accumulate debt the same way context windows do — gradually, then all at once. Stale branches, ignored PRs, dusty issues. These four skills clear that debt without ceremony.

**`/gh-clean-branches`** — Prunes local branches whose remote is gone and feature branches already merged into main. Shows candidates, waits for confirmation, uses safe delete. Never force-deletes without an explicit nod.

**`/gh-pr-triage`** — Surveys your open PRs and PRs waiting on your review. Groups into: your PRs needing action, PRs waiting on you to review, stale (>14 days). Concrete next-action suggestion per row. Read-only.

**`/gh-fork-sync`** — Syncs your fork's main with upstream. Shows how far behind you are, confirms the strategy, pushes to your origin. Hard safety rule: never pushes to upstream. (This rule exists because of a real incident involving an unintentional PR opened on an upstream repo — the guard is non-negotiable.)

**`/gh-stale-issues`** — Triages open issues by age and last activity. Groups into no-activity (90d+), no-author-response (30d+), needs labels, needs triage. Generates ready-to-run `gh` commands. Read-only — you run the commands.

---

## My stack (so you know what to swap)

These skills reference my specific setup. Here's what that means and what you'd swap:

| My tool                      | What it does                        | Swap for                                                     |
| ---------------------------- | ----------------------------------- | ------------------------------------------------------------ |
| Linear                       | Ticket tracker                      | GitHub Issues, Jira, Notion, etc.                            |
| Second Brain / QMD           | Long-term searchable notes          | Obsidian, Notion, your notes system                          |
| ORCHESTRATOR.md              | State file for orchestrator threads | Optional — only relevant if you use the orchestrator pattern |
| `.claude/projects/*/memory/` | Per-project memory dir              | Optional — Claude Code memory convention                     |

The gh cleanup skills are stack-agnostic. The wrap skills work without Linear or Second Brain — just skip those steps.

---

## Install

All six skills:

```bash
npx skills add seansmithdesign/agent-skills
```

One skill:

```bash
npx skills add seansmithdesign/agent-skills --skill wrap-continue
npx skills add seansmithdesign/agent-skills --skill gh-clean-branches
```

Skills land in `~/.claude/skills/` and are available as slash commands in the next Claude Code session.

---

## Skills ecosystem

These skills are built for the [open agent skills ecosystem](https://skills.sh/). Any SKILL.md-compatible harness can use them.

Browse more skills at [skills.sh](https://skills.sh/).
