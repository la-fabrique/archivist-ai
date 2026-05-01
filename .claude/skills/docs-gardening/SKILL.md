---
name: docs-gardening
description: Use on manual invocation to detect documentation drift - broken markdown links, undocumented packages, and stale plans in docs/superpowers/plans/
---

# Docs Gardening — Détection de dérives documentaires

## Vue d'ensemble

Ce workflow inspecte l'état de la documentation et produit une liste de corrections à apporter. Il ne modifie rien automatiquement — il signale, l'humain (ou l'agent sur confirmation) corrige.

## Workflow

Toutes les commandes s'exécutent depuis la racine du dépôt (`/home/deka/sources/github/archivist-ai` ou équivalent).

### Étape 1 — Vérifier la couverture des packages dans CLAUDE.md

```bash
ls packages/
```

Pour chaque dossier listé, vérifier qu'une ligne de `CLAUDE.md` le mentionne :

```bash
grep "packages/" CLAUDE.md
```

Packages non mentionnés → à documenter dans la section "Carte du dépôt" de `CLAUDE.md`.

### Étape 2 — Détecter les liens markdown cassés dans packages/referentiel/

Note : le scan se limite à `packages/referentiel/` car c'est le seul corpus documentaire avec des liens internes entre fichiers. Les plans dans `docs/superpowers/plans/` pointent vers des fichiers externes ou GitHub — hors scope de ce check.

```bash
grep -rn "\[.*\](.*\.md)" packages/referentiel/ 2>/dev/null | while IFS=: read file line rest; do
  echo "$rest" | grep -oP '\]\(\K[^)]+' | while read -r link; do
    [ -z "$link" ] && continue
    base=$(dirname "$file")
    target="$base/${link%%#*}"
    [ ! -f "$target" ] && echo "CASSÉ : $file:$line → $link"
  done
done
```

Résultat attendu : aucune sortie. Chaque ligne produite est un lien à corriger.

### Étape 3 — Détecter les plans potentiellement obsolètes

Identifier les plans dont le dernier commit date de plus de 30 jours :

```bash
# Lister les plans avec leur date de dernier commit
git log --format="" --name-only -- docs/superpowers/plans/*.md | sort -u | while read -r f; do
  [ -z "$f" ] && continue
  age=$(git log -1 --format="%ar" -- "$f" 2>/dev/null)
  open=$(grep -c "\- \[ \]" "$f" 2>/dev/null || echo 0)
  days=$(git log -1 --format="%ct" -- "$f" 2>/dev/null)
  now=$(date +%s)
  [ -n "$days" ] && diff=$(( (now - days) / 86400 )) || diff=0
  [ "$diff" -gt 30 ] && echo "$f : dernier commit il y a $age ($open tâches ouvertes)"
done
```

Un plan ancien avec 0 tâches ouvertes est terminé ou obsolète — signaler pour archivage ou suppression.

### Étape 4 — Produire le rapport

Synthétiser les résultats sous cette forme :

```
## Rapport docs-gardening — YYYY-MM-DD

### Packages non documentés dans CLAUDE.md
- (liste ou "aucun")

### Liens markdown cassés
- (liste ou "aucun")

### Plans potentiellement obsolètes (> 30 jours, 0 tâches ouvertes)
- (liste ou "aucun")
```

Ne proposer des corrections que si demandé. Ne rien modifier sans confirmation.

## Red Flags — STOP

| Pensée | Réalité |
|--------|---------|
| "Ce lien est juste mal formaté, inutile de le signaler" | Signaler quand même — l'agent le lit comme du texte mort. |
| "Le plan est ancien mais toujours utile" | Signaler avec contexte — l'humain décide de l'archiver ou pas. |
| "CLAUDE.md mentionne le package indirectement" | Une mention implicite ne suffit pas — un pointeur explicite est requis. |
| "Je vais corriger les liens cassés directement" | Ce workflow signale uniquement. Attendre confirmation avant de modifier. |

## Checklist rapide

- [ ] `ls packages/` croisé avec `grep "packages/" CLAUDE.md`
- [ ] Liens markdown vérifiés dans `packages/referentiel/`
- [ ] Plans > 30 jours identifiés et classés par nb de tâches ouvertes
- [ ] Rapport produit en texte clair
- [ ] Aucune modification effectuée sans confirmation
