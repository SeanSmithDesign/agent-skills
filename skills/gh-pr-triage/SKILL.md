---
name: gh-pr-triage
description: Survey open PRs — yours, assigned, and review-requested — grouped by what action is needed. Outputs a table with a concrete next-action suggestion per PR.
license: MIT
metadata:
  version: 1.0.0
  category: workflow
  domain: git-hygiene
  status: stable
  platforms: All
keywords:
  - github
  - pull-requests
  - triage
  - review
  - stale
  - ci
  - hygiene
---

# PR Triage

Survey open PRs and surface what needs action. Three buckets: your PRs waiting on something, PRs waiting on your review, and stale PRs that need a decision.

Triggered by: `/gh-pr-triage`, "pr triage", "triage prs", "review my prs", "what prs need attention".

Requires `gh` CLI authenticated.

## Steps

### 1. Gather open PRs

Run in parallel:

```bash
gh pr list --author @me --state open --json number,title,url,isDraft,mergeable,reviewDecision,statusCheckRollup,updatedAt,baseRefName
gh pr list --search "review-requested:@me state:open" --json number,title,url,author,isDraft,reviewDecision,statusCheckRollup,updatedAt
```

Deduplicate (a PR you authored may also be review-requested to you).

### 2. Classify each PR

For each PR, determine:

- **CI status** — passing / failing / pending / none
- **Review state** — approved / changes-requested / awaiting-review / none
- **Mergeability** — mergeable / conflicts / unknown
- **Staleness** — last updated date; flag if >14 days with no activity
- **Draft** — drafts go in a separate bucket, lower priority

### 3. Group into buckets

**Your PRs — needs action:**
PRs you authored where something is blocking: CI failing, conflicts, reviewer requested changes, or approved and ready to merge.

**Waiting on your review:**
PRs where you're a requested reviewer and haven't submitted a review yet.

**Stale (>14 days, no activity):**
PRs from either bucket with no updates in 14+ days. These need a decision: push, ping, or close.

**Drafts:**
Your draft PRs. Surface them briefly — they're in-progress, not blocked, but worth knowing about.

### 4. Output table

```
  Your PRs — needs action (2)
  ┌──────┬─────────────────────────────┬──────────┬──────────┬───────────────────────────┐
  │ #    │ Title                       │ CI       │ Reviews  │ Action                    │
  ├──────┼─────────────────────────────┼──────────┼──────────┼───────────────────────────┤
  │ #142 │ Add user avatar upload      │ ✓ pass   │ Approved │ Ready to merge            │
  │ #138 │ Refactor auth middleware    │ ✗ fail   │ Pending  │ Fix CI (2 checks failing) │
  └──────┴─────────────────────────────┴──────────┴──────────┴───────────────────────────┘

  Waiting on your review (1)
  ┌──────┬─────────────────────────────┬──────────┬───────────────────────────────────────┐
  │ #    │ Title                       │ Author   │ Action                                │
  ├──────┼─────────────────────────────┼──────────┼───────────────────────────────────────┤
  │ #145 │ Update onboarding copy      │ @alice   │ Review requested 3 days ago           │
  └──────┴─────────────────────────────┴──────────┴───────────────────────────────────────┘

  Stale (1)
  ┌──────┬─────────────────────────────┬──────────────┬──────────────────────────────────┐
  │ #    │ Title                       │ Last active  │ Action                           │
  ├──────┼─────────────────────────────┼──────────────┼──────────────────────────────────┤
  │ #129 │ Experiment: dark mode       │ 22 days ago  │ Decide: close or rebase + push   │
  └──────┴─────────────────────────────┴──────────────┴──────────────────────────────────┘
```

Skip empty buckets. Keep output tight.

## Judgment Calls

- **No open PRs?** Say so and exit.
- **Draft PRs?** Surface them in a collapsed "Drafts (N)" line — not in the main action buckets.
- **CI status unavailable?** Mark as "unknown" rather than inferring.
- **PR approved but has conflicts?** Action is "resolve conflicts" not "merge" — merge will fail.
- **You're both the author and a requested reviewer?** Put it in "Your PRs" bucket, not "Waiting on review."
- **Stale threshold:** 14 days of no activity (no commits, no comments, no review events). Adjust if the project has a longer natural PR cadence.
- This skill is read-only. It surfaces suggested actions — it doesn't merge, close, or push anything.
