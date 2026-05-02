#!/usr/bin/env bash
# PreToolUse hook: injecte un rappel referentiel-update si le fichier édité
# est dans packages/referentiel/

if ! command -v jq &>/dev/null; then exit 0; fi

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // empty')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Seulement pour Write et Edit
if [[ "$TOOL" != "Write" && "$TOOL" != "Edit" ]]; then exit 0; fi

# Seulement si le fichier est dans packages/referentiel/
if [[ "$FILE_PATH" != *"packages/referentiel/"* ]]; then exit 0; fi

jq -n '{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "HARNAIS: ce fichier est dans packages/referentiel/ — invoquer la skill referentiel-update (4 étapes : qualifier → impact → CLI build → tests)."
  }
}'
