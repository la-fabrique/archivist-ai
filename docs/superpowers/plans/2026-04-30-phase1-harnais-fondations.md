# Phase 1 — Fondations harnais archivist-ai

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Mettre en place les fondations du harnais : CLAUDE.md structuré comme table des matières, règle de formalisation des décisions, et 4 vérifications mécaniques en CI.

**Architecture:** 3 scripts Python dans `scripts/` (validation YAML, liens markdown, couverture CLAUDE.md) + 1 workflow GitHub Actions `ci.yml` qui les orchestre avec les tests pytest existants. Le CLAUDE.md est enrichi avec une "Carte du dépôt" et une règle sur les décisions. Les scripts utilisent PyYAML (déjà dans le projet) ; le CI les installe via `pip install pyyaml`.

**Tech Stack:** Python 3.12 stdlib + PyYAML, GitHub Actions, pytest (existant dans `packages/archivist-cli/`)

---

## Fichiers touchés

| Fichier | Action |
|---------|--------|
| `CLAUDE.md` | Modify — ajouter "Carte du dépôt" + règle décisions |
| `scripts/check_referentiel_yaml.py` | Create — validation YAML + schéma |
| `scripts/check_claude_coverage.py` | Create — chaque `packages/*/` documenté dans CLAUDE.md |
| `package.json` | Modify — ajouter `devDependencies` remark-cli + remark-validate-links + script `check:links` |
| `.remarkrc.yml` | Create — configuration remark (plugin + scope) |
| `.github/workflows/ci.yml` | Create — workflow CI pour push/PR sur main |

---

## Task 1 : Enrichir CLAUDE.md (points 1.1 et 1.2)

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1 : Lire l'état actuel**

```bash
cat CLAUDE.md
```

- [ ] **Step 2 : Ajouter "Carte du dépôt" et règle décisions**

Ajouter à la fin de `CLAUDE.md` :

```markdown
## Carte du dépôt

- `docs/vision-strategie.md` — vision produit, mission, objectifs
- `docs/architecture/` — diagrammes et décisions d'architecture
- `docs/superpowers/specs/` — décisions de conception (ADR) — *si une décision changerait le comportement de Claude Code, elle doit y être*
- `docs/superpowers/plans/` — plans d'exécution actifs et terminés
- `packages/referentiel/` — sources du référentiel (contenu documentaire, pas code)
- `packages/referentiel-cli/` — CLI développeur TypeScript (génération, validation, export)
- `packages/archivist-cli/` — CLI utilisateur final Python (classement de documents)
- `packages/landing/` — site vitrine

## Décisions dans le dépôt

Toute décision non-triviale qui changerait le comportement de Claude Code doit être dans `docs/superpowers/specs/` sous forme d'ADR. Les décisions orales ou Slack sont invisibles pour l'agent.
```

- [ ] **Step 3 : Commit**

```bash
git add CLAUDE.md
git commit -m "docs(claude): add repo map and decision-capture rule"
```

---

## Task 2 : Script de validation referentiel.yaml

**Files:**
- Create: `scripts/check_referentiel_yaml.py`

- [ ] **Step 1 : Créer le script**

```python
#!/usr/bin/env python3
"""Validate referentiel.yaml against the expected schema.

Usage (from repo root): python scripts/check_referentiel_yaml.py
Exit 0 = valid, exit 1 = errors (with actionable messages).
"""
import sys
import yaml
from pathlib import Path

REQUIRED_FIELDS = {
    "id", "folder_name", "path", "dynamic",
    "option", "required", "description", "organization",
}

def validate(path: Path) -> list[str]:
    errors = []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        return [f"referentiel.yaml invalide : erreur YAML — {e}"]

    if not isinstance(data, list):
        return ["referentiel.yaml doit être une liste d'entrées à la racine"]

    for i, entry in enumerate(data):
        if not isinstance(entry, dict):
            errors.append(f"Entrée {i} : doit être un objet, pas {type(entry).__name__}")
            continue
        missing = REQUIRED_FIELDS - entry.keys()
        if missing:
            entry_id = entry.get("id", f"#{i}")
            for field in sorted(missing):
                errors.append(
                    f"Entrée '{entry_id}' : le champ '{field}' est requis — "
                    f"ajouter `{field}: <valeur>` à cette entrée"
                )

    return errors


def main() -> None:
    path = Path("packages/referentiel/referentiel.yaml")
    if not path.exists():
        print(f"ERREUR : {path} introuvable — vérifier le chemin depuis la racine du dépôt")
        sys.exit(1)

    errors = validate(path)
    if errors:
        print("referentiel.yaml invalide :")
        for e in errors:
            print(f"  • {e}")
        sys.exit(1)

    print(f"referentiel.yaml valide ({path}).")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2 : Tester localement (doit passer)**

```bash
python scripts/check_referentiel_yaml.py
```

Sortie attendue : `referentiel.yaml valide (packages/referentiel/referentiel.yaml).`

- [ ] **Step 3 : Vérifier qu'une entrée cassée est détectée**

```bash
# Créer un fichier de test temporaire
python -c "
import yaml, pathlib, subprocess, sys
bad = [{'id': 'test', 'folder_name': 'Test'}]  # missing required fields
pathlib.Path('/tmp/test_ref.yaml').write_text(yaml.dump(bad))
"
# Vérifier le script sur ce fichier cassé (adapter temporairement le chemin pour valider la logique)
python -c "
import sys; sys.path.insert(0, 'scripts')
import yaml
from pathlib import Path
exec(open('scripts/check_referentiel_yaml.py').read().replace('\"packages/referentiel/referentiel.yaml\"', '\"/tmp/test_ref.yaml\"'))
" 2>&1 | grep "requis" || echo "ERREUR : le script n'a pas détecté les champs manquants"
```

Sortie attendue : plusieurs lignes `• Entrée 'test' : le champ '...' est requis`

- [ ] **Step 4 : Commit**

```bash
git add scripts/check_referentiel_yaml.py
git commit -m "ci: add referentiel.yaml schema validator"
```

---

## Task 3 : Vérification des liens markdown avec remark

**Files:**
- Modify: `package.json` — ajouter devDependencies + script `check:links`
- Create: `.remarkrc.yml` — configuration remark-validate-links

remark-validate-links suit la spec Markdown, résout les ancres (`#section`), et vérifie les liens inter-fichiers de façon fiable. Pas de regex à maintenir.

- [ ] **Step 1 : Ajouter les dépendances dans package.json**

Ajouter la section `devDependencies` et le script dans `package.json` :

```json
{
  "name": "archivist-ai",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "landing:install": "npm install --prefix packages/landing",
    "landing:dev": "npm run dev --prefix packages/landing",
    "landing:build": "npm run build --prefix packages/landing",
    "landing:preview": "npm run preview --prefix packages/landing",
    "referentiel-cli:install": "npm install --prefix packages/referentiel-cli",
    "referentiel-cli:build": "npm run build --prefix packages/referentiel-cli",
    "referentiel-cli:test": "npm run test --prefix packages/referentiel-cli",
    "referentiel-cli:push": "REFERENTIEL_CLI_GOOGLE_CLIENT_SECRET=./client_secret.json REFERENTIEL_CLI_PARENT_FOLDER_ID=1tWrWxfTrn-3pIlaYH1Dbsy6R555eCXdw node packages/referentiel-cli/dist/cli.js push",
    "referentiel-cli:help": "node packages/referentiel-cli/dist/cli.js help",
    "referentiel-cli:export-frontmatters": "node packages/referentiel-cli/dist/cli.js export-frontmatters",
    "referentiel-cli:generate-pdf": "node packages/referentiel-cli/dist/cli.js generate-pdf --referentiel-root packages/referentiel --output referentiel.pdf",
    "archivist-cli:build": "cd packages/archivist-cli && uv run pyinstaller archivist-cli.spec --distpath dist",
    "check:links": "remark --use remark-validate-links --frail packages/referentiel/"
  },
  "devDependencies": {
    "remark-cli": "^12.0.0",
    "remark-validate-links": "^13.0.0"
  }
}
```

- [ ] **Step 2 : Créer `.remarkrc.yml`**

```yaml
plugins:
  - remark-validate-links
```

La configuration est minimale : remark-validate-links détecte automatiquement les liens relatifs inter-fichiers et les ancres dans les fichiers `.md`. Les URLs externes sont ignorées par défaut.

- [ ] **Step 3 : Installer les dépendances**

```bash
npm install
```

Vérifie que `node_modules/remark-cli` et `node_modules/remark-validate-links` sont présents.

- [ ] **Step 4 : Tester localement (doit passer)**

```bash
npm run check:links
```

Sortie attendue : pas d'erreur, remark affiche les fichiers traités sans `warning` ni `error`. Exit code 0.

Le flag `--frail` fait échouer (exit 1) dès qu'il y a au moins un warning — nécessaire pour que le CI bloque.

Si des liens cassés apparaissent, les corriger avant de continuer.

- [ ] **Step 5 : Commit**

```bash
git add package.json package-lock.json .remarkrc.yml
git commit -m "ci: add remark-validate-links for markdown link checking"
```

---

## Task 4 : Script de couverture CLAUDE.md

**Files:**
- Create: `scripts/check_claude_coverage.py`

- [ ] **Step 1 : Créer le script**

```python
#!/usr/bin/env python3
"""Ensure every packages/* directory is documented in CLAUDE.md.

Usage (from repo root): python scripts/check_claude_coverage.py
Exit 0 = all packages covered, exit 1 = gaps (with actionable messages).
"""
import sys
from pathlib import Path


def main() -> None:
    packages_dir = Path("packages")
    claude_md = Path("CLAUDE.md")

    if not packages_dir.exists():
        print(f"ERREUR : {packages_dir} introuvable")
        sys.exit(1)
    if not claude_md.exists():
        print(f"ERREUR : {claude_md} introuvable")
        sys.exit(1)

    content = claude_md.read_text(encoding="utf-8")
    packages = sorted(p.name for p in packages_dir.iterdir() if p.is_dir())

    errors = []
    for pkg in packages:
        if pkg not in content:
            errors.append(
                f"Le package '{pkg}' n'est pas documenté dans CLAUDE.md — "
                f"ajouter une entrée `packages/{pkg}/` dans la section 'Carte du dépôt'"
            )

    if errors:
        print("Couverture CLAUDE.md incomplète :")
        for e in errors:
            print(f"  • {e}")
        sys.exit(1)

    print(f"CLAUDE.md couvre tous les packages ({len(packages)} vérifiés : {', '.join(packages)}).")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2 : Tester localement**

```bash
python scripts/check_claude_coverage.py
```

Sortie attendue (après Task 1) : `CLAUDE.md couvre tous les packages (4 vérifiés : archivist-cli, landing, referentiel, referentiel-cli).`

Si `landing` ou un autre package manque, vérifier que Task 1 a bien ajouté la "Carte du dépôt" à CLAUDE.md.

- [ ] **Step 3 : Commit**

```bash
git add scripts/check_claude_coverage.py
git commit -m "ci: add CLAUDE.md package coverage checker"
```

---

## Task 5 : Workflow CI GitHub Actions

**Files:**
- Create: `.github/workflows/ci.yml`

- [ ] **Step 1 : Créer le workflow**

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  checks:
    name: Vérifications mécaniques
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"

      - name: Install npm dependencies
        run: npm ci

      - name: Install Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install PyYAML
        run: pip install pyyaml

      - name: Valider referentiel.yaml
        run: python scripts/check_referentiel_yaml.py

      - name: Vérifier liens markdown
        run: npm run check:links

      - name: Vérifier couverture CLAUDE.md
        run: python scripts/check_claude_coverage.py

  tests:
    name: Tests archivist-cli
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: uv sync --frozen
        working-directory: packages/archivist-cli

      - name: Run tests
        run: uv run pytest tests/ -v
        working-directory: packages/archivist-cli
```

- [ ] **Step 2 : Vérifier la syntaxe YAML du workflow**

```bash
python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml').read()); print('YAML valide')"
```

Sortie attendue : `YAML valide`

- [ ] **Step 3 : Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "ci: add CI workflow with 4 mechanical checks"
```

---

## Task 6 : Validation finale locale

**Files:** aucun (vérification uniquement)

- [ ] **Step 1 : Lancer tous les checks depuis la racine**

```bash
pip install pyyaml 2>/dev/null
python scripts/check_referentiel_yaml.py && \
npm run check:links && \
python scripts/check_claude_coverage.py && \
echo "--- Tous les checks passent ---"
```

Sortie attendue :
```
referentiel.yaml valide (packages/referentiel/referentiel.yaml).
packages/referentiel/ ... (remark sans warning ni error)
CLAUDE.md couvre tous les packages (4 vérifiés : archivist-cli, landing, referentiel, referentiel-cli).
--- Tous les checks passent ---
```

- [ ] **Step 2 : Lancer les tests Python**

```bash
cd packages/archivist-cli && uv run pytest tests/ -v
```

Sortie attendue : tous les tests passent (PASSED).

- [ ] **Step 3 : Vérifier que la branche est propre**

```bash
git status
```

Aucun fichier non commité.

---

## Self-Review

### Couverture spec

| Préco feuille de route | Tâche |
|------------------------|-------|
| 1.1 CLAUDE.md = table des matières avec "Carte du dépôt" | Task 1 |
| 1.2 Décisions formalisées dans le dépôt (règle ADR) | Task 1 |
| 1.3 Check referentiel.yaml valide | Task 2 + Task 5 |
| 1.3 Check liens markdown non cassés | Task 3 (remark-validate-links) + Task 5 |
| 1.3 Check couverture CLAUDE.md | Task 4 + Task 5 |
| 1.3 Tests Python passent en CI | Task 5 (job `tests`) |

Toutes les préconisations de Phase 1 sont couvertes. ✓

### Messages d'erreur actionnables

Chaque script produit des messages du type "le champ X est requis — ajouter `X: <valeur>`" ou "lien cassé dans Y : 'Z' n'existe pas — corriger le chemin ou créer la cible". Conforme à la préco "messages d'erreur = instructions de correction". ✓

### Cohérence des types

- Les scripts s'appellent tous depuis la racine du dépôt avec `python scripts/check_*.py` ✓
- Le workflow CI utilise la même commande que les tests locaux ✓
- PyYAML est la seule dépendance externe des scripts, installée explicitement ✓
