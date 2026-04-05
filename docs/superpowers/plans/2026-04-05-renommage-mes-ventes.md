# Renommage Mes ventes — Plan d'implémentation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Renommer et restructurer les dossiers de `Mes ventes/` dans le référentiel : `Factures/` → `Mes factures clients/`, `Contrats modèles/` → `Mes modèles de contrat/`, ajouter `Mes modèles de devis/`, déplacer `Devis/` dans chaque client comme sous-dossier imposé.

**Architecture:** Modifications documentaires sur 7 fichiers markdown du référentiel + 1 fichier test CLI. Pas de changement de code applicatif — uniquement du contenu textuel et des noms de dossiers dans la documentation.

**Tech Stack:** Markdown, TypeScript (tests Vitest)

---

## Fichiers impactés

| Fichier | Action |
|---------|--------|
| `packages/referentiel/classement/mes_ventes.md` | Modification majeure — arbre, sections, descriptions |
| `packages/referentiel/regles-nommage.md` | Renommer les chemins de dossier dans les sections "Règles par dossier" et exemples |
| `packages/referentiel/regles-archivage.md` | Aucun changement nécessaire — les références sont à `Mes ventes/` (inchangé) et `mes_ventes_2024.zip` (inchangé) |
| `packages/referentiel/raccourcis-liens.md` | Renommer les chemins `factures/` → `mes_factures_clients/` et adapter la vue client (les devis sont maintenant dans le client) |
| `packages/referentiel/classement/__index.md` | Mettre à jour la colonne "Contenu type" et la ligne d'adaptation "sans devis" |
| `packages/referentiel/classement/mes_achats.md` | Mettre à jour la référence `Mes ventes/` (ligne 22) — les mois suffisent → adapter le texte au nouveau nom |
| `packages/referentiel-cli/test/walk-referentiel.test.ts` | Pas de changement nécessaire — le test utilise `Mes ventes` comme nom de dossier générique, qui reste valide |

---

### Task 1 : Réécrire `mes_ventes.md` — arbre et introduction

**Files:**
- Modify: `packages/referentiel/classement/mes_ventes.md:1-36`

- [ ] **Step 1 : Remplacer l'arbre et l'introduction**

Remplacer les lignes 1 à 36 par :

```markdown
# `Mes ventes/`

> [Plan de classement](__index.md) — [Référentiel](../_index.md) — v0

Relation commerciale sortante : factures clients, modèles de contrat et de devis, offres, suivi client.


```
Mes ventes/
├── Mes factures clients/
│   ├── 2026-01/
│   └── ...
├── Mes modèles de contrat/
│   └── ...
├── Mes modèles de devis/
│   └── ...
├── Mes offres/
│   ├── formation_react/
│   └── audit_seo/
└── Mes clients/
    ├── Client Dupont/
    │   ├── Contrats/
    │   ├── Devis/
    │   └── ...     ← notes, CR, suivi libre
    └── Client Martin/
        ├── Contrats/
        ├── Devis/
        └── ...     ← notes, CR, suivi libre
```

**Ce qu'il faut retenir :**

- `Mes factures clients/` contient les factures **émises**, classées dans des **sous-dossiers chronologiques** par mois (`Mes factures clients/2026-03/`). C'est l'emplacement de référence — pratique pour un export groupé (ex. envoi au comptable).
- `Mes modèles de contrat/` et `Mes modèles de devis/` regroupent les **gabarits réutilisables** à dupliquer et adapter. Pas de documents signés ni finalisés ici — uniquement des modèles types.
- `Mes clients/` offre une **vue par client** : chaque sous-dossier contient les contrats et devis réels du client ainsi que les documents de suivi (notes, CR…). `Contrats/` et `Devis/` sont imposés ; le reste de l'organisation est libre par client.
- `Mes offres/` contient un dossier par offre ou service — ces documents sont intemporels, pas liés à un mois.
```

- [ ] **Step 2 : Vérifier le rendu**

Relire le fichier pour s'assurer que le markdown est bien formé (pas de triple backtick en conflit, indentation correcte de l'arbre).

- [ ] **Step 3 : Commit**

```bash
git add packages/referentiel/classement/mes_ventes.md
git commit -m "docs(referentiel): rewrite mes_ventes tree and introduction

Rename Factures → Mes factures clients, Contrats modèles → Mes modèles de contrat,
add Mes modèles de devis, move Devis into client subfolders."
```

---

### Task 2 : Réécrire `mes_ventes.md` — section Factures

**Files:**
- Modify: `packages/referentiel/classement/mes_ventes.md:39-49` (anciens numéros)

- [ ] **Step 1 : Renommer la section `Factures/` → `Mes factures clients/`**

Remplacer la section `## \`Factures/\`` (lignes 39-49) par :

```markdown
## `Mes factures clients/`

**Rôle :** factures **émises** par ton entreprise (pas les brouillons : une fois validée et envoyée, le PDF ou l'export comptable vit ici).

**Organisation :** un sous-dossier par mois d'émission utile, format `AAAA-MM` (`Mes factures clients/2026-03/`).

**Format des fichiers:** `AAAA-MM_facture_tiers_numero.ext`

**Exemple :** `2026-03_facture_client-dupont_003.pdf`

Le numéro séquentiel (`001`, `002`…) différencie plusieurs factures au même client le même mois. Il correspond idéalement au numéro de facture de ta comptabilité.
```

- [ ] **Step 2 : Commit**

```bash
git add packages/referentiel/classement/mes_ventes.md
git commit -m "docs(referentiel): rename Factures section to Mes factures clients"
```

---

### Task 3 : Réécrire `mes_ventes.md` — supprimer section Devis du premier niveau

**Files:**
- Modify: `packages/referentiel/classement/mes_ventes.md` (ancienne section Devis lignes 53-63)

- [ ] **Step 1 : Supprimer la section `## \`Devis/\``**

Supprimer entièrement la section `## \`Devis/\`` et le séparateur `---` qui la précède (ancien contenu lignes 51-65). Cette section sera remplacée par une sous-section dans `Mes clients/` (Task 5).

- [ ] **Step 2 : Commit**

```bash
git add packages/referentiel/classement/mes_ventes.md
git commit -m "docs(referentiel): remove top-level Devis section (moved to client)"
```

---

### Task 4 : Réécrire `mes_ventes.md` — section Contrats modèles → Mes modèles de contrat + ajouter Mes modèles de devis

**Files:**
- Modify: `packages/referentiel/classement/mes_ventes.md` (ancienne section Contrats modèles lignes 67-77)

- [ ] **Step 1 : Remplacer la section `Contrats modèles/` et ajouter `Mes modèles de devis/`**

Remplacer la section `## \`Contrats modèles/\`` par :

```markdown
## `Mes modèles de contrat/`

**Rôle :** **modèles** de contrat ou d'avenant à dupliquer, compléter puis adapter pour chaque client. Pas de document signé ni de PDF « définitif client » dans ce dossier — uniquement les gabarits réutilisables (`.docx`, `.odt`, parfois PDF guide).

**Quand tu sors un contrat pour un client** (fichier adapté, puis signé ou archivé comme référence client), enregistre-le dans `Mes clients/[client]/Contrats/` — pas dans `Mes modèles de contrat/`. Voir la section **`Mes clients/`** pour le nommage des fichiers contrat.

**Format des fichiers:** `modele-contrat_objet_vN.ext`

**Exemple :** `modele-contrat_maintenance_annuelle_v2.docx`

Pas de date « client » dans le nom : ce sont des gabarits réutilisables. Le segment **objet** décrit le type de modèle (souvent plusieurs mots liés par des underscores ou des tirets, ex. `maintenance_annuelle`). **vN** est la version du gabarit (`v1`, `v2`…), pas une version « client ».

---

## `Mes modèles de devis/`

**Rôle :** **modèles** de devis à dupliquer, compléter puis adapter pour chaque client. Pas de devis finalisé ni envoyé dans ce dossier — uniquement les gabarits réutilisables (`.docx`, `.odt`, parfois PDF guide).

**Quand tu finalises un devis pour un client** (fichier adapté et envoyé), enregistre-le dans `Mes clients/[client]/Devis/` — pas dans `Mes modèles de devis/`. Voir la section **`Mes clients/`** pour le nommage des fichiers devis.

**Format des fichiers:** `modele-devis_objet_vN.ext`

**Exemple :** `modele-devis_prestation_conseil_v1.docx`

Même logique que les modèles de contrat : pas de date client, version du gabarit uniquement.
```

- [ ] **Step 2 : Commit**

```bash
git add packages/referentiel/classement/mes_ventes.md
git commit -m "docs(referentiel): rename Contrats modèles → Mes modèles de contrat, add Mes modèles de devis"
```

---

### Task 5 : Réécrire `mes_ventes.md` — section Mes clients (ajouter Devis comme sous-dossier imposé)

**Files:**
- Modify: `packages/referentiel/classement/mes_ventes.md` (section Mes clients, anciennement lignes 93-117)

- [ ] **Step 1 : Réécrire la section `Mes clients/`**

Remplacer toute la section `## \`Mes clients/\`` par :

```markdown
## `Mes clients/`

**Rôle :** **vue par client** regroupant les documents directement liés à la relation avec un client : contrats signés, devis envoyés, notes de suivi, comptes-rendus, échanges de référence. Chaque client dispose de son propre sous-dossier.

**Organisation :** un sous-dossier par client, nom en français lisible (`Client Dupont/`). Les sous-dossiers `Contrats/` et `Devis/` sont imposés dans chaque client ; le reste de l'organisation est libre.

```
Mes clients/
└── Client Dupont/
    ├── Contrats/    ← contrats et avenants réels du client
    ├── Devis/       ← devis envoyés au client
    └── ...          ← notes, CR, suivi (libre)
```

### `Contrats/` (dans chaque client)

**Rôle :** tout **contrat ou avenant** une fois sorti du statut « simple brouillon générique » : négociation, versions partagées, **PDF signé**, scans. Structure plate — pas de sous-dossiers mensuels, le volume par client reste faible.

**Format des fichiers:** `AAAA-MM-JJ_tiers_contrat_CAAAA-XX.ext` ou `AAAA-MM-JJ_tiers_avenant_CAAAA-XX.ext`

**Exemple :** `2026-04-03_societe-acme_contrat_C2026-01.pdf` (avenant : `2026-04-03_societe-acme_avenant_C2026-02.pdf`)

`AAAA-MM-JJ` est en général la **date de signature**. Le **tiers** est le client en minuscules, sans accents ni espaces, mots liés par des tirets (`societe-acme`). **`CAAAA-XX`** est une référence maison : `C` + année de numérotation + numéro d'ordre sur deux chiffres (`C2026-01`, …).

**Alternative :** `AAAA-MM_contrat_tiers_objet.ext` — ex. `2026-03_contrat_client-dupont_maintenance.pdf` — si tu préfères un **objet** lisible à la place du code `CAAAA-XX`. Ne pas mélanger les deux conventions sans les documenter.

### `Devis/` (dans chaque client)

**Rôle :** propositions chiffrées envoyées au client (devis, propositions commerciales assimilées), y compris les versions révisées tant qu'elles restent des **devis** (pas encore une facture). Structure plate — pas de sous-dossiers mensuels, le volume par client reste faible.

**Format des fichiers:** `AAAA-MM-JJ_tiers_devis_numero.ext`

**Exemple :** `2026-03-15_client-martin_devis_001.pdf`

Même logique que les contrats : date de référence, tiers normalisé, numéro d'ordre. Pour une révision du **même** devis, ajoute un suffixe `-v2`, `-v3` avant l'extension (ex. `2026-03-15_client-martin_devis_001-v2.pdf`) sans changer le numéro de base.
```

- [ ] **Step 2 : Commit**

```bash
git add packages/referentiel/classement/mes_ventes.md
git commit -m "docs(referentiel): add Devis as imposed subfolder in Mes clients"
```

---

### Task 6 : Mettre à jour `regles-nommage.md`

**Files:**
- Modify: `packages/referentiel/regles-nommage.md:32,63-122,201`

- [ ] **Step 1 : Mettre à jour les exemples de dossiers (ligne 32)**

Remplacer :
```
**Exemples de dossiers :** `Mes ventes/`, `Factures/`, `Modèles/`, `Factures fournisseurs/`, `Client dupont/`, `Archives/`, `2026-03/`.
```
Par :
```
**Exemples de dossiers :** `Mes ventes/`, `Mes factures clients/`, `Mes modèles de contrat/`, `Factures fournisseurs/`, `Client dupont/`, `Archives/`, `2026-03/`.
```

- [ ] **Step 2 : Renommer la section `Mes ventes/factures/` → `Mes ventes/mes_factures_clients/` (ligne 63)**

Remplacer :
```markdown
### `Mes ventes/factures/`
```
Par :
```markdown
### `Mes ventes/mes_factures_clients/`
```

- [ ] **Step 3 : Remplacer la section `Mes ventes/devis/` (lignes 73-79) par `Mes ventes/mes_modeles_de_devis/`**

Remplacer :
```markdown
### `Mes ventes/devis/`

**Format :** `AAAA-MM_devis_tiers_numero.ext`

**Exemple :** `2026-03_devis_client-martin_001.pdf`

Même logique que les factures. Si un devis est révisé, utilise le suffixe de version : `2026-03_devis_client-martin_001-v2.pdf`.
```
Par :
```markdown
### `Mes ventes/mes_modeles_de_devis/`

**Rôle :** gabarits de devis à dupliquer et adapter — pas les devis envoyés aux clients (voir `Mes ventes/mes_clients/[client]/devis/`).

**Format :** `modele-devis_objet_vN.ext`

**Exemple :** `modele-devis_prestation_conseil_v1.docx`

Même logique que les modèles de contrat : pas de date client, version du gabarit uniquement.
```

- [ ] **Step 4 : Renommer la section `Mes ventes/contrats_modeles/` (ligne 83)**

Remplacer :
```markdown
### `Mes ventes/contrats_modeles/`

**Rôle :** gabarits à dupliquer et adapter — pas les contrats signés clients (voir `Mes ventes/contrats/`).
```
Par :
```markdown
### `Mes ventes/mes_modeles_de_contrat/`

**Rôle :** gabarits à dupliquer et adapter — pas les contrats signés clients (voir `Mes ventes/mes_clients/[client]/contrats/`).
```

- [ ] **Step 5 : Renommer la section `Mes ventes/contrats/` (ligne 95) → `Mes ventes/mes_clients/[client]/contrats/`**

Remplacer :
```markdown
### `Mes ventes/contrats/`
```
Par :
```markdown
### `Mes ventes/mes_clients/[client]/contrats/`
```

- [ ] **Step 6 : Ajouter une section pour les devis client après la section contrats client**

Après la section `Mes ventes/mes_clients/[client]/contrats/` (après ligne 113), insérer :

```markdown
---

### `Mes ventes/mes_clients/[client]/devis/`

**Format :** `AAAA-MM-JJ_tiers_devis_numero.ext`

**Exemple :** `2026-03-15_client-martin_devis_001.pdf`

Même logique que les contrats client. Pour une révision du même devis, ajoute un suffixe `-v2`, `-v3` avant l'extension.
```

- [ ] **Step 7 : Renommer la section `Mes ventes/offres/` (ligne 116)**

Remplacer :
```markdown
### `Mes ventes/offres/`
```
Par :
```markdown
### `Mes ventes/mes_offres/`
```

- [ ] **Step 8 : Mettre à jour l'exemple dans le tableau des conventions (ligne 201)**

Remplacer :
```
| **Dossiers**                    | Français lisible, voir section [Dossiers de l'arborescence](#dossiers-de-larborescence) | `Mes ventes/factures/2026-03/`      |
```
Par :
```
| **Dossiers**                    | Français lisible, voir section [Dossiers de l'arborescence](#dossiers-de-larborescence) | `Mes ventes/Mes factures clients/2026-03/` |
```

- [ ] **Step 9 : Commit**

```bash
git add packages/referentiel/regles-nommage.md
git commit -m "docs(referentiel): update regles-nommage for mes_ventes renames"
```

---

### Task 7 : Mettre à jour `raccourcis-liens.md`

**Files:**
- Modify: `packages/referentiel/raccourcis-liens.md:20-38,74`

- [ ] **Step 1 : Réécrire le cas d'usage principal (lignes 19-38)**

Le concept change : les devis et contrats sont maintenant dans le dossier client directement, pas dans des dossiers chronologiques de premier niveau. Le cas d'usage des raccourcis concerne surtout les **factures** (qui restent dans un dossier chronologique de premier niveau).

Remplacer les lignes 19-38 par :

```markdown
## Cas d'usage principal : la vue par client

Le problème : les factures d'un client sont dans un dossier chronologique séparé de son dossier client.

- Sa facture est dans `Mes ventes/Mes factures clients/2026-03/`
- Son contrat et ses devis sont dans `Mes ventes/Mes clients/Client dupont/`

C'est logique pour le classement global, mais difficile quand tu veux voir **toutes les factures de ce client** depuis son dossier.

La solution : le dossier `Mes ventes/Mes clients/Client dupont/` contient des raccourcis vers les factures du client.

```
Mes ventes/Mes clients/
├── Client dupont/
│   ├── Contrats/
│   ├── Devis/
│   ├── → Mes factures clients/2026-03/2026-03_facture_client-dupont_001.pdf
│   └── → Mes factures clients/2026-02/2026-02_facture_client-dupont_002.pdf
└── Client martin/
    ├── Contrats/
    ├── Devis/
    └── → Mes factures clients/2026-02/2026-02_facture_client-martin_001.pdf
```

Tu vois l'ensemble du dossier client en un coup d'œil, sans avoir dupliqué un seul fichier.
```

- [ ] **Step 2 : Mettre à jour le tableau "Quand créer un raccourci" (ligne 74)**

Remplacer :
```
| Voir tous les documents d'un client | Raccourci dans `Mes ventes/gestion/{nom_client}/` |
```
Par :
```
| Voir les factures d'un client depuis son dossier | Raccourci dans `Mes ventes/Mes clients/{nom_client}/` |
```

- [ ] **Step 3 : Commit**

```bash
git add packages/referentiel/raccourcis-liens.md
git commit -m "docs(referentiel): update raccourcis-liens for new mes_ventes structure"
```

---

### Task 8 : Mettre à jour `classement/__index.md`

**Files:**
- Modify: `packages/referentiel/classement/__index.md:26,60`

- [ ] **Step 1 : Mettre à jour la ligne Mes ventes dans le tableau (ligne 26)**

Remplacer :
```
| `[Mes ventes/](mes_ventes.md)`                               | Relation commerciale sortante | Factures émises, devis, contrats clients, offres, suivi client |
```
Par :
```
| `[Mes ventes/](mes_ventes.md)`                               | Relation commerciale sortante | Factures clients, modèles de contrat et de devis, offres, suivi client |
```

- [ ] **Step 2 : Mettre à jour la ligne d'adaptation "sans devis" (ligne 60)**

Remplacer :
```
| Activité sans devis formels          | Simplifier `Mes ventes/` en retirant `devis/`                                           |
```
Par :
```
| Activité sans devis formels          | Simplifier `Mes ventes/` en retirant `Mes modèles de devis/` et `Devis/` des clients    |
```

- [ ] **Step 3 : Commit**

```bash
git add packages/referentiel/classement/__index.md
git commit -m "docs(referentiel): update __index.md for mes_ventes renames"
```

---

### Task 9 : Mettre à jour `mes_achats.md`

**Files:**
- Modify: `packages/referentiel/classement/mes_achats.md:22`

- [ ] **Step 1 : Mettre à jour la référence (ligne 22)**

Remplacer :
```
**Pourquoi un niveau "année" en plus ?** Les factures fournisseurs sont souvent consultées par exercice comptable. Ton comptable te demande "les achats 2025" — le dossier `2025/` répond directement. Pour `Mes ventes/`, les mois sont suffisants car les factures émises sont consultées individuellement.
```
Par :
```
**Pourquoi un niveau "année" en plus ?** Les factures fournisseurs sont souvent consultées par exercice comptable. Ton comptable te demande "les achats 2025" — le dossier `2025/` répond directement. Pour `Mes ventes/Mes factures clients/`, les mois sont suffisants car les factures émises sont consultées individuellement.
```

- [ ] **Step 2 : Commit**

```bash
git add packages/referentiel/classement/mes_achats.md
git commit -m "docs(referentiel): update mes_achats reference to Mes factures clients"
```

---

### Task 10 : Vérifier la CLI — build et tests

**Files:**
- Read: `packages/referentiel-cli/test/walk-referentiel.test.ts`

- [ ] **Step 1 : Vérifier que le test CLI ne dépend pas des noms renommés**

Le test `walk-referentiel.test.ts` utilise `"Mes ventes"` comme nom de dossier de test — ce nom n'a pas changé (le dossier racine reste `Mes ventes/`). **Aucune modification nécessaire.**

- [ ] **Step 2 : Lancer le build CLI**

```bash
cd packages/referentiel-cli && npm run build
```

Expected: Build succeeds without errors.

- [ ] **Step 3 : Lancer les tests CLI**

```bash
cd packages/referentiel-cli && npm test
```

Expected: All tests pass.

- [ ] **Step 4 : Commit final si des corrections ont été nécessaires**

Si le build ou les tests échouent et nécessitent des corrections, commiter les fixes :

```bash
git add -A
git commit -m "fix(referentiel-cli): adjust CLI for mes_ventes renames"
```

---

### Task 11 : Relecture finale complète

- [ ] **Step 1 : Grep de validation — vérifier qu'il ne reste aucune ancienne référence**

```bash
cd packages/referentiel && grep -rn "Factures/" --include="*.md" .
cd packages/referentiel && grep -rn "Contrats modèles" --include="*.md" .
cd packages/referentiel && grep -rn "contrats_modeles" --include="*.md" .
```

Les seules occurrences de `Factures/` tolérées sont `Mes factures clients/` et `Factures fournisseurs/` (dans `mes_achats.md`).
Aucune occurrence de `Contrats modèles` ou `contrats_modeles` ne doit rester.

- [ ] **Step 2 : Vérifier qu'aucune section `## \`Devis/\`` n'existe au premier niveau**

```bash
cd packages/referentiel && grep -rn '## `Devis/' --include="*.md" .
```

Expected: aucun résultat (la section a été supprimée et remplacée par la sous-section dans `Mes clients/`).

- [ ] **Step 3 : Corriger les éventuels résidus**

Si des occurrences sont trouvées, les corriger et commiter.
