# Design : transformation profils → options dans le référentiel

Date : 2026-04-09
Statut : approuvé

---

## Contexte

Le référentiel de gestion documentaire est structuré autour d'un noyau (`core`) et de modules optionnels (`dirigeant-assimile-salarie`, `assurances`). Jusqu'ici, des **profils prédéfinis** (`sasu-solo`, `indep-creatif-tech`…) combinaient ces modules et étaient encodés dans le frontmatter des fichiers `.md` (`profiles: [...]`).

Ce design supprime le concept de profil comme mécanisme de configuration du référentiel. Les profils prédéfinis deviennent de simples exemples documentaires. La configuration se fait désormais en choisissant des **options** à cumuler sur le `core`.

---

## Périmètre

| Fichier / composant | Nature du changement |
|---------------------|----------------------|
| `classement/*.md` (7 fichiers) | Frontmatter : `module:` → `option:`, suppression de `profiles:` |
| `classement/__index.md` | Section "Modules et profils" → "Options", suppression du tableau des profils prédéfinis |
| `demarrage-rapide.md` | Exemple CLI `--profile sasu-solo` → `--options dirigeant-assimile-salarie,assurances` |
| `_index.md` | Sommaire : "Le profil SASU solo" → "Les options activées pour une SASU solo" |
| `referentiel-cli/src/cli.ts` | Hors scope (commande `init` inexistante) — référence CLI uniquement dans la doc |

---

## Changements détaillés

### 1. Frontmatter des fichiers `classement/*.md`

**Avant :**
```yaml
module: dirigeant-assimile-salarie
profiles: [sasu-solo, sasu-solo-employe]
required: true
```

**Après :**
```yaml
option: dirigeant-assimile-salarie
required: true
```

- `module:` est renommé `option:`
- `profiles:` est supprimé

**Mapping option par fichier :**

| Fichier | option |
|---------|--------|
| `mes_ventes.md` | `core` |
| `mes_achats.md` | `core` |
| `mon_juridique.md` | `core` |
| `ma_fiscalite.md` | `core` |
| `ma_banque.md` | `core` |
| `archives.md` | `core` |
| `mon_social.md` | `dirigeant-assimile-salarie` |
| `mes_assurances.md` | `assurances` |

### 2. `classement/__index.md` — section "Modules et profils"

Le titre devient **"Options"**. Le tableau est adapté :

| Option | Dossier(s) ajouté(s) | Cas d'usage |
|--------|----------------------|-------------|
| `core` | `Mes ventes/`, `Mes achats/`, `Mon juridique/`, `Ma fiscalité/`, `Ma banque/`, `Archives/` | Tous |
| `dirigeant-assimile-salarie` | `Mon social/` | Dirigeant SASU, assimilé salarié |
| `assurances` | `Mes assurances/` | RC Pro, mutuelle, assurance locaux |

Le tableau "Profils prédéfinis" est supprimé de ce fichier.

### 3. `demarrage-rapide.md`

Le chapeau reste "Modules activés : `core` + `dirigeant-assimile-salarie` + `assurances`" — texte documentaire, pas une clé de config.

L'exemple CLI devient :
```bash
npx referentiel-cli init --options dirigeant-assimile-salarie,assurances --target /chemin/vers/mon/drive
```

### 4. `_index.md`

La ligne du sommaire :
- Avant : "Le profil SASU solo, l'arborescence résultante, et les 4 gestes quotidiens."
- Après : "Les options activées pour une SASU solo, l'arborescence résultante, et les 4 gestes quotidiens."

---

## Ce qui ne change pas

- La structure des dossiers et sous-dossiers dans chaque module
- Les règles de nommage et d'archivage
- Le concept de `core` (toujours inclus, toujours implicite)
- `required: true/false` dans le frontmatter
- `demarrage-rapide.md` peut continuer à documenter des exemples de combinaisons nommées ("SASU solo") — c'est de la doc, pas de la config

---

## Décisions de conception

- **Profils dans la doc, pas dans le référentiel.** Les profils prédéfinis sont des raccourcis pédagogiques utiles, mais ils ne doivent pas figurer dans le frontmatter structurel des fichiers `.md`. Si demain il y a 10 profils, les fichiers ne doivent pas être mis à jour pour chaque nouveau profil.
- **`option:` plutôt que `module:`.** Le terme "module" est technique et ambigu (module npm, module JS…). "Option" exprime mieux le caractère cumulable et facultatif.
- **CLI hors scope immédiat.** La commande `init` n'existe pas encore ; l'adaptation du flag se fera lors de son implémentation.
