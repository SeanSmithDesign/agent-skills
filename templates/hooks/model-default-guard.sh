#!/usr/bin/env bash
# model-default-guard.sh
# Fires on SessionStart. Warns if settings.json carries a global "model"
# default — Fable/Opus defaults carry cost into every session, and
# `/model fable` + Enter (no session-only flag) silently writes one with
# nothing else to catch it. Empty/no key is the 99% path: print nothing,
# exit 0. A value present emits one JSON object on both the systemMessage
# channel (the user's terminal only) and additionalContext (reaches the model).
# Always exits 0 — a malformed settings.json or missing jq must never
# break SessionStart.

set -uo pipefail

SETTINGS_FILE="${MODEL_GUARD_SETTINGS:-$HOME/.claude/settings.json}"

[ -f "$SETTINGS_FILE" ] || exit 0

command -v jq >/dev/null 2>&1 || exit 0

MODEL=$(jq -r '.model // empty' "$SETTINGS_FILE" 2>/dev/null) || exit 0

[ -n "$MODEL" ] || exit 0

jq -n --arg model "$MODEL" '{
  systemMessage: "⚠ settings.json has a global model default: \($model). Fable/Opus defaults carry cost into every session. Remove the \"model\" key or re-pick with /model + s (session-only).",
  hookSpecificOutput: {
    hookEventName: "SessionStart",
    additionalContext: "settings.json carries a global model default (\($model)). Tell the user once at the start of your first reply, in one line. Do not remove it yourself."
  }
}' 2>/dev/null || exit 0

exit 0
