# Referentiel MD Cleanup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Éliminer les doublons dans `packages/referentiel/`, en faire un référentiel pur, et déplacer le contenu CLI vers `packages/referentiel-cli/doc/`.

**Architecture:** Le dossier `classement/` est la source de vérité — tous les `file_naming` par dossier y sont déjà dans les frontmatters et corps des fichiers. `regles-nommage.md` garde uniquement les règles transversales (socle commun, conventions, cas particuliers). Le contenu CLI quitte `referentiel/` vers `referentiel-cli/doc/`.

**Tech Stack:** Markdown, YAML frontmatter — aucune dépendance de code à modifier.

---

## Fichiers concernés

| Fichier | Action |
|---------|--------|
| `packages/referentiel/plan-classement.md` | Supprimer (redirect orphelin vers `classement/__index.md`) |
| `packages/referentiel/regles-nommage.md` | Supprimer la section "Règles par dossier" (lignes 59–177) — déjà dans les fichiers classement |
| `packages/referentiel/demarrage-rapide.md` | Supprimer la section "Initialiser l'arborescence (CLI)" |
| `packages/referentiel-cli/doc/usage.md` | Créer — reçoit la section CLI de `demarrage-rapide.md` |

**Aucun code TypeScript à modifier.** Les fichiers classement (`classement/*.md`) ont déjà tous les `file_naming` nécessaires — aucune addition requise.

---

### Task 1: Supprimer `plan-classement.md`

**Files:**
- Delete: `packages/referentiel/plan-classement.md`

- [ ] **Step 1: Vérifier qu'aucun fichier ne lie vers `plan-classement.md`**

```bash
grep -r "plan-classement" /home/deka/sources/github/archivist-ai/packages/referentiel/ --include="*.md"
grep -r "plan-classement" /home/deka/sources/github/archivist-ai/packages/referentiel-cli/ --include="*.ts"
```

Expected : 0 résultats (le fichier est orphelin — `_index.md` lie directement vers `classement/__index.md`).

- [ ] **Step 2: Supprimer le fichier**

```bash
rm /home/deka/sources/github/archivist-ai/packages/referentiel/plan-classement.md
```

- [ ] **Step 3: Vérifier la suppression**

```bash
ls /home/deka/sources/github/archivist-ai/packages/referentiel/
```

Expected : `plan-classement.md` absent.

- [ ] **Step 4: Commit**

```bash
git add -A packages/referentiel/plan-classement.md
git commit -m "docs(referentiel): remove plan-classement.md redirect"
```

---

### Task 2: Épurer `regles-nommage.md`

**Files:**
- Modify: `packages/referentiel/regles-nommage.md`

Contexte : le fichier contient 3 types de contenu :
1. **Règles transversales** (principe directeur, dossiers de l'arborescence, socle commun, conventions, cas particuliers) — à **garder**
2. **"## Règles par dossier"** (sections `Mes ventes/Mes factures clients/`, `Mon social/`, etc.) — à **supprimer**, ces règles sont déjà dans les fichiers `classement/*.md`

La section à supprimer commence à `## Règles par dossier` (ligne 59) et se termine juste avant `## Conventions d'écriture` (ligne 179).

- [ ] **Step 1: Confirmer les bornes de la section à supprimer**

```bash
grep -n "## Règles par dossier\|## Conventions d'écriture" \
  /home/deka/sources/github/archivist-ai/packages/referentiel/regles-nommage.md
```

Expected : deux lignes indiquant les numéros exacts.

- [ ] **Step 2: Éditer `regles-nommage.md`**

Remplacer le contenu du fichier par la version épurée ci-dessous (supprimer toute la section `## Règles par dossier` et ses sous-sections) :

```markdown
# Règles de nommage

> Partie du [Référentiel de gestion documentaire](./_index.md) — v0

---

## Principe directeur

Un nom de fichier doit répondre à **3 questions sans ouvrir le document** :

1. **Quand ?** — à quelle période ce document se rapporte-t-il ?
2. **Quoi ?** — quel est le type de document ?
3. **Qui / quoi ?** — quel tiers, quel objet ?

Un bon nom de fichier est lisible par un humain ET triable automatiquement dans l'explorateur de fichiers.

---

## Dossiers de l'arborescence

Les **noms de dossiers** (toute l'arborescence de classement) suivent une convention en **français lisible** :


| Règle                  | Détail                                                                                                                    |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **Majuscule initiale** | Première lettre en majuscule, le reste en minuscules                                                                      |
| **Espaces**            | Les mots sont séparés par des espaces                                                                                     |
| **Accents**            | On conserve les accents français (`Ma fiscalité`, pas `Ma fiscalite`)                                                     |
| **Pas de tiret**       | Sauf pour les dossiers **uniquement chronologiques** au format `AAAA-MM` ou `AAAA` (lisibilité et tri dans l'explorateur) |


**Exemples de dossiers :** `Mes ventes/`, `Mes factures clients/`, `Mes modèles de contrat/`, `Factures fournisseurs/`, `Dupont/`, `Archives/`, `2026-03/`.

**Fichiers vs dossiers :** les règles du socle commun ci‑dessous concernent les **fichiers** (nom avec date, type, tiers…). Les dossiers ne reprennent pas ce format — uniquement la convention décrite ici.

---

## Socle commun (fichiers)

Ces 4 règles s'appliquent aux **fichiers** de tous les dossiers, sans exception.


| Règle                   | Détail                                                       |
| ----------------------- | ------------------------------------------------------------ |
| **Date en préfixe**     | Toujours en début de nom, format `AAAA-MM` ou `AAAA`         |
| **Casse**               | Majuscule initiale sur chaque segment, pas d'accents, pas d'espaces |
| **Séparateurs**         | Tiret `-` dans un segment, underscore `_` entre les segments |
| **Extension explicite** | `.pdf`, `.xlsx`, `.jpg` — toujours présente                  |


**Pourquoi ces choix :**

- **Date en préfixe** → l'explorateur trie les fichiers par ordre chronologique automatiquement. Les factures de janvier apparaissent avant celles de mars, sans intervention manuelle.
- **Majuscule initiale par segment, sans accents** → lisibilité immédiate du nom de fichier, tout en garantissant la portabilité entre systèmes (Windows, macOS, Linux, Google Drive, OneDrive, NAS). Pas d'accents pour éviter les problèmes d'encodage à l'échange ou à la sauvegarde.
- **Underscores entre segments** → la distinction visuelle entre les parties du nom est immédiate. `2026-03_Facture_Dupont_F2600003.pdf` se lit en un coup d'œil.

---

## Conventions d'écriture


| Convention                      | Règle                                                                                        | Exemple                             |
| ------------------------------- | -------------------------------------------------------------------------------------------- | ----------------------------------- |
| **Dossiers**                    | Français lisible, voir section [Dossiers de l'arborescence](#dossiers-de-larborescence) | `Mes ventes/Mes factures clients/2026-03/` |
| Casse (fichiers)                | Majuscule initiale sur chaque segment                                                        | `Facture`, `Dupont`, `Declaration`  |
| Mots dans un segment (fichiers) | Séparés par des tirets `-`                                                                   | `mise-en-demeure`, `fiche-paie`     |
| Segments entre eux (fichiers)   | Séparés par des underscores `_`                                                              | `2026-03_Facture_Dupont`            |
| Espaces                         | Jamais                                                                                       | `client-dupont` pas `client dupont` |
| Accents                         | Jamais                                                                                       | `fiscalite` pas `fiscalité`         |
| Abréviations                    | Seulement si universelles                                                                    | `tva`, `rh` — éviter le reste       |


---

## Cas particuliers


| Cas                                | Règle                                                                                            | Exemple                                           |
| ---------------------------------- | ------------------------------------------------------------------------------------------------ | ------------------------------------------------- |
| Pas de tiers                       | Omettre ce segment                                                                               | `2026-01_Declaration-TVA.pdf`                     |
| Pas de date mensuelle              | Date à l'année seule                                                                             | `2025_Statuts_SAS-Monentreprise.pdf`              |
| Plusieurs versions                 | Suffixe `-v2`, `-v3` avant l'extension                                                           | `2026-03_Devis_Dupont_D2600001-v2.pdf`            |
| Scan ou photo d'un document papier | Préfixer le type avec `scan-`                                                                    | `2026-03_scan-facture_fournisseur-brico_001.pdf`  |
| Deux clients sur un même document  | Choisir le client principal, noter l'autre dans les métadonnées ou dans un fichier `.md` associé | `2026-03_Contrat_Dupont_collaboration.pdf`        |
```

- [ ] **Step 3: Vérifier que le fichier ne contient plus la section supprimée**

```bash
grep -n "Règles par dossier\|Mes factures clients\|Mon social\|Ma fiscalité\|Ma banque\|Mon juridique" \
  /home/deka/sources/github/archivist-ai/packages/referentiel/regles-nommage.md
```

Expected : 0 résultats (les anciens titres de sections ne doivent plus apparaître).

- [ ] **Step 4: Vérifier que le contenu essentiel est présent**

```bash
grep -n "Socle commun\|Principe directeur\|Conventions d'écriture\|Cas particuliers" \
  /home/deka/sources/github/archivist-ai/packages/referentiel/regles-nommage.md
```

Expected : 4 lignes correspondant aux 4 sections conservées.

- [ ] **Step 5: Commit**

```bash
git add packages/referentiel/regles-nommage.md
git commit -m "docs(referentiel): remove per-folder naming rules from regles-nommage (already in classement files)"
```

---

### Task 3: Déplacer la section CLI hors de `demarrage-rapide.md`

**Files:**
- Modify: `packages/referentiel/demarrage-rapide.md`
- Create: `packages/referentiel-cli/doc/usage.md`

La section à extraire de `demarrage-rapide.md` :

```markdown
## Initialiser l'arborescence (CLI)

```bash
# Depuis la racine du projet
npx referentiel-cli init --options dirigeant-assimile-salarie,assurances --target /chemin/vers/mon/drive
```

Le CLI crée tous les dossiers correspondant aux options sélectionnées dans le dossier cible.
```

- [ ] **Step 1: Créer `packages/referentiel-cli/doc/usage.md`**

```bash
mkdir -p /home/deka/sources/github/archivist-ai/packages/referentiel-cli/doc
```

Contenu du fichier à créer :

```markdown
# Usage — referentiel-cli

## Initialiser l'arborescence

Crée tous les dossiers du référentiel selon les options choisies dans un dossier cible.

```bash
npx referentiel-cli init --options dirigeant-assimile-salarie,assurances --target /chemin/vers/mon/drive
```

### Options disponibles

| Option | Dossier(s) créé(s) | Cas d'usage |
|--------|--------------------|-------------|
| `core` | `Mes ventes/`, `Mes achats/`, `Mon juridique/`, `Ma fiscalité/`, `Ma banque/`, `Archives/` | Tous |
| `dirigeant-assimile-salarie` | `Mon social/` | Dirigeant SASU, assimilé salarié |
| `assurances` | `Mes assurances/` | RC Pro, mutuelle, assurance locaux |

`core` est toujours activé. Les autres options se cumulent.

### Exemple — SASU solo sans salarié

```bash
npx referentiel-cli init --options dirigeant-assimile-salarie,assurances --target ~/Documents/Mon-drive
```

Crée l'arborescence complète décrite dans le [démarrage rapide](../../referentiel/demarrage-rapide.md).
```

- [ ] **Step 2: Supprimer la section CLI de `demarrage-rapide.md`**

Retirer la section suivante du fichier `demarrage-rapide.md` (et le séparateur `---` qui la précède) :

```markdown
---

## Initialiser l'arborescence (CLI)

```bash
# Depuis la racine du projet
npx referentiel-cli init --options dirigeant-assimile-salarie,assurances --target /chemin/vers/mon/drive
```

Le CLI crée tous les dossiers correspondant aux options sélectionnées dans le dossier cible.
```

- [ ] **Step 3: Vérifier que `demarrage-rapide.md` ne contient plus la section CLI**

```bash
grep -n "CLI\|npx referentiel-cli\|Initialiser" \
  /home/deka/sources/github/archivist-ai/packages/referentiel/demarrage-rapide.md
```

Expected : 0 résultats.

- [ ] **Step 4: Vérifier que `doc/usage.md` est bien créé**

```bash
cat /home/deka/sources/github/archivist-ai/packages/referentiel-cli/doc/usage.md
```

Expected : le fichier s'affiche avec son contenu.

- [ ] **Step 5: Commit**

```bash
git add packages/referentiel/demarrage-rapide.md packages/referentiel-cli/doc/usage.md
git commit -m "docs: move CLI usage section from demarrage-rapide to referentiel-cli/doc/usage.md"
```

---

## Self-Review

### Spec coverage

| Exigence | Tâche couverte |
|----------|---------------|
| Supprimer `plan-classement.md` (redirect orphelin) | Task 1 |
| Pas de répétition dans `regles-nommage.md` | Task 2 |
| Contenu CLI hors de `referentiel/` | Task 3 |
| `referentiel/` ne contient que du référentiel | Tasks 1, 2, 3 |

### Placeholder scan

Aucun TBD, TODO, "implement later" ou "voir plus bas".

### Vérification des fichiers non modifiés

- `_index.md` : aucun lien vers `plan-classement.md`, lien vers `classement/__index.md` déjà correct — **pas de modification nécessaire**
- `regles-archivage.md` : contenu propre, pas de doublon — **pas de modification nécessaire**
- `classement/*.md` : déjà à jour, tous les `file_naming` sont en place — **pas de modification nécessaire**
- `referentiel-reader.ts` : ne lit pas `plan-classement.md`, pas de changement de source → **aucune mise à jour TypeScript nécessaire**
