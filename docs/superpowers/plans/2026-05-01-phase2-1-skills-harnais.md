# Phase 2.1 — Skills harnais : archivist-cli-dev, docs-gardening, pr-checklist

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create 3 Claude Code skills that automate the key quality workflows for archivist-ai, reducing cognitive load for the agent when touching the CLI, the docs, or preparing a commit.

**Architecture:** Each skill is a SKILL.md file in `.claude/skills/<name>/SKILL.md`. Skills are auto-discovered by Claude Code from this directory — no registration needed. The existing `referentiel-update` skill (`.claude/skills/referentiel-update/SKILL.md`) is the reference format. Skills are invoked via `Skill` tool; they contain a workflow with a checklist the agent follows step-by-step.

**Tech Stack:** Markdown (SKILL.md), bash commands (`uv run pytest`, `grep`, `git`), Python 3.12, uv.

---

## Carte des fichiers

| Action | Chemin |
|--------|--------|
| Create | `.claude/skills/archivist-cli-dev/SKILL.md` |
| Create | `.claude/skills/docs-gardening/SKILL.md` |
| Create | `.claude/skills/pr-checklist/SKILL.md` |

Aucune modification de code applicatif. Aucun test Python à écrire. La "vérification" de chaque skill se fait en l'invoquant manuellement et en vérifiant que les commandes embarquées produisent le résultat attendu.

---

## Task 1 : Skill `archivist-cli-dev`

**Fichiers :**
- Create: `.claude/skills/archivist-cli-dev/SKILL.md`

**Déclencheur :** Toute modification dans `packages/archivist-cli/` — nouveau fichier, refactor, bugfix, ajout de test.

**Ce que la skill doit faire :**
1. Qualifier la couche touchée (domain / application / adapters / cli / tests)
2. Lancer les tests complets
3. Vérifier la contrainte hexagonale : `domain/` ne doit rien importer depuis `adapters/` ni depuis `application/`
4. Vérifier que les adapters implémentent bien les ports déclarés dans `domain/ports.py`

**Contrainte hexagonale — commandes concrètes :**

```bash
# Vérifier qu'aucun fichier domain/ n'importe depuis adapters/ ou application/
grep -rn "from archivist_cli\.adapters\|from archivist_cli\.application\|import archivist_cli\.adapters\|import archivist_cli\.application" \
  packages/archivist-cli/src/archivist_cli/domain/
# Résultat attendu : aucune sortie (0 correspondances)
```

```bash
# Vérifier que les adapters déclarent bien les classes concrètes des ports
grep -n "class.*Referentiel\b\|class.*Filesystem\b" \
  packages/archivist-cli/src/archivist_cli/adapters/referentiel/yaml_file.py \
  packages/archivist-cli/src/archivist_cli/adapters/fs/local.py
# Résultat attendu : au moins une ligne par fichier (YamlFileReferentiel, LocalFilesystem, etc.)
```

- [ ] **Étape 1 : Créer `.claude/skills/archivist-cli-dev/SKILL.md`**

Contenu exact à écrire :

```markdown
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
| **tests** | `tests/` | Miroir de la structure src/ ; fakes dans `tests/fakes.py` |

### Étape 2 — Lancer les tests

```bash
cd packages/archivist-cli && uv run pytest tests/ -v
```

Résultat attendu : tous les tests passent. Si des tests échouent, diagnostiquer avant de continuer. Ne jamais commiter avec des tests rouges.

### Étape 3 — Vérifier la contrainte hexagonale (si domain/ est touché)

Si des fichiers dans `domain/` ont été modifiés, vérifier qu'aucun import interdit n'a été introduit :

```bash
grep -rn "from archivist_cli\.adapters\|from archivist_cli\.application\|import archivist_cli\.adapters\|import archivist_cli\.application" \
  packages/archivist-cli/src/archivist_cli/domain/
```

Résultat attendu : **aucune sortie**. Toute correspondance est une violation à corriger immédiatement.

### Étape 4 — Vérifier que les adapters implémentent les ports (si adapters/ est touché)

```bash
grep -n "class.*Referentiel\b\|class.*Filesystem\b" \
  packages/archivist-cli/src/archivist_cli/adapters/referentiel/yaml_file.py \
  packages/archivist-cli/src/archivist_cli/adapters/fs/local.py
```

Vérifier que les classes concrètes trouvées héritent bien des ABCs déclarées dans `domain/ports.py` (`Referentiel`, `Filesystem`).

## Red Flags — STOP

| Pensée | Réalité |
|--------|---------|
| "C'est juste un refactor, pas besoin de tester" | Les refactors cassent les invariants. Lancer les tests. |
| "J'ai ajouté un import dans domain/ pour simplifier" | Toute dépendance dans domain/ vers adapters/ détruit l'isolation. Revenir en arrière. |
| "L'adapter hérite de la bonne classe, inutile de vérifier" | Vérifier quand même — les ABCs ont une VERSION qui peut changer. |

## Checklist rapide

- [ ] Couche identifiée
- [ ] `uv run pytest tests/ -v` — tous les tests passent
- [ ] Contrainte hexagonale vérifiée (si domain/ modifié)
- [ ] Héritage adapters vérifié (si adapters/ modifié)
- [ ] Commit avec message conventionnel : `feat|fix|refactor|test(archivist-cli): <description>`
```

- [ ] **Étape 2 : Vérifier que la skill est bien découverte**

```bash
ls /home/deka/sources/github/archivist-ai/.claude/skills/
```
Résultat attendu : `archivist-cli-dev/` apparaît dans la liste aux côtés de `referentiel-update/`.

- [ ] **Étape 3 : Smoke test — lancer la commande de vérification hexagonale à la main**

```bash
grep -rn "from archivist_cli\.adapters\|from archivist_cli\.application\|import archivist_cli\.adapters\|import archivist_cli\.application" \
  packages/archivist-cli/src/archivist_cli/domain/
```
Résultat attendu : aucune sortie (le domaine actuel est propre).

- [ ] **Étape 4 : Smoke test — lancer les tests**

```bash
cd packages/archivist-cli && uv run pytest tests/ -v --tb=short 2>&1 | tail -20
```
Résultat attendu : toutes les suites passent.

- [ ] **Étape 5 : Commit**

```bash
git add .claude/skills/archivist-cli-dev/SKILL.md
git commit -m "feat(harnais): add archivist-cli-dev skill — hexagonal workflow"
```

---

## Task 2 : Skill `docs-gardening`

**Fichiers :**
- Create: `.claude/skills/docs-gardening/SKILL.md`

**Déclencheur :** Invocation manuelle (`/docs-gardening`) ou périodique. Utilisée pour détecter les dérives de documentation avant qu'elles s'accumulent.

**Ce que la skill doit faire :**
1. Vérifier que chaque `packages/*/` est documenté dans `CLAUDE.md`
2. Détecter les liens markdown cassés dans `packages/referentiel/`
3. Signaler les plans dans `docs/superpowers/plans/` qui semblent obsolètes (fichiers datant de plus de 30 jours sans référence à "actif" ou "en cours")
4. Produire une liste de corrections proposées — ne rien modifier automatiquement

**Commandes concrètes :**

```bash
# Lister les packages présents
ls packages/
```

```bash
# Vérifier la couverture dans CLAUDE.md
grep -c "packages/" CLAUDE.md
```

```bash
# Détecter les liens markdown cassés dans packages/referentiel/
# (liens de la forme [texte](fichier.md) qui pointent vers un fichier inexistant)
grep -rn "\[.*\](.*\.md)" packages/referentiel/ | \
  grep -v "^Binary" | \
  awk -F'(' '{print $2}' | \
  tr -d ')' | \
  while read link; do
    base=$(dirname "$(grep -rl "$link" packages/referentiel/ | head -1)")
    target="$base/$link"
    [ ! -f "$target" ] && echo "Lien cassé : $link (dans $base)"
  done
```

- [ ] **Étape 1 : Créer `.claude/skills/docs-gardening/SKILL.md`**

```markdown
---
name: docs-gardening
description: Use on manual invocation to detect documentation drift - broken markdown links, undocumented packages, and stale plans in docs/superpowers/plans/
---

# Docs Gardening — Détection de dérives documentaires

## Vue d'ensemble

Ce workflow inspecte l'état de la documentation et produit une liste de corrections à apporter. Il ne modifie rien automatiquement — il signale, l'humain (ou l'agent sur confirmation) corrige.

## Workflow

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

```bash
grep -rn "\[.*\](.*\.md)" packages/referentiel/ 2>/dev/null | while IFS=: read file line rest; do
  link=$(echo "$rest" | grep -oP '\]\(\K[^)]+')
  [ -z "$link" ] && continue
  base=$(dirname "$file")
  target="$base/$link"
  [ ! -f "$target" ] && echo "CASSÉ : $file:$line → $target"
done
```

Résultat attendu : aucune sortie. Chaque ligne produite est un lien à corriger.

### Étape 3 — Détecter les plans potentiellement obsolètes

```bash
find docs/superpowers/plans/ -name "*.md" -mtime +30 | sort
```

Pour chaque fichier retourné, vérifier si son contenu contient des indicateurs d'activité (`en cours`, `actif`, `TODO`, `- [ ]`). Un plan ancien sans tâches ouvertes est terminé ou obsolète.

```bash
for f in $(find docs/superpowers/plans/ -name "*.md" -mtime +30); do
  open=$(grep -c "\- \[ \]" "$f" 2>/dev/null || echo 0)
  echo "$f : $open tâches ouvertes"
done
```

### Étape 4 — Produire le rapport

Synthétiser les résultats :

```
## Rapport docs-gardening — YYYY-MM-DD

### Packages non documentés dans CLAUDE.md
- (liste ou "aucun")

### Liens markdown cassés
- (liste ou "aucun")

### Plans potentiellement obsolètes
- (liste avec nb de tâches ouvertes)
```

Proposer les corrections sans les appliquer. Attendre confirmation avant de modifier quoi que ce soit.

## Red Flags — STOP

| Pensée | Réalité |
|--------|---------|
| "Ce lien est juste mal formaté, inutile de le signaler" | Signaler quand même — l'agent le lit comme du texte mort. |
| "Le plan est ancien mais toujours utile" | Signaler avec contexte — l'humain décide de l'archiver ou pas. |
| "CLAUDE.md mentionne le package indirectement" | Une mention implicite ne suffit pas — un pointeur explicite est requis. |

## Checklist rapide

- [ ] Packages listés et croisés avec CLAUDE.md
- [ ] Liens markdown vérifiés dans packages/referentiel/
- [ ] Plans anciens identifiés et classés par nb de tâches ouvertes
- [ ] Rapport produit en texte clair
```

- [ ] **Étape 2 : Smoke test — couverture CLAUDE.md**

```bash
ls /home/deka/sources/github/archivist-ai/packages/ && echo "---" && grep "packages/" /home/deka/sources/github/archivist-ai/CLAUDE.md
```
Vérifier manuellement que chaque dossier a une ligne dans CLAUDE.md.

- [ ] **Étape 3 : Smoke test — liens markdown**

```bash
grep -rn "\[.*\](.*\.md)" /home/deka/sources/github/archivist-ai/packages/referentiel/ 2>/dev/null | head -20
```
Vérifier visuellement que les liens trouvés semblent pointer vers des fichiers existants.

- [ ] **Étape 4 : Commit**

```bash
git add .claude/skills/docs-gardening/SKILL.md
git commit -m "feat(harnais): add docs-gardening skill — documentation drift detection"
```

---

## Task 3 : Skill `pr-checklist`

**Fichiers :**
- Create: `.claude/skills/pr-checklist/SKILL.md`

**Déclencheur :** Avant chaque commit ou PR. Utilisée pour valider que le changement est propre avant d'atterrir sur `main`.

**Ce que la skill doit faire :**
1. Vérifier que les tests Python passent
2. Valider le YAML du référentiel (si `packages/referentiel/referentiel.yaml` est touché)
3. Détecter les imports wildcard (`from x import *`) dans les fichiers Python modifiés
4. Vérifier que le message de commit suit la convention `type(scope): description`

**Commandes concrètes :**

```bash
# Tests Python
cd packages/archivist-cli && uv run pytest tests/ -q 2>&1 | tail -5
```

```bash
# Validation YAML du référentiel
uv run python -c "
import yaml, sys
try:
    yaml.safe_load(open('packages/referentiel/referentiel.yaml'))
    print('referentiel.yaml : valide')
except yaml.YAMLError as e:
    print(f'referentiel.yaml INVALIDE : {e}')
    sys.exit(1)
"
```

```bash
# Imports wildcard dans les fichiers Python stagés
git diff --cached --name-only | grep '\.py$' | xargs grep -n "from .* import \*" 2>/dev/null
```

```bash
# Vérification du format du message de commit (dernier commit)
git log -1 --format="%s" | grep -Eq "^(feat|fix|refactor|test|docs|chore|ci|style|perf)(\([a-z-]+\))?: .+" \
  && echo "Message de commit : conforme" \
  || echo "ATTENTION : message de commit non conforme — attendu : type(scope): description"
```

- [ ] **Étape 1 : Créer `.claude/skills/pr-checklist/SKILL.md`**

```markdown
---
name: pr-checklist
description: Use before any commit or PR to validate tests, YAML integrity, import cleanliness, and commit message convention
---

# PR Checklist — Validation avant commit / PR

## Vue d'ensemble

4 vérifications à lancer dans l'ordre avant tout commit sur `main` ou ouverture de PR. Chaque check doit être vert. Ne pas commiter avec un check rouge.

## Workflow

### Check 1 — Tests Python

```bash
cd packages/archivist-cli && uv run pytest tests/ -q
```

Résultat attendu : ligne finale de la forme `X passed` sans `failed` ni `error`.

### Check 2 — Validité du YAML référentiel (si referentiel.yaml modifié)

Applicable uniquement si `packages/referentiel/referentiel.yaml` apparaît dans `git diff --cached --name-only`.

```bash
uv run python -c "
import yaml, sys
try:
    yaml.safe_load(open('packages/referentiel/referentiel.yaml'))
    print('referentiel.yaml : valide')
except yaml.YAMLError as e:
    print(f'referentiel.yaml INVALIDE : {e}')
    sys.exit(1)
"
```

Résultat attendu : `referentiel.yaml : valide`. Toute erreur YAML doit être corrigée avant de continuer.

### Check 3 — Pas d'imports wildcard dans les fichiers Python stagés

```bash
git diff --cached --name-only | grep '\.py$' | xargs grep -n "from .* import \*" 2>/dev/null
```

Résultat attendu : **aucune sortie**. Les imports wildcard masquent les dépendances et rendent le code difficile à analyser pour l'agent.

### Check 4 — Convention de message de commit

Format attendu : `type(scope): description` où `type` est l'un de : `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `ci`, `style`, `perf`.

Vérifier le message prévu avant de commiter :

```bash
# Remplacer "feat(archivist-cli): add X" par le message prévu
echo "feat(archivist-cli): add X" | grep -Eq "^(feat|fix|refactor|test|docs|chore|ci|style|perf)(\([a-z-]+\))?: .+" \
  && echo "conforme" || echo "non conforme"
```

Exemples valides :
- `feat(archivist-cli): add scaffold dry-run flag`
- `fix(referentiel): correct broken link in classement/`
- `test(archivist-cli): add adapter contract tests`
- `docs(harnais): add docs-gardening skill`

## Red Flags — STOP

| Pensée | Réalité |
|--------|---------|
| "Les tests passaient avant mon changement" | Les tester maintenant. Les régressions existent. |
| "Le YAML est valide, je l'ai écrit à la main" | Le parser YAML voit des choses que l'œil humain rate. |
| "Le scope est optionnel dans les commits" | Il est optionnel dans la spec, mais obligatoire ici pour la traçabilité. |

## Checklist rapide

- [ ] `uv run pytest tests/ -q` — tous les tests passent
- [ ] `referentiel.yaml` validé (si modifié)
- [ ] Pas d'import wildcard dans les fichiers Python stagés
- [ ] Message de commit au format `type(scope): description`
```

- [ ] **Étape 2 : Smoke test — lancer les checks sur l'état actuel**

```bash
cd /home/deka/sources/github/archivist-ai/packages/archivist-cli && uv run pytest tests/ -q 2>&1 | tail -5
```
Résultat attendu : tous les tests passent.

```bash
cd /home/deka/sources/github/archivist-ai && uv run python -c "
import yaml, sys
try:
    yaml.safe_load(open('packages/referentiel/referentiel.yaml'))
    print('referentiel.yaml : valide')
except Exception as e:
    print(f'INVALIDE : {e}')
    sys.exit(1)
" 2>/dev/null || echo "(referentiel.yaml absent ou non applicable)"
```

- [ ] **Étape 3 : Commit**

```bash
git add .claude/skills/pr-checklist/SKILL.md
git commit -m "feat(harnais): add pr-checklist skill — pre-commit validation"
```

---

## Self-review

### Couverture de la spec (Phase 2.1)

| Exigence | Task |
|----------|------|
| Skill `archivist-cli-dev` : qualifier changement, lancer tests, vérifier architecture hexagonale | Task 1 |
| Skill `docs-gardening` : détecter incohérences docs/, CLAUDE.md, plans obsolètes | Task 2 |
| Skill `pr-checklist` : tests, YAML valide, imports propres, convention commit | Task 3 |

Couverture complète.

### Scan placeholders

Aucun "TBD", "TODO", "implement later", "fill in details", ou "similar to Task N" dans ce document.

### Cohérence des commandes

- `uv run pytest tests/ -v` en Task 1, `uv run pytest tests/ -q` en Task 3 : intentionnel (`-v` pour debug en dev, `-q` pour check rapide avant commit). Les deux sont valides.
- Les chemins `packages/archivist-cli/src/archivist_cli/domain/` sont cohérents avec la structure réelle du dépôt.
- `packages/referentiel/referentiel.yaml` : à vérifier que le fichier existe avant d'intégrer le Check 2 dans la skill. Si le fichier n'existe pas encore, le check ne s'applique pas (la skill le précise avec "si referentiel.yaml modifié").
