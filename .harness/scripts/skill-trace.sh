#!/usr/bin/env bash
# PostToolUse hook: fires when the Skill tool is used.
# Emits an OTEL GenAI "execute_tool" span to Tempo and a Prometheus metric.
# Self-filters: exits 0 immediately for any tool other than Skill.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SESSION_FILE="/tmp/claude-harness-session.env"

CANONICAL_SKILLS=(
  "superpowers:using-git-worktrees"
  "superpowers:brainstorming"
  "superpowers:writing-plans"
  "superpowers:test-driven-development"
  "superpowers:verification-before-completion"
  "superpowers:finishing-a-development-branch"
  "superpowers:requesting-code-review"
)

_is_canonical() {
  local name="$1"
  for s in "${CANONICAL_SKILLS[@]}"; do
    [[ "$s" == "$name" ]] && echo "true" && return
  done
  echo "false"
}

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)
[[ "$TOOL_NAME" == "Skill" ]] || exit 0

SKILL_NAME=$(echo "$INPUT" | jq -r '.tool_input.skill // empty' 2>/dev/null)
[[ -n "$SKILL_NAME" ]] || exit 0

[[ -f "$SESSION_FILE" ]] || exit 0
# shellcheck source=/dev/null
source "$SESSION_FILE"

# shellcheck source=harness-trace.sh
source "${SCRIPT_DIR}/harness-trace.sh" 2>/dev/null || exit 0

SPAN_ID=$(openssl rand -hex 8 2>/dev/null \
  || cat /proc/sys/kernel/random/uuid | tr -d '-' | cut -c1-16)
IS_CANONICAL=$(_is_canonical "$SKILL_NAME")

ATTRS=$(printf '[
  {"key":"gen_ai.operation.name",   "value":{"stringValue":"execute_tool"}},
  {"key":"gen_ai.tool.name",        "value":{"stringValue":"%s"}},
  {"key":"gen_ai.tool.type",        "value":{"stringValue":"function"}},
  {"key":"harness.skill.canonical", "value":{"stringValue":"%s"}}
]' "$SKILL_NAME" "$IS_CANONICAL")

emit_span "execute_tool ${SKILL_NAME}" \
  "$HARNESS_TRACE_ID" "$SPAN_ID" "$HARNESS_ROOT_SPAN_ID" "$ATTRS"

emit_skill_metric "$HARNESS_SESSION_ID" "$SKILL_NAME" "${HARNESS_BRANCH:-unknown}"
