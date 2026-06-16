#!/usr/bin/env bash
# Stop hook: fires at end of Claude session on a feature branch.
# 1. ALWAYS reminds to commit when the working tree is dirty — work must never
#    be left uncommitted at the end of a session.
# 2. Reminds to run /simplify + the harness-cleaner agent (dev cycle wrap-up).
branch=$(git branch --show-current 2>/dev/null)
[ -n "$branch" ] || exit 0
[ "$branch" != "main" ] && [ "$branch" != "master" ] || exit 0

cleanup="Dev cycle reminder: invoke /simplify on changed code, then launch the harness-cleaner agent to archive plans and harvest learnings."

if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
  msg="HARNAIS: modifications non committées sur '${branch}'. Tu DOIS committer ton travail avant de terminer la session — ne jamais laisser de travail non committé. Ensuite : ${cleanup}"
else
  msg="$cleanup"
fi

if command -v jq &>/dev/null; then
  jq -n --arg m "$msg" '{"systemMessage": $m}'
else
  # Fallback without jq: escape double quotes for valid JSON.
  printf '{"systemMessage": "%s"}\n' "${msg//\"/\\\"}"
fi
