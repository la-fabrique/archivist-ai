# Référentiel v0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Write the 5 files of the référentiel v0 in `packages/referentiel/` — a document management guide for TPE/freelances, structured as a practical guide (context → rules → examples → edge cases).

**Architecture:** Each file is a standalone Markdown document. `_index.md` is the entry point with links to the 4 topic files. The tone is accessible but rigorous — this is a spec that will later become public content. All design decisions are documented in `docs/superpowers/specs/2026-04-01-referentiel-v0-design.md`.

**Tech Stack:** Markdown only. No build step.

**Writing conventions:**
- French language throughout
- Tutoiement (informel, accessible)
- Format "guide pratique" : contexte → règles → exemples concrets → cas limites
- Pas de jargon archivistique sans explication
- Chaque règle a un "pourquoi"

---

### Task 1: `_index.md` — Introduction du référentiel

**Files:**
- Modify: `packages/referentiel/_index.md`

- [ ] **Step 1: Write the introduction file**

Content structure:
1. **Titre** : "Référentiel de gestion documentaire — v0"
2. **Accroche** : "Ce référentiel contient les règles qu'un archiviste professionnel appliquerait à tes documents. Elles sont simples, visibles, et adaptées aux TPE et indépendants."
3. **À qui s'adresse ce référentiel** : TPE, freelances, artisans, professions libérales (1-10 personnes, pas de service IT). Quiconque range ses documents "au feeling" et perd du temps à chercher.
4. **Principes fondateurs** (4 piliers) :
   - **Visibilité** — Les règles sont lisibles et compréhensibles, pas une boîte noire
   - **Co-construction** — Élaborées avec des experts et itérées avec les utilisateurs
   - **Simplicité** — Applicables sans formation, sans outil spécial
   - **Compatibilité** — Se branchent sur ton stockage existant (Drive, OneDrive, serveur local)
5. **Sommaire** avec liens relatifs vers :
   - [Plan de classement](plan-classement.md) — L'arborescence de tes dossiers
   - [Règles de nommage](regles-nommage.md) — Comment nommer tes fichiers
   - [Règles d'archivage](regles-archivage.md) — Quoi garder, combien de temps, comment
   - [Raccourcis et liens](raccourcis-liens.md) — Naviguer sans dupliquer
6. **Statut** : "v0 — version de travail. Ce référentiel est en construction et sera enrichi par les retours de la communauté."

- [ ] **Step 2: Commit**

```bash
git add packages/referentiel/_index.md
git commit -m "feat(referentiel): write _index.md introduction"
```

---

### Task 2: `plan-classement.md` — Plan de classement

**Files:**
- Modify: `packages/referentiel/plan-classement.md`

- [ ] **Step 1: Write the plan de classement file**

Content structure:

**Section 1 — Principe directeur**
- Classement par fonction métier/comptable, pas par client ni par date
- Pourquoi : un classement par client explose à 20+ clients. Un classement par date ne dit rien sur la nature du document. Le classement par fonction reste stable même quand l'activité grandit.

**Section 2 — Les 8 dossiers racine**

Tableau avec :

| Dossier | Rôle | Contenu type |
|---------|------|-------------|
| `Mes Ventes/` | Relation commerciale sortante | Factures émises, devis, contrats, offres, suivi client |
| `Mes Achats/` | Dépenses | Factures fournisseurs, assurances |
| `Mon Juridique/` | Entité juridique | Statuts, K-bis, PV d'AG |
| `Mon Social/` | Gestion du personnel | Contrats de travail, fiches de paie |
| `Ma Fiscalité/` | Obligations fiscales | Déclarations, TVA, CFE, avis d'imposition |
| `Ma Banque et Caisse/` | Trésorerie | Relevés bancaires, remises de chèques, journaux de caisse |
| `Ma Gestion Administrative/` | Divers | Courriers, documents administratifs |
| `Archives/` | Années closes | Archives annuelles compressées avec manifest |

Expliquer la logique de nommage : tous les dossiers commencent par `Mon/Ma/Mes` (sauf Archives) pour un sentiment d'appartenance et une cohérence visuelle.

**Section 3 — Sous-structure de `Mes Ventes/`**

```
Mes Ventes/
├── Factures/
│   ├── 2026-01/
│   ├── 2026-02/
│   └── ...
├── Devis/
│   └── ...
├── Contrats/
│   └── ...
├── Offres/
│   └── ...
└── Gestion/
    ├── Client Dupont/   ← raccourcis uniquement
    └── Client Martin/   ← raccourcis uniquement
```

Expliquer :
- Documents dans les dossiers chronologiques par type
- `Gestion/` = vue par client via raccourcis (détail dans raccourcis-liens.md)
- Sous-dossiers mensuels `AAAA-MM` pour éviter 500 fichiers au même niveau

**Section 4 — Sous-structure de `Mes Achats/`**

```
Mes Achats/
├── Factures fournisseurs/
│   ├── 2026/
│   │   ├── 2026-01/
│   │   └── ...
│   └── 2025/
└── Assurances/
    ├── polices/
    └── attestations/
```

Expliquer : niveau "année" en plus car consultation par exercice comptable. Assurances ici car en comptabilité c'est une charge.

**Section 5 — Les autres dossiers racine**

Pour chacun (`Mon Juridique/`, `Mon Social/`, `Ma Fiscalité/`, `Ma Banque et Caisse/`, `Ma Gestion Administrative/`) :
- Pas de sous-dossiers mensuels obligatoires
- Volume faible, consultation par thème
- Exemples de sous-dossiers possibles (ex: `Mon Juridique/` → statuts, K-bis, PV ; `Mon Social/` → contrats-travail, fiches-paie)

**Section 6 — `Archives/`**

Renvoi vers regles-archivage.md pour le détail. Juste montrer la structure :

```
Archives/
└── 2024/
    ├── mes-ventes-2024.zip
    ├── mes-achats-2024.zip
    └── manifest.md
```

**Section 7 — Quand adapter ce plan**

- Multi-société → un dossier racine par entité juridique
- Projets longs (BTP, conseil) → ajouter `Mes Projets/`

- [ ] **Step 2: Commit**

```bash
git add packages/referentiel/plan-classement.md
git commit -m "feat(referentiel): write plan-classement.md"
```

---

### Task 3: `regles-nommage.md` — Règles de nommage

**Files:**
- Modify: `packages/referentiel/regles-nommage.md`

- [ ] **Step 1: Write the règles de nommage file**

Content structure:

**Section 1 — Principe directeur**

Un nom de fichier doit répondre à 3 questions sans ouvrir le document : quand ? quoi ? qui/quoi ?. Lisible par un humain ET triable dans l'explorateur de fichiers.

**Section 2 — Socle commun**

Les 4 règles qui s'appliquent partout :
- Date en préfixe (toujours)
- Tout en minuscules, pas d'accents, pas d'espaces
- Tirets `-` dans un segment, underscores `_` entre segments
- Extension explicite

Expliquer pourquoi :
- Date en préfixe → tri chronologique automatique
- Underscores entre segments → distinction visuelle
- Minuscules sans accents → portabilité (Drive, OneDrive, NAS, tous les OS)

**Section 3 — Règles par dossier**

Chaque dossier définit ses propres segments pertinents. Tableau :

| Dossier | Format | Exemple |
|---------|--------|---------|
| `Mes Ventes/Factures/` | `AAAA-MM_facture_tiers_numero` | `2026-03_facture_client-dupont_003.pdf` |
| `Mes Ventes/Devis/` | `AAAA-MM_devis_tiers_numero` | `2026-03_devis_client-martin_001.pdf` |
| `Mes Ventes/Contrats/` | `AAAA-MM_contrat_tiers_objet` | `2026-03_contrat_client-dupont_maintenance.pdf` |
| `Mes Ventes/Offres/` | `nom-offre_version` | `formation-react_v2.pdf` |
| `Mes Achats/Factures/` | `AAAA-MM_facture_fournisseur_numero` | `2026-03_facture_orange_012.pdf` |
| `Mes Achats/Assurances/` | `AAAA_type_assureur_objet` | `2026_police_axa_rcpro.pdf` |
| `Mon Social/` | `AAAA-MM_type_nom-salarie` | `2026-03_fiche-paie_dupont-jean.pdf` |
| `Ma Fiscalité/` | `AAAA-MM_type_impot` | `2026-01_declaration_tva.pdf` |
| `Ma Banque et Caisse/` | `AAAA-MM_releve_banque` | `2026-03_releve_banque-populaire.pdf` |
| `Mon Juridique/` | `AAAA_type_objet` | `2025_statuts_sas-monentreprise.pdf` |
| `Ma Gestion Administrative/` | `AAAA-MM_type_expediteur_objet` | `2026-03_courrier_urssaf_mise-en-demeure.pdf` |

Pour chaque ligne, ajouter un court paragraphe expliquant pourquoi ce format (ex: les Offres n'ont pas de date mensuelle car elles sont intemporelles, le Juridique n'a souvent qu'une date annuelle, etc.)

**Section 4 — Conventions d'écriture**

- Minuscules uniquement
- Tirets `-` pour séparer les mots dans un segment (`client-dupont`)
- Underscores `_` pour séparer les segments (`facture_client-dupont`)
- Pas d'espaces, pas d'accents, pas de caractères spéciaux
- Pas d'abréviations sauf universellement comprises (`tva`, `rh`)

**Section 5 — Cas particuliers**

| Cas | Règle | Exemple |
|-----|-------|---------|
| Document sans tiers | Omettre le segment tiers | `2026-01_declaration_tva.pdf` |
| Document sans date précise | Année seule `AAAA` | `2025_statuts_sas-monentreprise.pdf` |
| Plusieurs versions | Suffixe `-v2`, `-v3` avant l'extension | `2026-03_devis_client-dupont_001-v2.pdf` |
| Scan ou photo | Préfixer le type avec `scan-` | `2026-03_scan-facture_fournisseur-brico_001.pdf` |

- [ ] **Step 2: Commit**

```bash
git add packages/referentiel/regles-nommage.md
git commit -m "feat(referentiel): write regles-nommage.md"
```

---

### Task 4: `regles-archivage.md` — Règles d'archivage

**Files:**
- Modify: `packages/referentiel/regles-archivage.md`

- [ ] **Step 1: Write the règles d'archivage file**

Content structure:

**Section 1 — Principe directeur**

L'archivage répond à deux besoins : garder l'espace de travail lisible et respecter les obligations légales de conservation. On ne supprime jamais sans prévenir.

**Section 2 — Cycle de vie d'un document**

Schéma :
```
Actif (N et N-1)  →  Archivé (N-2+)  →  Purgeable (après durée légale)
```

Expliquer chaque état :
- Actif : dans l'arborescence courante, accès direct
- Archivé : compressé dans `Archives/AAAA/`, consultable mais hors du quotidien
- Purgeable : durée légale expirée, notification avant suppression

**Section 3 — Durées de conservation légales**

| Type de document | Durée | Base légale |
|-----------------|-------|-------------|
| Factures (émises et reçues) | 10 ans | Code de commerce, art. L123-22 |
| Contrats commerciaux | 5 ans après fin du contrat | Code civil, art. 2224 |
| Documents fiscaux (déclarations, TVA) | 6 ans | Livre des procédures fiscales, art. L102 B |
| Bulletins de paie | 5 ans | Code du travail, art. L3243-4 |
| Documents sociaux (PV d'AG, statuts) | 5 ans après radiation | Code de commerce |
| Relevés bancaires | 5 ans | Code de commerce |
| Polices d'assurance | 2 ans après fin du contrat | Code des assurances, art. L114-1 |
| Documents juridiques (K-bis, statuts) | Durée de vie de l'entreprise + 5 ans | — |

Ajouter un avertissement : ces durées sont des minimums légaux. En cas de doute, conserver plus longtemps. Toujours vérifier avec son expert-comptable.

**Section 4 — Règles par dossier**

| Dossier | Accès direct | Archivage | Purge |
|---------|-------------|-----------|-------|
| `Mes Ventes/` | N et N-1 | N-2 → Archives | 10 ans (factures), 5 ans (contrats) |
| `Mes Achats/` | N et N-1 | N-2 → Archives | 10 ans (factures), 2 ans (assurances échues) |
| `Ma Fiscalité/` | N et N-1 | N-2 → Archives | 6 ans |
| `Mon Social/` | N et N-1 | N-2 → Archives | 5 ans |
| `Ma Banque et Caisse/` | N et N-1 | N-2 → Archives | 5 ans |
| `Mon Juridique/` | Toujours actif | Jamais tant que l'entreprise existe | 5 ans après radiation |
| `Ma Gestion Administrative/` | N et N-1 | N-2 → Archives | Au cas par cas |

**Section 5 — Structure des archives**

```
Archives/
├── 2024/
│   ├── mes-ventes-2024.zip
│   ├── mes-achats-2024.zip
│   ├── ma-fiscalite-2024.zip
│   ├── mon-social-2024.zip
│   ├── ma-banque-et-caisse-2024.zip
│   ├── ma-gestion-administrative-2024.zip
│   └── manifest.md
└── 2023/
    └── ...
```

Détailler le manifest : nombre de documents par catégorie, date de création de l'archive, date de purge la plus proche.

**Section 6 — Règles de sécurité**

- Jamais de suppression automatique — notification à l'utilisateur, action manuelle requise
- Jamais de duplication — un document n'existe qu'à un seul endroit
- Compression avec vérification d'intégrité avant suppression de l'original
- Archivage par année entière, jamais par mois isolé

- [ ] **Step 2: Commit**

```bash
git add packages/referentiel/regles-archivage.md
git commit -m "feat(referentiel): write regles-archivage.md"
```

---

### Task 5: `raccourcis-liens.md` — Raccourcis et liens

**Files:**
- Modify: `packages/referentiel/raccourcis-liens.md`

- [ ] **Step 1: Write the raccourcis et liens file**

Content structure:

**Section 1 — Principe directeur**

Un document ne vit qu'à un seul endroit — son dossier de classement. Quand on a besoin de le retrouver depuis un autre angle (par client, par projet), on crée un raccourci, jamais une copie. Pourquoi : la duplication crée des incohérences.

**Section 2 — Cas d'usage principal : la vue par client**

Expliquer le problème : les documents d'un client sont dispersés (facture dans Factures/, devis dans Devis/, contrat dans Contrats/). Le dossier `Mes Ventes/Gestion/Client Dupont/` rassemble des raccourcis vers tous ces documents.

Montrer :
```
Mes Ventes/Gestion/
├── Client Dupont/
│   ├── → Factures/2026-03/2026-03_facture_client-dupont_001.pdf
│   ├── → Devis/2026-02/2026-02_devis_client-dupont_001.pdf
│   └── → Contrats/2026-01/2026-01_contrat_client-dupont_001.pdf
└── Client Martin/
    └── → ...
```

**Section 3 — Implémentation selon le système**

| Système | Mécanisme | Remarque |
|---------|-----------|----------|
| Windows | Raccourci `.lnk` | Natif dans l'explorateur |
| macOS | Alias | Résiste au déplacement de l'original |
| Linux | Lien symbolique `ln -s` | Natif |
| Google Drive | Raccourci Drive | Clic droit → "Ajouter un raccourci vers Drive" |
| OneDrive / SharePoint | `.url` ou fichier `.md` avec lien | Support limité |

**Section 4 — Règles**

- Un raccourci n'est pas un document — si l'original est archivé, le raccourci devient mort. C'est normal, il faut le nettoyer.
- Pas de raccourci vers un raccourci — toujours pointer vers l'original
- Même nom que l'original (le dossier parent donne le contexte)
- Nettoyage lors de l'archivage annuel — supprimer les raccourcis vers des documents archivés

**Section 5 — Quand créer un raccourci**

| Situation | Raccourci ? |
|-----------|-------------|
| Voir tous les docs d'un client | Oui — dans `Gestion/{Client}/` |
| Accéder vite à un document fréquent | Oui — dossier personnel |
| "Copier" un document dans deux dossiers | Toujours raccourci, jamais copie |
| Document qui concerne deux clients | Un raccourci dans chaque dossier client |

**Section 6 — Limites**

Les raccourcis ne fonctionnent pas de manière uniforme entre systèmes. C'est une limite connue. Quand l'agent IA sera en place, il gérera la création et le nettoyage automatiquement.

- [ ] **Step 2: Commit**

```bash
git add packages/referentiel/raccourcis-liens.md
git commit -m "feat(referentiel): write raccourcis-liens.md"
```

---

### Task 6: Commit final et mise à jour du design doc

**Files:**
- Modify: `docs/plans/2026-03-09-positionnement-discovery-design.md`

- [ ] **Step 1: Marquer l'étape 2 comme terminée dans le design doc**

Dans la section "Prochaines étapes", marquer l'étape 2 comme faite (par exemple avec un ~~strikethrough~~ ou une checkbox cochée).

- [ ] **Step 2: Commit**

```bash
git add docs/plans/2026-03-09-positionnement-discovery-design.md
git commit -m "docs: mark referentiel v0 step as complete"
```
