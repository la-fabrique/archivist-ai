#!/usr/bin/env bash
# PostToolUse hook: valide le format du message de commit après git commit
# Format attendu : type(scope): description
# type ∈ {feat, fix, refactor, test, docs, chore, ci, style, perf}

if ! command -v jq &>/dev/null; then exit 0; fi

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // empty')

# Seulement pour Bash
if [[ "$TOOL" != "Bash" ]]; then exit 0; fi

CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Seulement si c'est un git commit
if ! echo "$CMD" | grep -q "git commit"; then exit 0; fi

# Extraire le message de commit. Couvre les formes courantes :
#   -m "msg"  -m 'msg'  -m=msg  --message "msg"  --message='msg'
# (chaque lookbehind est de largeur fixe, contrainte de grep -P).
MSG=$(echo "$CMD" | grep -oP "(?<=-m )[\"\x27][^\x27\"]+[\"\x27]|(?<=--message )[\"\x27][^\x27\"]+[\"\x27]|(?<=-m=)[\"\x27][^\x27\"]+[\"\x27]|(?<=--message=)[\"\x27][^\x27\"]+[\"\x27]" | head -1 | tr -d '"'"'")

# Fallback : heredoc ou message en variable (on ne peut pas l'extraire ici — laisser passer)
if [[ -z "$MSG" ]]; then exit 0; fi
# Ignorer les messages qui contiennent une substitution shell ($(cat <<'EOF'...))
if [[ "$MSG" == *'$('* ]]; then exit 0; fi

PATTERN='^(feat|fix|refactor|test|docs|chore|ci|style|perf)\([a-z][a-z0-9-]*\): .+'

if echo "$MSG" | grep -qE "$PATTERN"; then
  exit 0
fi

# Message non conforme : injecter un avertissement dans le contexte de l'agent
jq -n \
  --arg msg "$MSG" \
  '{
    "hookSpecificOutput": {
      "hookEventName": "PostToolUse",
      "decisionContext": ("HARNAIS WARNING: message de commit non conforme : \"" + $msg + "\". Format attendu : type(scope): description. Exemples valides : feat(archivist-cli): add dry-run flag | fix(referentiel): correct broken link | docs(harnais): add hooks plan")
    }
  }'
