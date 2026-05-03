---
name: gh-stale-issues
description: Triage open issues by age and last activity. Groups into action buckets and suggests what to do per issue. Read-only — surfaces actions, doesn't take them.
license: MIT
metadata:
  version: 1.0.0
  category: workflow
  domain: git-hygiene
  status: stable
  platforms: All
keywords:
  - github
  - issues
  - triage
  - stale
  - cleanup
  - hygiene
---

# Stale Issues

Triage open issues by age and activity. Groups into buckets with a suggested action per issue. Useful before a release, after a period of heavy development, or when the issue list has drifted into noise.

Triggered by: `/gh-stale-issues`, "stale issues", "triage issues", "clean up issues", "issue cleanup".

Requires `gh` CLI authenticated.

## Steps

### 1. Fetch open issues

```bash
gh issue list --state open --limit 200 --json number,title,createdAt,updatedAt,labels,assignees,comments,author
```

If the repo has 200+ open issues, note the cap and ask whether to paginate.

### 2. Classify by activity

For each issue, compute:

- **Age** — days since `createdAt`
- **Inactivity** — days since `updatedAt` (last event: comment, label, assignment, etc.)
- **Author response** — did the issue author comment after the initial post? (approximated by checking if `author` appears in later comments)

### 3. Group into buckets

**No activity (90+ days):**
Issues nobody has touched in 3 months. Likely abandoned or superseded. Suggest: close with a "stale — closing for inactivity, reopen if still relevant" comment, or label `wontfix`.

**No author response (30+ days):**
Issues that received a response (question, request for repro, etc.) but the original author hasn't replied. Suggest: ping author or close with "closing for no response."

**Needs labels:**
Issues with no labels at all. Hard to search, sort, or prioritize unlabeled issues. Suggest: add at least one label (`bug`, `enhancement`, `question`, etc.).

**Needs triage:**
Issues labeled `triage` or with no assignee and no label. Suggest: assign, label, or move to a milestone.

**Healthy:**
Everything else — labeled, assigned, recently active. Don't clutter the output with these.

### 4. Output

```
  No activity — 90+ days (3)
  ┌──────┬──────────────────────────────────────┬──────────────┬──────────────────────────────┐
  │ #    │ Title                                │ Last active  │ Suggested action             │
  ├──────┼──────────────────────────────────────┼──────────────┼──────────────────────────────┤
  │ #22  │ Dark mode flicker on load            │ 112 days ago │ Close as stale               │
  │ #18  │ Export to PDF                        │ 98 days ago  │ Close as wontfix or backlog  │
  │ #11  │ Add keyboard shortcuts               │ 91 days ago  │ Label + milestone or close   │
  └──────┴──────────────────────────────────────┴──────────────┴──────────────────────────────┘

  No author response — 30+ days (1)
  ┌──────┬──────────────────────────────────────┬──────────────┬──────────────────────────────┐
  │ #    │ Title                                │ Waiting      │ Suggested action             │
  ├──────┼──────────────────────────────────────┼──────────────┼──────────────────────────────┤
  │ #31  │ Login fails on Safari 16             │ 34 days      │ Close — no response          │
  └──────┴──────────────────────────────────────┴──────────────┴──────────────────────────────┘

  Needs labels (2)
  #27 — "Button hover state wrong color" → suggest: bug
  #33 — "Can I add custom domains?" → suggest: question
```

Skip empty buckets. Don't show the Healthy bucket unless asked.

### 5. Provide runnable commands

After the table, offer a block of `gh` commands the user can run to execute the suggestions:

```bash
# Close stale issues
gh issue close 22 --comment "Closing as stale — no activity in 90+ days. Reopen if this is still relevant."
gh issue close 18 --comment "Closing as wontfix for now — feel free to reopen with more detail."

# Add labels
gh issue edit 27 --add-label bug
gh issue edit 33 --add-label question
```

These are suggestions — the user runs them manually. This skill takes no actions.

## Judgment Calls

- **Large issue backlog (50+)?** Still show all candidates, but group into collapsible-style sections. Don't hide issues silently.
- **Repo uses a bot for stale issues?** Note it and still run — manual triage catches what bots miss.
- **Issue has a recent comment but old `updatedAt`?** Trust the most recent comment date over `updatedAt` if there's a discrepancy.
- **Thresholds:** 90 days for "no activity," 30 days for "no author response." Adjust in the prompt if your project has a different cadence.
- **This skill is read-only.** It fetches data and suggests commands. It never closes issues, adds labels, or modifies anything.
