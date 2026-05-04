#!/usr/bin/env bash
# PreToolUse hook: bloque git commit sur main — toujours travailler dans un worktree

if ! command -v jq &>/dev/null; then exit 0; fi

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // empty')

if [[ "$TOOL" != "Bash" ]]; then exit 0; fi

CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if ! echo "$CMD" | grep -qE '(^|\s|;|&&|\|\|)git commit'; then exit 0; fi

CURRENT_BRANCH=$(git -C "$(pwd)" branch --show-current 2>/dev/null)

if [[ "$CURRENT_BRANCH" == "main" || "$CURRENT_BRANCH" == "master" ]]; then
  jq -n \
    --arg branch "$CURRENT_BRANCH" \
    '{
      "decision": "block",
      "reason": ("HARNAIS BLOCK: commit bloqué sur " + $branch + ". Invoke superpowers:using-git-worktrees to create an isolated workspace first, then commit from within that worktree.")
    }'
  exit 2
fi
