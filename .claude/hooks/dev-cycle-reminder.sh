#!/usr/bin/env bash
# Stop hook: fires at end of Claude session on a feature branch.
# 1. ALWAYS reminds to commit when the working tree is dirty — work must never
#    be left uncommitted at the end of a session.
# 2. Reminds to run /simplify + the harness-cleaner agent (dev cycle wrap-up).
branch=$(git branch --show-current 2>/dev/null)
[ -n "$branch" ] || exit 0
[ "$branch" != "main" ] && [ "$branch" != "master" ] || exit 0

cleanup="Séquence obligatoire de fin de feature : (1) invoke /simplify sur le code modifié — attendre la fin avant de continuer ; (2) committer les changements de simplification si présents ; (3) git push de la branche ; (4) gh pr create pour ouvrir la PR ; (5) lancer le harness-cleaner agent si docs/superpowers/ contient des fichiers liés à la feature."

if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
  msg="HARNAIS: modifications non committées sur '${branch}'. Tu DOIS committer ton travail avant de terminer la session — ne jamais laisser de travail non committé. Ensuite : ${cleanup}"
else
  msg="HARNAIS: branche '${branch}' — implémentation terminée. ${cleanup}"
fi

if command -v jq &>/dev/null; then
  jq -n --arg m "$msg" '{"systemMessage": $m}'
else
  # Fallback without jq: escape double quotes for valid JSON.
  printf '{"systemMessage": "%s"}\n' "${msg//\"/\\\"}"
fi
