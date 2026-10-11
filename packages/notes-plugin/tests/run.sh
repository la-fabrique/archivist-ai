#!/usr/bin/env bash
# Lance tous les tests/test-*.sh ; sort en échec si l'un d'eux échoue.
HERE=$(cd "$(dirname "$0")" && pwd)
failed=()
for f in "$HERE"/test-*.sh; do
  echo "== $(basename "$f")"
  bash "$f" || failed+=("$(basename "$f")")
done
if [ "${#failed[@]}" -gt 0 ]; then
  echo "Échec : ${failed[*]}"
  exit 1
fi
echo "Tous les fichiers de tests passent"
