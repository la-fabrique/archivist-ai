#!/usr/bin/env bash
# Stop hook: fires at end of Claude session on a feature branch.
# 1. ALWAYS reminds to commit when the working tree is dirty — work must never
#    be left uncommitted at the end of a session.
# 2. Reminds to run /simplify + the harness-cleaner agent (dev cycle wrap-up).
branch=$(git branch --show-current 2>/dev/null)
[ -n "$branch" ] || exit 0
[ "$branch" != "main" ] && [ "$branch" != "master" ] || exit 0

cleanup="Séquence obligatoire de fin de feature : (1) invoke /simplify sur le code modifié — attendre la fin ; (2) mettre à jour la doc (README, docs/architecture/, ADRs, docs/features/) pour refléter l'état du code — si une commande/feature est supprimée, supprimer son fichier ADR et son fichier .feature, ne pas les garder en 'superseded' ; (3) committer tous les changements ; (4) git push de la branche ; (5) gh pr create pour ouvrir la PR ; (6) lancer le harness-cleaner agent si docs/superpowers/ contient des fichiers liés à la feature."

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
