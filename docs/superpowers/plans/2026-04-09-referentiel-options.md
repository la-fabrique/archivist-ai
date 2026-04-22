# Referentiel : profils → options — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remplacer le mécanisme de profils prédéfinis dans le référentiel par un système d'options cumulables sur un `core`, sans changer la structure des dossiers ni les règles.

**Architecture:** Chaque fichier `.md` du classement perd son champ `profiles:` et son champ `module:` devient `option:`. La section "Modules et profils" de `__index.md` est remplacée par une section "Options" sans tableau de profils. Les profils prédéfinis subsistent uniquement dans `demarrage-rapide.md` comme exemples documentaires.

**Tech Stack:** Markdown, frontmatter YAML. Pas de code à écrire — uniquement des éditions de fichiers `.md`.

---

### Task 1 : Frontmatter des fichiers `core`

Mettre à jour les 6 fichiers dont `option: core`.

**Files:**
- Modify: `packages/referentiel/classement/mes_ventes.md` (ligne 3-4)
- Modify: `packages/referentiel/classement/mes_achats.md` (ligne 3-4)
- Modify: `packages/referentiel/classement/mon_juridique.md` (ligne 3-4)
- Modify: `packages/referentiel/classement/ma_fiscalite.md` (ligne 3-4)
- Modify: `packages/referentiel/classement/ma_banque.md` (ligne 3-4)
- Modify: `packages/referentiel/classement/archives.md` (ligne 3-4)

- [ ] **Step 1 : Éditer `mes_ventes.md`**

Remplacer dans le frontmatter :
```yaml
module: core
profiles: [indep-solo-micro, sasu-solo, sasu-solo-employe, indep-creatif-tech]
```
par :
```yaml
option: core
```

- [ ] **Step 2 : Éditer `mes_achats.md`**

Remplacer dans le frontmatter :
```yaml
module: core
profiles: [indep-solo-micro, sasu-solo, sasu-solo-employe, indep-creatif-tech]
```
par :
```yaml
option: core
```

- [ ] **Step 3 : Éditer `mon_juridique.md`**

Remplacer dans le frontmatter :
```yaml
module: core
profiles: [indep-solo-micro, sasu-solo, sasu-solo-employe, indep-creatif-tech]
```
par :
```yaml
option: core
```

- [ ] **Step 4 : Éditer `ma_fiscalite.md`**

Remplacer dans le frontmatter :
```yaml
module: core
profiles: [indep-solo-micro, sasu-solo, sasu-solo-employe, indep-creatif-tech]
```
par :
```yaml
option: core
```

- [ ] **Step 5 : Éditer `ma_banque.md`**

Remplacer dans le frontmatter :
```yaml
module: core
profiles: [indep-solo-micro, sasu-solo, sasu-solo-employe, indep-creatif-tech]
```
par :
```yaml
option: core
```

- [ ] **Step 6 : Éditer `archives.md`**

Remplacer dans le frontmatter :
```yaml
module: core
profiles: [indep-solo-micro, sasu-solo, sasu-solo-employe, indep-creatif-tech]
```
par :
```yaml
option: core
```

- [ ] **Step 7 : Vérifier**

```bash
grep -n "module:\|profiles:" packages/referentiel/classement/mes_ventes.md packages/referentiel/classement/mes_achats.md packages/referentiel/classement/mon_juridique.md packages/referentiel/classement/ma_fiscalite.md packages/referentiel/classement/ma_banque.md packages/referentiel/classement/archives.md
```
Résultat attendu : aucune ligne (grep retourne rien).

- [ ] **Step 8 : Commit**

```bash
git add packages/referentiel/classement/mes_ventes.md packages/referentiel/classement/mes_achats.md packages/referentiel/classement/mon_juridique.md packages/referentiel/classement/ma_fiscalite.md packages/referentiel/classement/ma_banque.md packages/referentiel/classement/archives.md
git commit -m "refactor(referentiel): module → option, suppression profiles (fichiers core)"
```

---

### Task 2 : Frontmatter des fichiers d'options

Mettre à jour les 2 fichiers non-core.

**Files:**
- Modify: `packages/referentiel/classement/mon_social.md` (lignes 2-5)
- Modify: `packages/referentiel/classement/mes_assurances.md` (lignes 2-5)

- [ ] **Step 1 : Éditer `mon_social.md`**

Remplacer dans le frontmatter :
```yaml
module: dirigeant-assimile-salarie
profiles: [sasu-solo, sasu-solo-employe]
required: true
```
par :
```yaml
option: dirigeant-assimile-salarie
required: true
```

- [ ] **Step 2 : Éditer `mes_assurances.md`**

Remplacer dans le frontmatter :
```yaml
module: assurances
profiles: [sasu-solo, sasu-solo-employe, indep-creatif-tech]
required: false
```
par :
```yaml
option: assurances
required: false
```

- [ ] **Step 3 : Vérifier**

```bash
grep -n "module:\|profiles:" packages/referentiel/classement/mon_social.md packages/referentiel/classement/mes_assurances.md
```
Résultat attendu : aucune ligne.

```bash
grep -n "option:" packages/referentiel/classement/mon_social.md packages/referentiel/classement/mes_assurances.md
```
Résultat attendu :
```
packages/referentiel/classement/mon_social.md:2:option: dirigeant-assimile-salarie
packages/referentiel/classement/mes_assurances.md:2:option: assurances
```

- [ ] **Step 4 : Commit**

```bash
git add packages/referentiel/classement/mon_social.md packages/referentiel/classement/mes_assurances.md
git commit -m "refactor(referentiel): module → option, suppression profiles (options)"
```

---

### Task 3 : `classement/__index.md` — section "Modules et profils" → "Options"

**Files:**
- Modify: `packages/referentiel/classement/__index.md` (lignes 65-83)

- [ ] **Step 1 : Remplacer la section entière**

Remplacer le bloc existant :
```markdown
## Modules et profils

Le référentiel est organisé en un **noyau (`core`)** et des **modules optionnels** activés selon le profil.

| Module | Dossier(s) ajouté(s) | Profils concernés |
|--------|---------------------|-------------------|
| `core` | `Mes ventes/`, `Mes achats/`, `Mon juridique/`, `Ma fiscalité/`, `Ma banque/`, `Archives/` | Tous |
| `dirigeant-assimile-salarie` | `Mon social/` | SASU (dirigeant assimilé salarié) |
| `assurances` | `Mes assurances/` | SASU, indép avec RC Pro ou mutuelle |

### Profils prédéfinis

| Profil | Modules activés |
|--------|----------------|
| **Indep solo micro** | `core` |
| **SASU solo sans salarié** | `core` + `dirigeant-assimile-salarie` + `assurances` |
| **SASU solo + salariés** | `core` + `dirigeant-assimile-salarie` + `assurances` |
| **Indep créatif/tech** | `core` + `assurances` |
```

par :
```markdown
## Options

Le référentiel est organisé en un **noyau (`core`)** et des **options** que tu cumules selon ta situation.

| Option | Dossier(s) ajouté(s) | Cas d'usage |
|--------|----------------------|-------------|
| `core` | `Mes ventes/`, `Mes achats/`, `Mon juridique/`, `Ma fiscalité/`, `Ma banque/`, `Archives/` | Tous |
| `dirigeant-assimile-salarie` | `Mon social/` | Dirigeant SASU, assimilé salarié |
| `assurances` | `Mes assurances/` | RC Pro, mutuelle, assurance locaux |
```

- [ ] **Step 2 : Vérifier**

```bash
grep -n "Modules et profils\|Profils prédéfinis\|Profils concernés\|Modules activés" packages/referentiel/classement/__index.md
```
Résultat attendu : aucune ligne.

```bash
grep -n "## Options" packages/referentiel/classement/__index.md
```
Résultat attendu : une ligne avec `## Options`.

- [ ] **Step 3 : Commit**

```bash
git add packages/referentiel/classement/__index.md
git commit -m "refactor(referentiel): modules et profils → options dans plan-classement"
```

---

### Task 4 : `demarrage-rapide.md` et `_index.md`

**Files:**
- Modify: `packages/referentiel/demarrage-rapide.md` (ligne 4 et bloc CLI)
- Modify: `packages/referentiel/_index.md` (ligne 29)

- [ ] **Step 1 : Éditer le chapeau de `demarrage-rapide.md`**

Remplacer :
```markdown
Ce guide présente le cas le plus courant : **SASU solo sans salarié** (profil `sasu-solo`). Modules activés : `core` + `dirigeant-assimile-salarie` + `assurances`.
```
par :
```markdown
Ce guide présente le cas le plus courant : **SASU solo sans salarié**. Options activées : `core` + `dirigeant-assimile-salarie` + `assurances`.
```

- [ ] **Step 2 : Éditer l'exemple CLI dans `demarrage-rapide.md`**

Remplacer :
```bash
npx referentiel-cli init --profile sasu-solo --target /chemin/vers/mon/drive
```
par :
```bash
npx referentiel-cli init --options dirigeant-assimile-salarie,assurances --target /chemin/vers/mon/drive
```

- [ ] **Step 3 : Éditer le sommaire de `_index.md`**

Remplacer :
```markdown
- [Démarrage rapide](demarrage-rapide.md) — Le profil SASU solo, l'arborescence résultante, et les 4 gestes quotidiens.
```
par :
```markdown
- [Démarrage rapide](demarrage-rapide.md) — Les options activées pour une SASU solo, l'arborescence résultante, et les 4 gestes quotidiens.
```

- [ ] **Step 4 : Vérifier**

```bash
grep -n "profil\|--profile\|Modules activés" packages/referentiel/demarrage-rapide.md packages/referentiel/_index.md
```
Résultat attendu : aucune ligne (toutes les occurrences ont été remplacées).

- [ ] **Step 5 : Commit**

```bash
git add packages/referentiel/demarrage-rapide.md packages/referentiel/_index.md
git commit -m "refactor(referentiel): supprimer références aux profils dans demarrage-rapide et index"
```

---

### Task 5 : Vérification finale — cohérence globale

- [ ] **Step 1 : Contrôle résiduel `module:` et `profiles:`**

```bash
grep -rn "module:\|profiles:" packages/referentiel/
```
Résultat attendu : aucune ligne.

- [ ] **Step 2 : Contrôle `option:` présent dans tous les fichiers classement**

```bash
grep -l "option:" packages/referentiel/classement/*.md
```
Résultat attendu : les 8 fichiers `.md` du dossier `classement/` (hors `__index.md`).

- [ ] **Step 3 : Contrôle aucune référence à `--profile` dans toute la doc**

```bash
grep -rn "\-\-profile" packages/referentiel/
```
Résultat attendu : aucune ligne.
