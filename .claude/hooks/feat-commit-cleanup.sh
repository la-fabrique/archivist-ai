#!/usr/bin/env bash
# PostToolUse hook: rappel harness-cleaner après un commit feat()
# Détecte les commits feat() et injecte un additionalContext obligatoire.

if ! command -v jq &>/dev/null; then exit 0; fi

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // empty')

if [[ "$TOOL" != "Bash" ]]; then exit 0; fi

CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if ! echo "$CMD" | grep -qE "git( -C [^ ]+)? commit"; then exit 0; fi

# Only fire when the commit actually succeeded. A successful `git commit` prints
# "[<branch> <hash>] <subject>" to stdout. If that line is absent (nothing staged,
# rejected pre-commit hook, failed command), HEAD is unchanged and reading
# `git log -1` would inspect the WRONG commit — producing a false reminder.
RESPONSE=$(echo "$INPUT" | jq -r '
  .tool_response
  | if type == "object" then (.stdout // .output // .stderr // "")
    elif type == "string" then .
    else "" end' 2>/dev/null)
if ! echo "$RESPONSE" | grep -qE '^\[.+ [0-9a-f]{7,}\]'; then exit 0; fi

LAST_MSG=$(git log -1 --pretty=%s 2>/dev/null)

if echo "$LAST_MSG" | grep -qE "^(feat|fix|refactor)\("; then
  jq -n --arg msg "$LAST_MSG" '{
    "hookSpecificOutput": {
      "hookEventName": "PostToolUse",
      "additionalContext": ("HARNAIS OBLIGATOIRE: commit détecté — \"" + $msg + "\". Séquence à enchaîner MAINTENANT sans attendre : 1) invoke /simplify sur le code modifié ; 2) mettre à jour README, docs/architecture/, ADRs et docs/features/ pour refléter l'état du code — supprimer les fichiers ADR et .feature des éléments supprimés, ne pas les garder en superseded ; 3) committer tous les changements ; 4) git push de la branche courante ; 5) gh pr create pour ouvrir la PR. Si feat() : aussi lancer le harness-cleaner agent.")
    }
  }'
fi
