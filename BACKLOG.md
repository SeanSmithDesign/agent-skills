# Backlog

Open items for the skills repo. Greppable, no ticket overhead.

## 2026-08-27 (thread "MD Probe") — config-evolution loop, planned and gated

Plan plus the unedited refutation live at `~/.claude/plans/config-evolution/`
(`draft-plan.md`, `refutation.md`). Verdict was **revise**; the revised order is below.
Nothing has been built yet.

- [x] **Fix the pending-updates counter.** Done, `b2cda14`. Reader (`orchestrator-boot/SKILL.md:19`),
  writer instruction (`orchestrator-update/SKILL.md:15,73`), and `templates/orchestrator-prompt.md:13`
  now all use the registry's real `- **Status:** pending` format. Verified by execution: synthetic
  pending entry → 1, real registry (3 applied entries) → 0.
- [ ] ~~Fix the pending-updates counter (do this FIRST, everything else is downstream).~~
  `skills/orchestrator-boot/SKILL.md:19` counts with `grep -c 'status: pending'`, but the registry
  and `templates/PENDING-UPDATES.md:28` both write `- **Status:** pending`. Case-sensitive substring
  mismatch, so the counter returns 0 for a correctly-formatted entry and boot has been silent since
  April. Verified by execution, not by reading. Fix the reader AND
  `skills/orchestrator-update/SKILL.md:73`, which instructs the applier to write the non-matching
  format, in the same commit so reader and writer agree. Verify against a synthetic pending entry.
- [ ] **Re-baseline the claude-config versioning gap against a real `git status`.**
  `~/.claude` shows ~399 dirty lines: 72 modified, 12 deleted, 314 untracked. The load-bearing ones
  are `agents/explore.md`, `agents/implementer.md`, `agents/planner.md` (the tier-routing files
  global CLAUDE.md calls load-bearing), uncommitted since `c94f929`, 2026-07-06; plus a deleted
  `policy-limits.json` and a deleted Annotie memory tree. Commit by explicit path.
  **Pushing `~/.claude` is reserved for Sean** (`ORCHESTRATOR.md:35`).
- [ ] **Resolve the admission path before writing any wrap rule.** DECIDE OR KILL. All three
  registry entries record `Discovered: from post-slim behavioral eval` and each names a test that was
  already run, so field 3 of the admission rule (`skills/orchestrator-update/SKILL.md:93`) is
  retrospectively unproducible by a wrap that ran no eval. Strawman: admit a fourth path, "names the
  eval test that would need to be added." Alternative: entries stage in a separate list, not the
  registry itself.
- [ ] **Then the wire, last.** One sentence in `skills/wrap/SKILL.md` step 5 routing tooling and
  config learnings to `~/.claude/PENDING-UPDATES.md` when they clear the admission rule, plus the
  matching `README.md:227` correction in the same commit (that line currently scopes the registry to
  the orchestrator family only, which the new rule would contradict). One sentence, no table row, no
  restated "one home per fact" clause. Read `~/.claude/CONTEXT-RIGHTSIZING.md` first, as global
  CLAUDE.md requires before adding to an instruction file.
- [ ] **Three untracked skills in claude-config** — `brukas-queue` (1 file), `genomics-viz`
  (4 files), `snippost` (1 file). Read them, then recommend track-or-ignore rather than asking.
  `jefe` is correctly gitignored: its own repo, 943 MB.
- [ ] **`.gitignore` inconsistency in claude-config.** `.gitignore:68` is
  `skills/workflow/brand-naming/`, not `skills/brand-naming`, which is tracked and not ignored.
  Six symlinks point into this repo but only four are ignored; `skills/orchestrator-boot` and
  `skills/orchestrator-route` are tracked as mode-120000 blobs. Decide the intended rule, then make
  the file match it.
- [ ] **Four `gh-*` skills are published here but not installed locally** — `gh-clean-branches`,
  `gh-fork-sync`, `gh-pr-triage`, `gh-stale-issues` have no symlink in `~/.claude/skills/`.
  Parked, off-objective, discovered incidentally.
- [ ] **Not doing, deliberately:** redesigning the four-channel model, moving skills from the private
  `claude-config` into this public repo, adding `## Learnings` sections to skills generally, or
  touching `ce-compound` / `docs/solutions/` routing.

- [ ] **`templates/orchestrator-prompt.md` is stale against the prompt Sean actually runs.** Discovered
  while verifying the counter fix. The installed `~/.claude/orchestrator-prompt.md` is a slimmer,
  newer design that delegates session start to the `/orchestrator-boot` skill; the repo template still
  inlines a "Phase 1: Codebase Exploration" flow with the counting logic written out, and is missing
  the Cardinal Rule, the scope-card rule, and the non-boot session guidance. A cold installer from
  this public repo inherits the old prompt. Decide whether the template should be regenerated from the
  installed file or is deliberately a different artifact.
