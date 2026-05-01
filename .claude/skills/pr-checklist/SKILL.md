---
name: pr-checklist
description: Use before any commit or PR to validate tests, YAML integrity, import cleanliness, and commit message convention
---

# PR Checklist — Validation avant commit / PR

## Vue d'ensemble

4 vérifications à lancer depuis la racine du dépôt avant tout commit sur `main` ou ouverture de PR. Chaque check doit être vert. Ne pas commiter avec un check rouge.

## Workflow

### Check 1 — Tests Python

```bash
cd packages/archivist-cli && uv run pytest tests/ -q
```

Résultat attendu : ligne finale de la forme `X passed` sans `failed` ni `error`.

### Check 2 — Validité du YAML référentiel (si referentiel.yaml modifié)

Applicable uniquement si `packages/referentiel/referentiel.yaml` apparaît dans `git diff --cached --name-only`.

```bash
git diff --cached --name-only | grep -q "referentiel/referentiel.yaml" && \
  uv run python -c "
import yaml, sys
try:
    yaml.safe_load(open('packages/referentiel/referentiel.yaml'))
    print('referentiel.yaml : valide')
except yaml.YAMLError as e:
    print(f'referentiel.yaml INVALIDE : {e}')
    sys.exit(1)
" || echo "referentiel.yaml non modifié — check ignoré"
```

Résultat attendu : `referentiel.yaml : valide` (si le fichier est stagé) ou `referentiel.yaml non modifié — check ignoré`.

### Check 3 — Pas d'imports wildcard dans les fichiers Python stagés

```bash
git diff --cached --name-only | grep '\.py$' | xargs grep -n "from .* import \*" 2>/dev/null
```

Résultat attendu : **aucune sortie**. Toute correspondance est un import wildcard à remplacer par des imports explicites.

### Check 4 — Convention de message de commit

Format attendu : `type(scope): description` où `type` ∈ {feat, fix, refactor, test, docs, chore, ci, style, perf}.

Vérifier le message prévu avant de commiter :

```bash
# Remplacer le message entre guillemets par le message prévu
echo "feat(archivist-cli): add X" | grep -Eq "^(feat|fix|refactor|test|docs|chore|ci|style|perf)(\([a-z][a-z0-9-]*\))?: .{1,}" \
  && echo "conforme" || echo "NON CONFORME — attendu : type(scope): description"
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
| "Un import wildcard c'est juste du sucre syntaxique" | Ça masque les dépendances et rend le code opaque pour l'agent. |

## Checklist rapide

- [ ] `uv run pytest tests/ -q` — tous les tests passent
- [ ] `referentiel.yaml` validé (si modifié dans le staging)
- [ ] Pas d'import wildcard dans les fichiers Python stagés
- [ ] Message de commit au format `type(scope): description`
