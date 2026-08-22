---
name: gh-fork-sync
description: Sync your fork's main branch with upstream. Shows how far behind you are, confirms the strategy, syncs and pushes to your origin. Safety guard — never pushes to upstream.
license: MIT
metadata:
  version: 1.0.0
  category: workflow
  domain: git-hygiene
  status: stable
  platforms: All
keywords:
  - git
  - fork
  - upstream
  - sync
  - rebase
  - merge
  - hygiene
---

# Fork Sync

Sync your fork's main branch with upstream. Shows the gap, confirms the strategy, syncs cleanly.

Triggered by: `/gh-fork-sync`, "sync fork", "sync with upstream", "update fork", "bring fork up to date".

## Steps

### 1. Detect upstream remote

```bash
git remote -v
```

Look for a remote named `upstream` pointing to the original repo. If none exists, prompt:

> No upstream remote found. Add one with:
> `git remote add upstream <original-repo-url>`
> Then re-run this skill.

Don't guess the upstream URL. Exit and wait.

### 2. Detect the default branch and check it out

```bash
git fetch upstream
```

Try `main` first, fall back to `master` if `upstream/main` doesn't exist (same fallback `gh-clean-branches` uses). Call the result `$BRANCH` for the rest of this skill.

```bash
git checkout $BRANCH
```

Check out the branch before measuring the gap — behind/ahead counts computed from whatever branch the user happened to be on are wrong.

### 3. Show the gap

```bash
git log HEAD..upstream/$BRANCH --oneline | wc -l   # commits behind
git log upstream/$BRANCH..HEAD --oneline            # commits unique to fork
```

Present a summary:

```
  Fork status vs upstream/main

  Behind:  14 commits
  Ahead:   3 commits (your changes not in upstream)

  Your commits:
    a1b2c3d  fix: button padding on mobile
    e4f5g6h  chore: update dependencies
    i7j8k9l  feat: add user avatar support
```

If already up to date, say so and exit.

### 4. Confirm sync strategy

Default recommendation: **merge** (preserves your fork's commit history, safer for active forks). Offer rebase as an alternative if the user prefers a cleaner history.

> Sync upstream/$BRANCH into your fork's $BRANCH?
> Default strategy: merge. Say "rebase" to use rebase instead.

### 5. Sync

You're already on `$BRANCH` from step 2. For merge:

```bash
git merge upstream/$BRANCH
```

For rebase:

```bash
git rebase upstream/$BRANCH
```

If conflicts arise, stop immediately. List the conflicting files and exit with instructions:

> Conflicts in: src/auth.ts, package.json
> Resolve manually, then run `git merge --continue` (or `git rebase --continue`).
> Do NOT auto-resolve conflicts.

### 6. Push to your fork's origin

```bash
git push origin $BRANCH
```

**Safety rule: always push to `origin`, never to `upstream`.** This skill will never push to an upstream remote under any circumstances — not even if asked. Unintentional upstream pushes are hard to undo and can affect other contributors.

### 7. Report

```
  ┌──────────────┬───────────────────────────────────────┐
  │ Strategy     │ merge                                 │
  │ Synced       │ 14 commits from upstream/main         │
  │ Your commits │ 3 preserved                           │
  │ Pushed to    │ origin/main                           │
  │ Status       │ Up to date with upstream              │
  └──────────────┴───────────────────────────────────────┘
```

## Judgment Calls

- **No upstream remote?** Exit with instructions to add one. Don't guess.
- **Conflicts?** Stop and surface them. Never auto-resolve or proceed past a conflict.
- **Fork is ahead but not behind?** Upstream has nothing new — say so and exit. No sync needed.
- **Protected branches?** Only sync `main` (or `master`). Don't touch feature branches or release branches without explicit instruction.
- **Rebase vs merge:** Default to merge for forks with active work — rebase rewrites the fork's history and can complicate existing PRs from that fork. Only use rebase if the user explicitly asks.
- **Never push to upstream.** This is not a judgment call — it's a hard rule. Pushing to upstream on a fork affects everyone using that repo, and the damage is hard to reverse.
