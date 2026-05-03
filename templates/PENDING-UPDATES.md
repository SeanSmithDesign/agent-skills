# Pending Orchestrator Updates

> Registry of config improvements discovered during session work. Each entry must tie to output quality or token/context cost — not "nice to have."
>
> **Workflow:** Run `/orchestrator:update` to review and apply. Stale entries (60+ days pending) are candidates for pruning.
>
> **Admission rule:** no entry without a concrete, measurable effect. If you can't say what the eval delta should look like, it doesn't belong here.

## Status key

- `pending` — discovered, not yet applied
- `applied-YYYY-MM-DD` — applied, eval delta recorded
- `dismissed-YYYY-MM-DD` — decided not worth doing
- `deferred-YYYY-MM-DD` — paused for now, revisit

---

<!-- Add entries below. Format:

## UPD-001 — [short title]

- **Discovered:** YYYY-MM-DD, from [context]
- **Change type:** efficiency | quality | behavior
- **Blast radius:** [files to touch]
- **Effort:** ~N min (brief description)
- **Expected eval delta:** [measurable expectation]
- **Eval test to run:** [how to verify]
- **Status:** pending
- **Rationale:** [why this is worth doing]

-->
