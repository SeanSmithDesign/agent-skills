---
name: gh-clean-branches
description: Prune stale local branches — detects branches whose remote is gone and merged feature branches still hanging around. Shows a combined list for confirmation before deleting anything.
license: MIT
metadata:
  version: 1.0.0
  category: workflow
  domain: git-hygiene
  status: stable
  platforms: All
keywords:
  - git
  - branches
  - cleanup
  - prune
  - merged
  - stale
  - hygiene
---

# Clean Branches

Prune stale local branches. Two kinds of branch debt cleaned up in one pass: branches whose remote is gone, and feature branches already merged into main.

Triggered by: `/gh-clean-branches`, "clean branches", "prune branches", "delete stale branches".

## Steps

### 1. Sync remote refs

```bash
git fetch --prune
```

This removes remote-tracking refs for branches that no longer exist on the remote. Required before detection — without it, gone branches won't show as gone.

### 2. Detect branches with gone remotes

```bash
git branch -vv | grep ': gone]'
```

Lists local branches whose upstream tracking remote has been deleted (e.g., merged PRs where the branch was auto-deleted on GitHub).

### 3. Detect merged feature branches

```bash
git branch --merged main
```

Also try `master` if `main` doesn't exist. Lists local branches fully merged into main. Exclude: `main`, `master`, `develop`, `staging`, and the currently checked-out branch.

### 4. Present combined candidate list

Show a single deduplicated table:

```
  Branches to delete:

  ┌──────────────────────────────┬─────────────────────────────┐
  │ Branch                       │ Reason                      │
  ├──────────────────────────────┼─────────────────────────────┤
  │ feat/old-login               │ remote gone                 │
  │ fix/button-color             │ merged into main            │
  │ chore/deps-update            │ remote gone + merged        │
  └──────────────────────────────┴─────────────────────────────┘

  3 branches. Confirm to delete, or say which to skip.
```

Wait for explicit confirmation before proceeding. Never auto-delete.

### 5. Delete on confirmation

```bash
git branch -d branch-name   # safe delete (refuses if unmerged)
```

Use `-d` (not `-D`) by default. If `-d` fails because git thinks a branch is unmerged, surface the error and ask before escalating to `-D`. Never silently force-delete.

### 6. Report

```
  ┌──────────────┬────────────────────────────────┐
  │ Deleted      │ feat/old-login, fix/button-color│
  │ Skipped      │ chore/deps-update (user request)│
  │ Repo         │ Clean                           │
  └──────────────┴────────────────────────────────┘
```

## Judgment Calls

- **No candidates found?** Say so and exit. No need to show an empty table.
- **Currently on a candidate branch?** Skip it with a note — can't delete the active branch.
- **Protected branch in the list?** Skip main, master, develop, staging automatically — don't even show them as candidates.
- **`-d` fails on a branch?** Surface the branch name and last commit, ask whether to force. Don't decide unilaterally.
- **Large number of candidates (10+)?** Still show all — let the user decide what to prune. Don't filter silently.
