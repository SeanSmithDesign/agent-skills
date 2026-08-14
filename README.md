# agent-skills

Skills I use to run Claude Code as a designer. Not a framework: a process snapshot.

---

## Install

```bash
npx skills add seansmithworks/agent-skills --list          # browse
npx skills add seansmithworks/agent-skills --skill wrap    # one skill
npx skills add seansmithworks/agent-skills -s '*' -g       # all of them, globally
```

`-a claude-code` targets Claude Code specifically. `-g` installs to `~/.claude/skills` instead of the current project.

---

## What's here

Four families. Nine skills. All opinionated.

### Wrap family: session hygiene

Every Claude Code session ends the same two ways: you're done for the day, or you're not done but the context window is getting expensive. These are different situations that need different behavior.

**`/wrap`**: End-of-session. Heavy capture. Runs in this order: plan reconciliation (if orchestrator), commit and push, ticket tracker, memories, orchestrator state, session notes, long-term notes. The goal is to leave nothing on the table, every decision, every commit SHA, every deferred task captured before the thread closes.

```bash
npx skills add seansmithworks/agent-skills --skill wrap
```

**`/wrap-continue`**: Mid-task context reset. Light capture. Commit and push (mandatory), save anything you'd lose if context cleared, generate a hot-resume pickup prompt. The goal is to close the thread and start the next one with a precise handoff, not to summarize everything, just to preserve the thread.

```bash
npx skills add seansmithworks/agent-skills --skill wrap-continue
```

The distinction matters. Running the heavy end-of-day flow on a continue wastes the tokens you were trying to save. Running the light continue flow on an end-of-day loses capture. Two skills, two modes.

### Orchestrator family: pattern hygiene

The orchestrator is a long-lived Claude Code thread that never writes code. It learns the codebase, maintains context across compactions, and delegates all implementation to subagents. These three skills maintain the orchestrator itself, not the work it does.

**`/orchestrator:update`**: Config evolution, opt-in. Reads `~/.claude/PENDING-UPDATES.md`, presents pending entries, applies selected ones via subagents, and validates with an eval suite. The mandatory baseline plus post-apply eval loop is non-bypassable by design, you need a signal before and after any config change to know if behavior regressed.

```bash
npx skills add seansmithworks/agent-skills --skill orchestrator-update
```

**`/orchestrator:scaffold`**: Project setup and gap-filling. Three modes: default (auto-detect what's missing), `lifecycle` (scaffold the six agent files: product, experience, craft, build, data, quality), and `grounding` (interview-driven drafting of mission.md, brand.md, principles.md). The grounding files are the identity layer, they travel with the code, survive compaction, and give every subagent a consistent product lens without you having to re-explain context each session.

```bash
npx skills add seansmithworks/agent-skills --skill orchestrator-scaffold
```

**`/orchestrator-route`**: Routes an over-cap `ORCHESTRATOR.md` down to a router-shaped file without destroying durable value. Use it when a size gate fires, when `/wrap` reports the file is over its 20,000-char cap, or when you say "route this" or "this file is too big." It's not a tidy-up pass, the trigger is size or staleness, and the operation is routing durable facts to the memory files that own them, never deleting by age. Six gates keep it honest: never evict by recency, route to the on-demand layer instead of always-read agent files, never archive a fact that's still true, verify every fact kept a home, commit a baseline before editing, and measure the whole boot set, not just the one file, before and after.

```bash
npx skills add seansmithworks/agent-skills --skill orchestrator-route
```

The orchestrator family requires two companion files that aren't skills, copy them from `templates/` before using:

```bash
# Copy the companion files into your Claude config dir
curl -o ~/.claude/orchestrator-prompt.md \
  https://raw.githubusercontent.com/seansmithworks/agent-skills/main/templates/orchestrator-prompt.md

curl -o ~/.claude/PENDING-UPDATES.md \
  https://raw.githubusercontent.com/seansmithworks/agent-skills/main/templates/PENDING-UPDATES.md
```

Then launch the orchestrator thread with:

```bash
claude --append-system-prompt-file ~/.claude/orchestrator-prompt.md
```

---

### GH cleanup family: repo hygiene

Repos accumulate debt the same way context windows do, gradually, then all at once. Stale branches, ignored PRs, dusty issues. These four skills clear that debt without ceremony.

**`/gh-clean-branches`**: Prunes local branches whose remote is gone and feature branches already merged into main. Shows candidates, waits for confirmation, uses safe delete. Never force-deletes without an explicit nod.

```bash
npx skills add seansmithworks/agent-skills --skill gh-clean-branches
```

**`/gh-pr-triage`**: Surveys your open PRs and PRs waiting on your review. Groups into: your PRs needing action, PRs waiting on you to review, stale (>14 days). Concrete next-action suggestion per row. Read-only.

```bash
npx skills add seansmithworks/agent-skills --skill gh-pr-triage
```

**`/gh-fork-sync`**: Syncs your fork's main with upstream. Shows how far behind you are, confirms the strategy, pushes to your origin. Hard safety rule: never pushes to upstream. (This rule exists because of a real incident involving an unintentional PR opened on an upstream repo, the guard is non-negotiable.)

```bash
npx skills add seansmithworks/agent-skills --skill gh-fork-sync
```

**`/gh-stale-issues`**: Triages open issues by age and last activity. Groups into no-activity (90d+), no-author-response (30d+), needs labels, needs triage. Generates ready-to-run `gh` commands. Read-only, you run the commands.

```bash
npx skills add seansmithworks/agent-skills --skill gh-stale-issues
```

---

## My stack (so you know what to swap)

These skills reference my specific setup. Here's what that means and what you'd swap:

| My tool                             | What it does                        | Swap for                                                                      |
| ------------------------------------ | ------------------------------------ | ------------------------------------------------------------------------------ |
| Linear                              | Ticket tracker                      | GitHub Issues, Jira, Notion, etc.                                             |
| Second Brain / QMD                  | Long-term searchable notes          | Obsidian, Notion, your notes system                                           |
| ORCHESTRATOR.md                     | State file for orchestrator threads | Optional, only relevant if you use the orchestrator pattern                   |
| `.claude/projects/*/memory/`        | Per-project memory dir              | Optional, Claude Code memory convention                                      |
| `~/.claude/orchestrator-prompt.md`  | Orca system prompt                  | Required for orchestrator family, copy from `templates/`                     |
| `~/.claude/PENDING-UPDATES.md`      | Config update registry              | Required for `/orchestrator:update`, copy from `templates/`                  |
| `~/.claude/projects/SCAFFOLDING.md` | Per-project scaffold version index  | Used by `/orchestrator:scaffold`, create manually or let the skill create it |

The gh cleanup skills are stack-agnostic. The wrap skills work without Linear or Second Brain, just skip those steps. The orchestrator skills require the two template files above.

---

## Install all skills

All nine skills:

```bash
npx skills add seansmithworks/agent-skills
```

Skills land in `~/.claude/skills/` and are available as slash commands in the next Claude Code session.

---

## Skills ecosystem

These skills are built for the [open agent skills ecosystem](https://skills.sh/). Any SKILL.md-compatible harness can use them.

Browse more skills at [skills.sh](https://skills.sh/).
