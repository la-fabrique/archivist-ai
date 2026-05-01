---
name: archivist-cli-dev
description: Use when any file in packages/archivist-cli/ is added, modified, or deleted - covers layer qualification, full test run, and hexagonal architecture verification
---

# Archivist CLI — Workflow de développement

## Vue d'ensemble

Toute modification de `packages/archivist-cli/` déclenche ce workflow en 4 étapes. Ne sauter aucune étape, même pour "juste un test".

## Workflow

### Étape 1 — Qualifier la couche touchée

Identifier les fichiers modifiés et leur couche :

| Couche | Chemins | Contraintes |
|--------|---------|-------------|
| **domain** | `src/archivist_cli/domain/` | Aucun import externe au domaine (pas d'adapters, pas d'application) |
| **application** | `src/archivist_cli/application/` | Peut importer depuis domain uniquement |
| **adapters** | `src/archivist_cli/adapters/` | Implémente les ports de domain ; peut importer des libs externes |
| **cli** | `src/archivist_cli/cli.py`, `registry.py` | Point d'entrée et injection de dépendances uniquement |
| **tests** | `tests/` | Miroir partiel de la structure src/ ; tests de haut niveau dans tests/ directement (test_cli.py, test_registry.py) ; fakes dans `tests/fakes.py` |

### Étape 2 — Lancer les tests

```bash
cd packages/archivist-cli && uv run pytest tests/ -v
```

Résultat attendu : tous les tests passent. Si des tests échouent, diagnostiquer avant de continuer. Ne jamais commiter avec des tests rouges.

### Étape 2b — Vérifier la contrainte de la couche application (si application/ est touché)

Si des fichiers dans `application/` ont été modifiés, vérifier qu'aucun import depuis `adapters/` n'a été introduit :

```bash
grep -rn "from archivist_cli\.adapters\|import archivist_cli\.adapters" \
  packages/archivist-cli/src/archivist_cli/application/
```

Résultat attendu : **aucune sortie**. La couche application ne doit dépendre que du domaine.

### Étape 3 — Vérifier la contrainte hexagonale (si domain/ est touché)

Si des fichiers dans `domain/` ont été modifiés, vérifier qu'aucun import interdit n'a été introduit :

```bash
grep -rn "from archivist_cli\.adapters\|from archivist_cli\.application\|import archivist_cli\.adapters\|import archivist_cli\.application" \
  packages/archivist-cli/src/archivist_cli/domain/
```

Résultat attendu : **aucune sortie**. Toute correspondance est une violation à corriger immédiatement.

### Étape 4 — Vérifier que les adapters implémentent les ports (si adapters/ est touché)

```bash
grep -rn "class.*Referentiel\b\|class.*Filesystem\b" \
  packages/archivist-cli/src/archivist_cli/adapters/
```

In the grep output, confirm each class's parenthesised superclass matches an ABC from `domain/ports.py` (`Referentiel` or `Filesystem`). No second command needed.

## Red Flags — STOP

| Pensée | Réalité |
|--------|---------|
| "C'est juste un refactor, pas besoin de tester" | Les refactors cassent les invariants. Lancer les tests. |
| "J'ai ajouté un import dans domain/ pour simplifier" | Toute dépendance dans domain/ vers adapters/ détruit l'isolation. Revenir en arrière. |
| "L'adapter hérite de la bonne classe, inutile de vérifier" | Vérifier quand même — les ABCs ont une VERSION qui peut changer. |

## Checklist rapide

- [ ] Couche identifiée
- [ ] `uv run pytest tests/ -v` — tous les tests passent
- [ ] Contrainte application vérifiée (si application/ modifié)
- [ ] Contrainte hexagonale vérifiée (si domain/ modifié)
- [ ] Héritage adapters vérifié (si adapters/ modifié)
- [ ] Commit avec message conventionnel : `feat|fix|refactor|test(archivist-cli): <description>`
