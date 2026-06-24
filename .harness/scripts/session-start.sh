#!/usr/bin/env bash
# SessionStart hook: generates OTEL trace context, emits the root GenAI span,
# reminds to create a worktree when on main, and reports collector reachability.
# It does NOT start the monitoring stack — that is the devcontainer's job
# (.devcontainer/compose.yml). This hook only observes and reminds.

COLLECTOR_HOST="localhost"
COLLECTOR_PORT="4317"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SESSION_FILE="/tmp/claude-harness-session.env"

_gen_trace_id() {
  cat /proc/sys/kernel/random/uuid 2>/dev/null | tr -d '-' \
    || openssl rand -hex 16
}

_gen_span_id() {
  openssl rand -hex 8 2>/dev/null \
    || cat /proc/sys/kernel/random/uuid | tr -d '-' | cut -c1-16
}

_emit_session_trace() {
  local trace_id="$1" span_id="$2" session_id="$3" branch="$4"
  # shellcheck source=harness-trace.sh
  source "${SCRIPT_DIR}/harness-trace.sh" 2>/dev/null || return 0

  local attrs
  attrs=$(printf '[
  {"key":"gen_ai.operation.name","value":{"stringValue":"invoke_agent"}},
  {"key":"gen_ai.provider.name", "value":{"stringValue":"anthropic"}},
  {"key":"gen_ai.agent.name",    "value":{"stringValue":"claude-code"}},
  {"key":"gen_ai.request.model", "value":{"stringValue":"%s"}},
  {"key":"harness.session.id",   "value":{"stringValue":"%s"}},
  {"key":"harness.branch",       "value":{"stringValue":"%s"}}
]' "${HARNESS_MODEL:-claude-sonnet-4-6}" "$session_id" "$branch")

  emit_span "invoke_agent claude-code" "$trace_id" "$span_id" "" "$attrs"
  emit_session_metric "$session_id" "$branch"
}

_init_session() {
  local branch; branch=$(git branch --show-current 2>/dev/null || echo "unknown")
  local trace_id span_id session_id
  trace_id=$(_gen_trace_id)
  span_id=$(_gen_span_id)
  session_id=$(_gen_span_id)

  printf 'HARNESS_TRACE_ID=%s\nHARNESS_ROOT_SPAN_ID=%s\nHARNESS_SESSION_ID=%s\nHARNESS_BRANCH=%s\n' \
    "$trace_id" "$span_id" "$session_id" "$branch" > "$SESSION_FILE"

  _emit_session_trace "$trace_id" "$span_id" "$session_id" "$branch"
}

# Always initialize session IDs (emit_* functions handle collector-down gracefully)
_init_session

# Branch-state reminder runs ALWAYS — independent of collector reachability.
# The worktree rule is a hard project invariant; gating it behind monitoring
# would silently disable the harness's most important guardrail when the
# collector is down (exactly when the environment is already degraded).
REMINDER=""
BRANCH=$(git branch --show-current 2>/dev/null)
if [[ "$BRANCH" == "main" || "$BRANCH" == "master" ]]; then
  REMINDER="HARNAIS: tu es sur main. Si tu démarres une feature (brainstorming inclus), invoke superpowers:using-git-worktrees pour créer un worktree isolé AVANT de commencer."
elif [[ -z "$BRANCH" ]]; then
  REMINDER="HARNAIS: branche indéterminée (detached HEAD ?). Vérifie ton contexte git avant de commencer."
fi

# Collector reachability is informational and only surfaced when it is down.
COLLECTOR_MSG=""
if ! bash -c "echo >/dev/tcp/${COLLECTOR_HOST}/${COLLECTOR_PORT}" 2>/dev/null; then
  COLLECTOR_MSG="HARNAIS: Collector inaccessible sur localhost:4317 — la stack monitoring démarre normalement avec le devcontainer (otel-collector, grafana:3000, prometheus:9090, tempo:3200)"
fi

# Emit a single systemMessage combining whichever notices apply.
MSG="$REMINDER"
if [[ -n "$COLLECTOR_MSG" ]]; then
  if [[ -n "$MSG" ]]; then MSG="${MSG}"$'\n\n'"${COLLECTOR_MSG}"; else MSG="$COLLECTOR_MSG"; fi
fi
if [[ -n "$MSG" ]]; then
  jq -n --arg m "$MSG" '{"systemMessage": $m}'
fi
