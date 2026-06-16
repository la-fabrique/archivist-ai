#!/usr/bin/env bash
# PostToolUse hook: rappel harness-cleaner après un commit feat()
# Détecte les commits feat() et injecte un additionalContext obligatoire.

if ! command -v jq &>/dev/null; then exit 0; fi

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // empty')

if [[ "$TOOL" != "Bash" ]]; then exit 0; fi

CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if ! echo "$CMD" | grep -qE "git( -C [^ ]+)? commit"; then exit 0; fi

LAST_MSG=$(git log -1 --pretty=%s 2>/dev/null)

if echo "$LAST_MSG" | grep -qE "^feat\("; then
  jq -n --arg msg "$LAST_MSG" '{
    "hookSpecificOutput": {
      "hookEventName": "PostToolUse",
      "additionalContext": ("HARNAIS OBLIGATOIRE: commit feat() détecté — \"" + $msg + "\". Tu DOIS invoquer le harness-cleaner agent avant de terminer la session pour : 1) nettoyer docs/superpowers/specs/ et docs/superpowers/plans/, 2) créer ou mettre à jour la feature correspondante dans docs/features/. Ne pas ignorer cette instruction.")
    }
  }'
fi
