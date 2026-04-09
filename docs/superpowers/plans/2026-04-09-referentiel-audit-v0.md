# Référentiel Audit v0 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement all P0/P1/P2 fixes identified in the audit `docs/audit/2026-04-09-audit.md` on the `packages/referentiel/` documentation package.

**Architecture:** Pure documentation changes (Markdown files). No CLI code changes required — the CLI reads files generically and is not sensitive to content or file renames. Changes follow priority order: P0 (critical) → P1 → P2.

**Tech Stack:** Markdown, YAML frontmatter. Test verification: `npm test` in `packages/referentiel-cli/` after each task to confirm no regressions.

---

## File Map

Files modified:
- `packages/referentiel/regles-nommage.md` — Tasks 1, 8, 9
- `packages/referentiel/classement/mon_social.md` — Tasks 2, 3
- `packages/referentiel/classement/mon_juridique.md` — Tasks 2, 7
- `packages/referentiel/classement/ma_banque_et_caisse.md` → renamed `ma_banque.md` — Task 8
- `packages/referentiel/classement/mes_ventes.md` — Tasks 9, 10
- `packages/referentiel/classement/__index.md` — Tasks 4, 8, 10
- `packages/referentiel/_index.md` — Tasks 4, 5
- `packages/referentiel/regles-archivage.md` — Tasks 5, 8

Files created:
- `packages/referentiel/classement/mes_assurances.md` — Task 4

Files deleted:
- `packages/referentiel/raccourcis-liens.md` — Task 5

---

## Task 1 — Fix naming inconsistencies in `regles-nommage.md` (P0)

**Context:** The audit (§3.1–3.3) identified that examples in `regles-nommage.md` violate the socle commun they describe. Fixes: lowercase → Majuscule initiale, underscores within segments → tirets, align with classement files.

**Files:**
- Modify: `packages/referentiel/regles-nommage.md`

- [ ] **Step 1: Fix section `Mon social/`**

Current (lines ~166–172):
```markdown
### `Mon social/`

**Format :** `AAAA-MM_type_nom-salarie.ext`

**Exemple :** `2026-03_fiche-paie_dupont-jean.pdf`

Le nom du salarié en dernier : dans ce dossier, tous les documents concernent du personnel. Le type en premier (`fiche-paie`, `contrat-travail`, `dpae`, `avenant`) facilite le tri.
```

Replace with:
```markdown
### `Mon social/`

**Format :** `[AAAA-MM]_[Type]_[Nom-salarie].[ext]`

**Exemple :** `2026-03_Fiche-de-paie_Dupont.pdf`

Le nom du salarié en dernier : dans ce dossier, tous les documents concernent du personnel. Le type en premier (`Fiche-de-paie`, `Contrat-travail`, `DPAE`, `Avenant`) facilite le tri.
```

- [ ] **Step 2: Fix section `Ma fiscalité/`**

Current (lines ~175–181):
```markdown
### `Ma fiscalité/`

**Format :** `AAAA-MM_type_impot.ext`

**Exemple :** `2026-01_declaration_tva.pdf` / `2026_avis_cfe.pdf`

Pas de numéro séquentiel : il y a rarement deux déclarations TVA le même mois. La date peut être à l'année (`AAAA`) pour les impôts annuels (CFE, liasse fiscale).
```

Replace with:
```markdown
### `Ma fiscalité/`

**Format :** `[AAAA-MM]_[Type].[ext]`

**Exemple :** `2026-01_Declaration-TVA.pdf` / `2026_Avis-CFE.pdf`

Pas de numéro séquentiel : il y a rarement deux déclarations TVA le même mois. La date peut être à l'année (`AAAA`) pour les impôts annuels (CFE, liasse fiscale).
```

- [ ] **Step 3: Fix section `Ma banque et caisse/`**

Current (lines ~184–191):
```markdown
### `Ma banque et caisse/`

**Format :** `AAAA-MM_releve_banque.ext`

**Exemple :** `2026-03_releve_banque-populaire.pdf`

Si tu as plusieurs comptes, le nom de la banque les différencie. Pour les remises de chèques : `2026-03_remise-cheques_banque-populaire_001.pdf` (nom de fichier inchangé ; le dossier parent éventuel suit la convention dossiers, ex. `Remises chèques/`).
```

Replace with:
```markdown
### `Ma banque/`

**Format :** `[AAAA-MM]_Releve_[Nom-banque]_[Numero].[ext]`

**Exemple :** `2026-03_Releve_Banque-Populaire_003.pdf`

Le sous-dossier `[Nom banque]/` permet de distinguer plusieurs établissements. Le numéro de relevé (tel qu'il apparaît sur le document) permet de trier les relevés d'un même compte.
```

- [ ] **Step 4: Fix section `Mon juridique/`**

Current (lines ~194–201):
```markdown
### `Mon juridique/`

**Format :** `AAAA_type_objet.ext`

**Exemple :** `2025_statuts_sas-monentreprise.pdf` / `2024_pv-ag_approbation-comptes.pdf`

Date à l'année — les documents juridiques ne se rapportent généralement pas à un mois précis. L'objet décrit le contenu (`approbation-comptes`, `nomination-gerant`, `modification-statuts`).
```

Replace with:
```markdown
### `Mon juridique/`

**Format :** `[AAAA]_[Type]_[Objet].[ext]`

**Exemple :** `2025_Statuts_SAS-Monentreprise.pdf` / `2024_PV-AG_approbation-comptes.pdf`

Date à l'année — les documents juridiques ne se rapportent généralement pas à un mois précis. L'objet décrit le contenu (`approbation-comptes`, `nomination-gerant`, `modification-statuts`).
```

- [ ] **Step 5: Fix underscore-in-segment in model contract examples**

Find all occurrences of `modele-contrat_maintenance_annuelle` in `regles-nommage.md` and replace with `modele-contrat_maintenance-annuelle` (tiret within segment, not underscore).

Affected lines (examples in sections `Mes modèles de contrat/` and conventions table):
- `modele-contrat_maintenance_annuelle_v2.docx` → `modele-contrat_maintenance-annuelle_v2.docx`

- [ ] **Step 6: Verify all examples in `regles-nommage.md` against socle commun**

Manually scan for any remaining violations:
- No lowercase-only segments (each segment must have Majuscule initiale, except model-file prefixes like `modele-contrat` which have no date)
- No accents in file names
- No underscores within a segment
- No spaces

- [ ] **Step 7: Run CLI tests**

```bash
cd packages/referentiel-cli && npm test
```

Expected: all tests pass.

- [ ] **Step 8: Commit**

```bash
git add packages/referentiel/regles-nommage.md
git commit -m "fix(referentiel): align regles-nommage.md examples with socle commun"
```

---

## Task 2 — Fix inconsistencies in classement files (P0)

**Context:** `mon_social.md` has an accent in a file name example (§3.3). `mon_juridique.md` uses `[AAAA-MM]` but `regles-nommage.md` says `[AAAA]` for juridique (§3.2).

**Files:**
- Modify: `packages/referentiel/classement/mon_social.md`
- Modify: `packages/referentiel/classement/mon_juridique.md`

- [ ] **Step 1: Fix accent in `mon_social.md`**

Find in `mon_social.md` (line ~102):
```
**Exemple :** `2026-01_Contrat_Dupont_CDI.pdf` (avenant : `2026-06_Avenant_Dupont_télétravail.pdf`)
```

Replace with:
```
**Exemple :** `2026-01_Contrat_Dupont_CDI.pdf` (avenant : `2026-06_Avenant_Dupont_teletravail.pdf`)
```

- [ ] **Step 2: Align `mon_juridique.md` to year-only dates**

In `mon_juridique.md`, change all `[AAAA-MM]` to `[AAAA]` and update examples accordingly.

Replace in section `Mes statuts/`:
- Format: `[AAAA-MM]_Statuts_[Objet].[ext]` → `[AAAA]_Statuts_[Objet].[ext]`
- Bullet: `[AAAA-MM]` description → `[AAAA]` — année de signature ou d'enregistrement
- Example: `2026-01_Statuts_constitution.pdf` → `2026_Statuts_constitution.pdf`

Replace in section `Mes K-bis/`:
- Format: `[AAAA-MM]_Kbis.[ext]` → `[AAAA]_Kbis.[ext]`
- Bullet: `[AAAA-MM]` description → `[AAAA]` — année d'émission du K-bis
- Example: `2026-03_Kbis.pdf` → `2026_Kbis.pdf`

Replace in section `Mes PV d'assemblée/`:
- Format: `[AAAA-MM]_PV-AG_[Objet].[ext]` → `[AAAA]_PV-AG_[Objet].[ext]`
- Bullet: `[AAAA-MM]` description → `[AAAA]` — année de l'assemblée
- Example: `2026-04_PV-AG_approbation-comptes.pdf` → `2026_PV-AG_approbation-comptes.pdf`

- [ ] **Step 3: Run CLI tests**

```bash
cd packages/referentiel-cli && npm test
```

Expected: all tests pass.

- [ ] **Step 4: Commit**

```bash
git add packages/referentiel/classement/mon_social.md packages/referentiel/classement/mon_juridique.md
git commit -m "fix(referentiel): remove accent in mon_social example, align juridique to year-only dates"
```

---

## Task 3 — Add URSSAF/DSN/attestations to `mon_social.md` (P0)

**Context:** The audit (§1.1) found no place for URSSAF declarations (DSN), contribution bordereaux, or URSSAF vigilance certificates — all mandatory documents for a SASU dirigeant.

**Files:**
- Modify: `packages/referentiel/classement/mon_social.md`

- [ ] **Step 1: Update tree in `mon_social.md`**

Replace the existing tree block:
```
Mon social/
├── Mes fiches de paie/
│   ├── [AAAA-MM]/
│   └── ...
├── Mes DPAE/
│   └── ...
├── Mes modèles de contrat de travail/
│   └── ...
└── Mes salariés/
    └── [Nom du salarié]/
        ├── Contrats/
        └── ...     ← avenants, courriers, suivi libre
```

With:
```
Mon social/
├── Mes fiches de paie/
│   ├── [AAAA-MM]/
│   └── ...
├── Mes DPAE/
│   └── ...
├── Mes modèles de contrat de travail/
│   └── ...
├── Mes salariés/
│   └── [Nom du salarié]/
│       ├── Contrats/
│       └── ...     ← avenants, courriers, suivi libre
├── Mes déclarations sociales/      ← DSN, bordereaux URSSAF
│   └── [AAAA]/
│       └── [AAAA-MM]/
└── Mes attestations URSSAF/        ← attestations de vigilance, relevés de situation
    └── ...
```

- [ ] **Step 2: Update "Ce qu'il faut retenir" section**

Find the existing block:
```markdown
**Ce qu'il faut retenir :**

- `Mes fiches de paie/` contient les bulletins de paie de **tous les salariés**, classés dans des **sous-dossiers chronologiques** par mois (`Mes fiches de paie/2026-03/`). C'est l'emplacement de référence — pratique pour un export groupé (ex. envoi au comptable).
- `Mes DPAE/` contient les déclarations préalables à l'embauche, en structure plate.
- `Mes modèles de contrat de travail/` regroupe les **gabarits réutilisables** à dupliquer et adapter. Pas de documents signés ici — uniquement des modèles types.
- `Mes salariés/` offre une **vue par salarié** : chaque sous-dossier contient les contrats signés, avenants et documents de suivi du salarié. `Contrats/` est imposé ; le reste de l'organisation est libre par salarié.
```

Replace with:
```markdown
**Ce qu'il faut retenir :**

- `Mes fiches de paie/` contient les bulletins de paie de **tous les salariés**, classés dans des **sous-dossiers chronologiques** par mois (`Mes fiches de paie/2026-03/`). C'est l'emplacement de référence — pratique pour un export groupé (ex. envoi au comptable).
- `Mes DPAE/` contient les déclarations préalables à l'embauche, en structure plate.
- `Mes modèles de contrat de travail/` regroupe les **gabarits réutilisables** à dupliquer et adapter. Pas de documents signés ici — uniquement des modèles types.
- `Mes salariés/` offre une **vue par salarié** : chaque sous-dossier contient les contrats signés, avenants et documents de suivi du salarié. `Contrats/` est imposé ; le reste de l'organisation est libre par salarié.
- `Mes déclarations sociales/` regroupe les DSN mensuelles et les bordereaux de cotisations URSSAF, classés par année puis par mois.
- `Mes attestations URSSAF/` contient les attestations de vigilance (exigées par les clients pour tout contrat > 5 000 €) et les relevés de situation de compte URSSAF.
```

- [ ] **Step 3: Append new sections at end of file**

Add after the last existing section (`Mes salariés/` → `Contrats/`):

```markdown
---

## `Mes déclarations sociales/`

**Rôle :** déclarations sociales transmises à l'URSSAF — DSN mensuelles et bordereaux de cotisations. Obligatoire pour tout dirigeant SASU (assimilé salarié) même sans salarié.

**Organisation :** un sous-dossier par année (`[AAAA]/`), puis un sous-dossier par mois (`[AAAA-MM]/`). La DSN est mensuelle ; le volume justifie cette double hiérarchie.

**Format des fichiers:** `[AAAA-MM]_[Type].[ext]`

- `[AAAA-MM]` — mois de la déclaration
- `[Type]` — type de document : `DSN`, `Bordereau-cotisations`
- `[ext]` — extension du fichier (`pdf`…)

**Exemples :** `2026-03_DSN.pdf` / `2026-03_Bordereau-cotisations.pdf`

---

## `Mes attestations URSSAF/`

**Rôle :** attestations de vigilance délivrées par l'URSSAF (exigées par les clients pour tout contrat > 5 000 €) et relevés de situation de compte URSSAF.

**Organisation :** structure plate — volume faible (une attestation par trimestre environ).

**Format des fichiers:** `[AAAA-MM]_[Type].[ext]`

- `[AAAA-MM]` — date de délivrance du document
- `[Type]` — type de document : `Attestation-vigilance`, `Releve-situation`
- `[ext]` — extension du fichier (`pdf`…)

**Exemples :** `2026-03_Attestation-vigilance.pdf` / `2026-03_Releve-situation.pdf`
```

- [ ] **Step 4: Run CLI tests**

```bash
cd packages/referentiel-cli && npm test
```

Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add packages/referentiel/classement/mon_social.md
git commit -m "feat(referentiel): add URSSAF/DSN sections to mon_social (P0)"
```

---

## Task 4 — Create `mes_assurances.md` (P0)

**Context:** The audit (§1.2) found that insurance documents (RC Pro, mutuelle, assurance locaux) have a retention rule in `regles-archivage.md` but no folder. This creates a new `Mes assurances/` root folder.

**Files:**
- Create: `packages/referentiel/classement/mes_assurances.md`
- Modify: `packages/referentiel/classement/__index.md`
- Modify: `packages/referentiel/_index.md`

- [ ] **Step 1: Create `mes_assurances.md`**

Create the file with this content:

```markdown
# `Mes assurances/`

> [Plan de classement](__index.md) — [Référentiel](../_index.md) — v0

Couvertures assurantielles : RC professionnelle, mutuelle et prévoyance, assurance locaux et matériel.


\```
Mes assurances/
├── RC Pro/
│   └── ...
├── Mutuelle et prévoyance/
│   └── ...
└── Assurance locaux et matériel/
    └── ...
\```

**Ce qu'il faut retenir :**

- `RC Pro/` contient les polices, attestations et avis d'échéance de la responsabilité civile professionnelle.
- `Mutuelle et prévoyance/` contient les polices et attestations de mutuelle santé et de prévoyance (obligatoire avec salarié).
- `Assurance locaux et matériel/` contient les polices et attestations d'assurance des locaux professionnels et du matériel.

---

## `RC Pro/`

**Rôle :** responsabilité civile professionnelle — police en vigueur, attestations annuelles, avis d'échéance, courriers compagnie.

**Organisation :** structure plate — volume faible, un ou deux documents par an.

**Format des fichiers:** `[AAAA]_[Type]_[Assureur].[ext]`

- `[AAAA]` — année de validité du document
- `[Type]` — nature du document : `Police`, `Attestation`, `Echeance`, `Resiliation`
- `[Assureur]` — nom de la compagnie d'assurance, forme lisible
- `[ext]` — extension du fichier (`pdf`…)

**Exemples :** `2026_Attestation_Hiscox.pdf` / `2026_Police_Hiscox.pdf`

---

## `Mutuelle et prévoyance/`

**Rôle :** mutuelle santé et prévoyance — police, attestations d'affiliation, relevés de remboursements si conservés.

**Organisation :** structure plate — volume faible.

**Format des fichiers:** `[AAAA]_[Type]_[Assureur].[ext]`

- `[AAAA]` — année de validité du document
- `[Type]` — nature du document : `Police`, `Attestation`, `Remboursement`
- `[Assureur]` — nom de la compagnie, forme lisible
- `[ext]` — extension du fichier (`pdf`…)

**Exemple :** `2026_Attestation_AlanSante.pdf`

---

## `Assurance locaux et matériel/`

**Rôle :** assurance des locaux professionnels (bureau, atelier) et du matériel (ordinateurs, outillage).

**Organisation :** structure plate — volume faible.

**Format des fichiers:** `[AAAA]_[Type]_[Assureur].[ext]`

- `[AAAA]` — année de validité du document
- `[Type]` — nature du document : `Police`, `Attestation`, `Echeance`
- `[Assureur]` — nom de la compagnie, forme lisible
- `[ext]` — extension du fichier (`pdf`…)

**Exemple :** `2026_Police_MMA.pdf`
```

Note: remove the `\` before the triple-backtick fence in the actual file.

- [ ] **Step 2: Update `classement/__index.md` table**

Add `Mes assurances/` row to the table of root folders. After the `Ma banque et caisse/` row, insert:

```markdown
| `[Mes assurances/](mes_assurances.md)` | Couvertures assurantielles | RC Pro, mutuelle/prévoyance, assurance locaux |
```

- [ ] **Step 3: Update `_index.md` sommaire**

Add a line in the Sommaire section of `packages/referentiel/_index.md`:

```markdown
- [Plan de classement](classement/__index.md) — L'arborescence de tes dossiers : quels dossiers créer, comment les organiser, et pourquoi.
```

No change needed there — the sommaire points to the plan index. But update the description of `Ma banque et caisse/` in the `__index.md` only.

- [ ] **Step 4: Run CLI tests**

```bash
cd packages/referentiel-cli && npm test
```

Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add packages/referentiel/classement/mes_assurances.md packages/referentiel/classement/__index.md
git commit -m "feat(referentiel): add Mes assurances/ folder with RC Pro, mutuelle, locaux (P0)"
```

---

## Task 5 — Delete `raccourcis-liens.md`, update references (P1)

**Context:** The audit (§5) decided to suppress shortcuts/symlinks in v0. The file exists and is referenced in `_index.md` and `regles-archivage.md`.

**Files:**
- Delete: `packages/referentiel/raccourcis-liens.md`
- Modify: `packages/referentiel/_index.md`
- Modify: `packages/referentiel/regles-archivage.md`

- [ ] **Step 1: Delete `raccourcis-liens.md`**

```bash
rm packages/referentiel/raccourcis-liens.md
```

- [ ] **Step 2: Remove link from `_index.md`**

Find in `packages/referentiel/_index.md`:
```markdown
- [Raccourcis et liens](raccourcis-liens.md) — Comment naviguer dans tes documents depuis plusieurs angles sans jamais dupliquer.
```

Delete that line entirely.

- [ ] **Step 3: Remove reference from `regles-archivage.md`**

Find in `packages/referentiel/regles-archivage.md`:
```markdown
**Jamais de duplication.** Un document n'existe qu'à un seul endroit physique. Les raccourcis (voir [Raccourcis et liens](raccourcis-liens.md)) ne comptent pas comme des copies.
```

Replace with:
```markdown
**Jamais de duplication.** Un document n'existe qu'à un seul endroit physique.
```

- [ ] **Step 4: Run CLI tests**

```bash
cd packages/referentiel-cli && npm test
```

Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add -u packages/referentiel/
git commit -m "feat(referentiel): remove raccourcis-liens.md (suppressed in v0)"
```

---

## Task 6 — Enrich `mon_juridique.md` with mandatory SASU folders (P1)

**Context:** The audit (§2.2) found `Mon juridique/` missing obligatory SASU registers, leases/domiciliation, CGV, and an optional PI section.

**Files:**
- Modify: `packages/referentiel/classement/mon_juridique.md`

- [ ] **Step 1: Update tree in `mon_juridique.md`**

Replace existing tree:
```
Mon juridique/
├── Mes statuts/
│   └── ...
├── Mes K-bis/
│   └── ...
└── Mes PV d'assemblée/
    └── ...
```

With:
```
Mon juridique/
├── Mes statuts/
│   └── ...
├── Mes K-bis/
│   └── ...
├── Mes PV et décisions/            ← PV d'AG + décisions de l'associé unique (SASU)
│   └── ...
├── Mes registres/
│   ├── Registre des mouvements de titres/
│   └── Registre des décisions/
├── Mes baux et domiciliation/
│   └── ...
├── Mes CGV et mentions légales/
│   └── ...
└── Mes marques et licences/        ← optionnel : indépendants numérique/créatif
    └── ...
```

- [ ] **Step 2: Update "Ce qu'il faut retenir"**

Replace:
```markdown
**Ce qu'il faut retenir :**

- `Mes statuts/` contient les statuts constitutifs et leurs mises à jour successives.
- `Mes K-bis/` contient les extraits K-bis demandés ou reçus.
- `Mes PV d'assemblée/` contient les procès-verbaux d'assemblée générale (approbation des comptes, décisions extraordinaires…).
```

With:
```markdown
**Ce qu'il faut retenir :**

- `Mes statuts/` contient les statuts constitutifs et leurs mises à jour successives.
- `Mes K-bis/` contient les extraits K-bis demandés ou reçus.
- `Mes PV et décisions/` contient les PV d'assemblée générale ET les décisions de l'associé unique (SASU). En SASU, les décisions importantes remplacent les délibérations collectives.
- `Mes registres/` contient les registres obligatoires pour une SASU : mouvements de titres et registre des décisions.
- `Mes baux et domiciliation/` contient les baux commerciaux et contrats de domiciliation.
- `Mes CGV et mentions légales/` contient les conditions générales de vente, CGU, mentions légales et politique de confidentialité.
- `Mes marques et licences/` (optionnel) contient les dépôts de marque INPI, licences logicielles et cessions de droits d'auteur.
```

- [ ] **Step 3: Rename section `Mes PV d'assemblée/` → `Mes PV et décisions/`**

In `mon_juridique.md`, replace the section heading:
```markdown
## `Mes PV d'assemblée/`
```
with:
```markdown
## `Mes PV et décisions/`
```

And replace the Rôle description:
```markdown
**Rôle :** procès-verbaux d'assemblée générale ordinaire ou extraordinaire (approbation des comptes, nomination de gérant, décisions stratégiques…).
```
with:
```markdown
**Rôle :** procès-verbaux d'assemblée générale (AGO/AGE) et décisions de l'associé unique (SASU). En SASU, les décisions importantes de l'associé unique ont la même valeur juridique qu'un PV d'AG.
```

And update format and example to include `Decision-AU`:
```markdown
**Format des fichiers:** `[AAAA]_[Type]_[Objet].[ext]`

- `[AAAA]` — année de la décision ou de l'assemblée
- `[Type]` — `PV-AG` (assemblée générale) ou `Decision-AU` (décision associé unique)
- `[Objet]` — objet principal (approbation-comptes, dividendes, nomination-gerant…)
- `[ext]` — extension du fichier (`pdf`, `docx`…)

**Exemples :** `2026_PV-AG_approbation-comptes.pdf` / `2026_Decision-AU_dividendes.pdf`
```

- [ ] **Step 4: Append new sections at end of file**

Add after the `Mes PV et décisions/` section:

```markdown
---

## `Mes registres/`

**Rôle :** registres obligatoires pour une SASU — le registre des mouvements de titres et le registre des décisions sont légalement requis et doivent être tenus à jour.

**Organisation :** deux sous-dossiers fixes. Chaque registre est un document mis à jour en continu ; on conserve les versions successives (PDF exporté ou scan du registre papier).

```
Mes registres/
├── Registre des mouvements de titres/
└── Registre des décisions/
```

**Format des fichiers:** `[AAAA]_Registre_[Type].[ext]`

- `[AAAA]` — année de l'export ou du scan
- `[Type]` — `Mouvements-titres`, `Decisions`
- `[ext]` — extension du fichier (`pdf`…)

**Exemple :** `2026_Registre_Decisions.pdf`

---

## `Mes baux et domiciliation/`

**Rôle :** baux commerciaux, contrats de sous-location, contrats de domiciliation. Inclut les avenants et les quittances de loyer si conservées.

**Organisation :** structure plate — volume faible.

**Format des fichiers:** `[AAAA]_[Type]_[Bailleur].[ext]`

- `[AAAA]` — année de signature du contrat
- `[Type]` — type de document : `Bail-commercial`, `Domiciliation`, `Avenant`, `Quittance`
- `[Bailleur]` — nom du bailleur ou de la société de domiciliation, forme lisible
- `[ext]` — extension du fichier (`pdf`…)

**Exemple :** `2026_Domiciliation_Regus.pdf`

---

## `Mes CGV et mentions légales/`

**Rôle :** conditions générales de vente (CGV), conditions générales d'utilisation (CGU), mentions légales du site web, politique de confidentialité. Documents contractuels qui régissent la relation avec les clients et les obligations légales d'affichage.

**Organisation :** structure plate — volume faible, une version par année.

**Format des fichiers:** `[AAAA]_[Type]_v[N].[ext]`

- `[AAAA]` — année de la version
- `[Type]` — type de document : `CGV`, `CGU`, `Mentions-legales`, `Politique-confidentialite`
- `v[N]` — numéro de version (`v1`, `v2`…)
- `[ext]` — extension du fichier (`pdf`…)

**Exemple :** `2026_CGV_v2.pdf`

---

## `Mes marques et licences/`

> **Dossier optionnel** — utile pour les indépendants du numérique, du créatif ou de la tech.

**Rôle :** dépôts de marque INPI, certificats d'enregistrement, licences logicielles (SaaS, perpétuelles), contrats de cession ou de licence de droits d'auteur.

**Organisation :** structure plate — volume variable selon l'activité.

**Format des fichiers:** `[AAAA]_[Type]_[Objet].[ext]`

- `[AAAA]` — année du dépôt, de la signature ou du début de validité
- `[Type]` — type de document : `Depot-marque`, `Licence`, `Cession-droits`, `Certificat`
- `[Objet]` — nom de la marque, du logiciel ou de l'œuvre concerné, forme lisible
- `[ext]` — extension du fichier (`pdf`…)

**Exemples :** `2026_Depot-marque_NomDeMarque.pdf` / `2026_Licence_Figma.pdf`
```

Note: remove the `\` before the triple-backtick fence in the `Mes registres/` subsection.

- [ ] **Step 5: Run CLI tests**

```bash
cd packages/referentiel-cli && npm test
```

Expected: all tests pass.

- [ ] **Step 6: Commit**

```bash
git add packages/referentiel/classement/mon_juridique.md
git commit -m "feat(referentiel): enrich Mon juridique with registres, baux, CGV, marques (P1)"
```

---

## Task 7 — Rename and enrich `ma_banque_et_caisse.md` → `ma_banque.md` (P1)

**Context:** The audit (§2.1) found the folder name noisy ("et caisse" irrelevant for SASU without cash), missing a `Mes RIB/` section, and a flat structure that can't handle multiple banks.

**Files:**
- Rename: `packages/referentiel/classement/ma_banque_et_caisse.md` → `packages/referentiel/classement/ma_banque.md`
- Modify (after rename): `packages/referentiel/classement/ma_banque.md`
- Modify: `packages/referentiel/classement/__index.md`
- Modify: `packages/referentiel/regles-archivage.md`

- [ ] **Step 1: Git rename the file**

```bash
git mv packages/referentiel/classement/ma_banque_et_caisse.md packages/referentiel/classement/ma_banque.md
```

- [ ] **Step 2: Update file header and title in `ma_banque.md`**

Replace:
```markdown
# `Ma banque et caisse/`

> [Plan de classement](__index.md) — [Référentiel](../_index.md) — v0

Trésorerie : relevés bancaires.
```

With:
```markdown
# `Ma banque/`

> [Plan de classement](__index.md) — [Référentiel](../_index.md) — v0

Trésorerie : relevés bancaires et RIB.
```

- [ ] **Step 3: Update tree in `ma_banque.md`**

Replace:
```
Ma banque et caisse/
└── Mes relevés bancaires/
    └── ...
```

With:
```
Ma banque/
├── Mes relevés bancaires/
│   └── [Nom banque]/               ← un sous-dossier par établissement
│       └── [AAAA-MM]/
└── Mes RIB/
    └── ...
```

- [ ] **Step 4: Update "Ce qu'il faut retenir" section**

Replace:
```markdown
**Ce qu'il faut retenir :**

- `Mes relevés bancaires/` contient les relevés de compte reçus de ta banque, classés à plat. C'est l'emplacement de référence — pratique pour un export groupé (ex. envoi au comptable).
```

With:
```markdown
**Ce qu'il faut retenir :**

- `Mes relevés bancaires/` contient les relevés de compte reçus de ta banque, organisés par établissement puis par mois. Si tu n'as qu'un seul compte, crée un seul sous-dossier `[Nom banque]/`.
- `Mes RIB/` contient les RIB actifs de chaque compte bancaire — demandés en permanence par les clients, fournisseurs et administrations.
```

- [ ] **Step 5: Update `Mes relevés bancaires/` section**

Replace the existing section content:

```markdown
## `Mes relevés bancaires/`

**Rôle :** relevés de compte bancaire reçus (PDF ou export depuis l'espace en ligne).

**Organisation :** un sous-dossier par établissement bancaire (`[Nom banque]/`), puis un sous-dossier par mois (`[AAAA-MM]/`). Si tu n'as qu'un seul compte, l'organisation reste la même — un seul sous-dossier banque.

**Format des fichiers:** `[AAAA-MM]_Releve_[Nom-banque]_[Numero].[ext]`

- `[AAAA-MM]` — mois couvert par le relevé
- `[Nom-banque]` — nom de la banque, forme lisible (ex. `Credit-Mutuel`, `BNP`, `Qonto`)
- `[Numero]` — numéro du relevé tel qu'il apparaît sur le document
- `[ext]` — extension du fichier (`pdf`, `csv`…)

**Exemple :** `2026-03_Releve_Credit-Mutuel_003.pdf`
```

- [ ] **Step 6: Append `Mes RIB/` section**

Add at end of file:

```markdown
---

## `Mes RIB/`

**Rôle :** relevés d'identité bancaire (RIB) de chaque compte professionnel actif. Documents demandés en permanence — clients, fournisseurs, URSSAF, administrations.

**Organisation :** structure plate — un fichier par compte bancaire. Le RIB ne change que si le compte change ; pas de sous-dossiers chronologiques.

**Format des fichiers:** `RIB_[Nom-banque]_[Compte].[ext]`

- `[Nom-banque]` — nom de la banque, forme lisible
- `[Compte]` — type ou libellé du compte si plusieurs comptes chez la même banque (`Courant`, `Epargne-pro`…) — omettre si un seul compte
- `[ext]` — extension du fichier (`pdf`…)

**Exemples :** `RIB_Credit-Mutuel.pdf` / `RIB_Qonto_Courant.pdf`
```

- [ ] **Step 7: Update `__index.md` link and table**

In `classement/__index.md`, replace all occurrences of `ma_banque_et_caisse.md` with `ma_banque.md`, and replace `Ma banque et caisse/` with `Ma banque/` in the table.

- [ ] **Step 8: Update `regles-archivage.md`**

Replace `Ma banque et caisse/` with `Ma banque/` everywhere in `regles-archivage.md` (table row and any inline references).

Also update the archive zip name example in the manifest example:
- `ma_banque_et_caisse_2024.zip` → `ma_banque_2024.zip` (2 occurrences)

- [ ] **Step 9: Run CLI tests**

```bash
cd packages/referentiel-cli && npm test
```

Expected: all tests pass.

- [ ] **Step 10: Commit**

```bash
git add packages/referentiel/classement/ma_banque.md packages/referentiel/classement/__index.md packages/referentiel/regles-archivage.md
git commit -m "feat(referentiel): rename Ma banque et caisse → Ma banque, add RIB section, multi-bank structure (P1)"
```

---

## Task 8 — Consolidate devis/offre in `mes_ventes.md` (P1)

**Context:** The audit (§2.3) found three separate model folders (contrat, devis, offre) where for a solo indep, devis and offre are the same thing. Also, the `Offres/` sub-folder in each client folder should be merged into `Devis/`.

**Files:**
- Modify: `packages/referentiel/classement/mes_ventes.md`
- Modify: `packages/referentiel/regles-nommage.md`

- [ ] **Step 1: Update tree in `mes_ventes.md`**

Replace existing tree:
```
Mes ventes/
├── Mes factures clients/
│   ├── [AAAA-MM]/
│   └── ...
├── Mes modèles de contrat/
│   └── ...
├── Mes modèles de devis/
│   └── ...
├── Mes modèles d'offre/
│   └── ...
└── Mes clients/
    └── [Nom du client]/
        ├── Contrats/
        ├── Devis/
        ├── Offres/
        └── ...     ← notes, CR, suivi libre
```

With:
```
Mes ventes/
├── Mes factures clients/
│   ├── [AAAA-MM]/
│   └── ...
├── Mes modèles/                    ← contrat + devis/offre réunis
│   ├── Contrats/
│   └── Devis et offres/
└── Mes clients/
    └── [Nom du client]/
        ├── Contrats/
        ├── Devis/                  ← inclut les propositions commerciales / offres
        └── ...     ← notes, CR, suivi libre
```

- [ ] **Step 2: Update "Ce qu'il faut retenir" section**

Replace:
```markdown
- `Mes modèles de contrat/`, `Mes modèles de devis/` et `Mes modèles d'offre/` regroupent les **gabarits réutilisables** à dupliquer et adapter. Pas de documents signés ni finalisés ici — uniquement des modèles types.
- `Mes clients/` offre une **vue par client** : chaque sous-dossier contient les contrats, devis et offres réels du client ainsi que les documents de suivi (notes, CR…). `Contrats/`, `Devis/` et `Offres/` sont imposés ; le reste de l'organisation est libre par client.
```

With:
```markdown
- `Mes modèles/` regroupe les **gabarits réutilisables** : sous-dossier `Contrats/` pour les modèles de contrat, sous-dossier `Devis et offres/` pour les modèles de devis et d'offre commerciale (fusionnés — pour un indep solo, un devis est une offre).
- `Mes clients/` offre une **vue par client** : chaque sous-dossier contient les contrats et devis réels du client ainsi que les documents de suivi (notes, CR…). `Contrats/` et `Devis/` sont imposés ; le reste de l'organisation est libre par client.
```

- [ ] **Step 3: Replace the three model sections with a single `Mes modèles/` section**

Remove sections `Mes modèles de contrat/`, `Mes modèles de devis/`, `Mes modèles d'offre/` and replace them with:

```markdown
## `Mes modèles/`

**Rôle :** gabarits réutilisables à dupliquer et adapter. Pas de document signé ni finalisé ici — uniquement les modèles types. Deux sous-dossiers fixes.

```
Mes modèles/
├── Contrats/       ← modèles de contrat et d'avenant
└── Devis et offres/  ← modèles de devis et de propositions commerciales
```

### `Contrats/` (modèles)

**Format des fichiers:** `modele-contrat_[objet]_v[N].[ext]`

- `[objet]` — type de contrat en mots séparés par des tirets (ex. `maintenance-annuelle`, `prestation-conseil`)
- `v[N]` — version du gabarit (`v1`, `v2`…)
- `[ext]` — extension du fichier (`.docx`, `.odt`…)

**Exemple :** `modele-contrat_maintenance-annuelle_v2.docx`

### `Devis et offres/` (modèles)

**Format des fichiers:** `modele-devis_[objet]_v[N].[ext]`

- `[objet]` — type de prestation ou de format (ex. `prestation-conseil`, `formation-react`)
- `v[N]` — version du gabarit (`v1`, `v2`…)
- `[ext]` — extension du fichier (`.docx`, `.odt`…)

**Exemple :** `modele-devis_prestation-conseil_v1.docx`
```

Note: remove the `\` before the triple-backtick fence.

- [ ] **Step 4: Update `Mes clients/` section**

In the `Mes clients/` section tree block, remove `Offres/`:
```
Mes clients/
└── [Nom du client]/
    ├── Contrats/    ← contrats et avenants réels du client
    ├── Devis/       ← devis et propositions commerciales envoyés au client
    └── ...          ← notes, CR, suivi (libre)
```

Update `Mes clients/` intro to remove mention of `Offres/`:
```markdown
**Organisation :** un sous-dossier par client, nom en français lisible (`[Nom du client]/`). Les sous-dossiers `Contrats/` et `Devis/` sont imposés dans chaque client ; le reste de l'organisation est libre.
```

Remove the `### Offres/ (dans chaque client)` subsection entirely.

Update `### Devis/ (dans chaque client)` rôle to mention it absorbs offers:
```markdown
**Rôle :** propositions chiffrées et offres commerciales envoyées au client (devis, propositions commerciales, offres personnalisées). Pour un indep solo, un devis IS l'offre — pas de distinction nécessaire. Structure plate — pas de sous-dossiers mensuels, le volume par client reste faible.
```

- [ ] **Step 5: Update `regles-nommage.md` — remove offre sections**

In `regles-nommage.md`, remove the sections:
- `### \`Mes ventes/mes_modeles_de_devis/\``
- `### \`Mes ventes/mes_modeles_d_offre/\``
- `### \`Mes ventes/Mes clients/[Nom du client]/Offres/\``

And update the section `### \`Mes ventes/mes_modeles_de_contrat/\`` to reference the new path:
- Rename to `### \`Mes ventes/Mes modèles/Contrats/\``

Add a new section for the merged models:

```markdown
### `Mes ventes/Mes modèles/Devis et offres/`

**Rôle :** gabarits de devis et d'offres commerciales à dupliquer et adapter.

**Format :** `modele-devis_[objet]_v[N].[ext]`

**Exemple :** `modele-devis_prestation-conseil_v1.docx`

Pas de préfixe date : ce sont des gabarits réutilisables. La version (`v1`, `v2`) distingue les révisions.
```

- [ ] **Step 6: Run CLI tests**

```bash
cd packages/referentiel-cli && npm test
```

Expected: all tests pass.

- [ ] **Step 7: Commit**

```bash
git add packages/referentiel/classement/mes_ventes.md packages/referentiel/regles-nommage.md
git commit -m "feat(referentiel): consolidate devis/offre into single Mes modeles/ folder (P1)"
```

---

## Task 9 — Add module frontmatter to all `classement/*.md` files (P2)

**Context:** The audit (§4) proposes a core + modules system driven by frontmatter YAML so the CLI can deploy only the folders relevant to a user's profile.

**Files:**
- Modify: All `packages/referentiel/classement/*.md` (except `__index.md`)
- Modify: `packages/referentiel/classement/__index.md`

- [ ] **Step 1: Add frontmatter to core files**

Add this frontmatter block at the very top of each file (before the `# Title` line):

`mes_ventes.md`:
```yaml
---
id: mes_ventes
module: core
profiles: [indep-solo-micro, sasu-solo, sasu-solo-employe, indep-creatif-tech]
required: true
---
```

`mes_achats.md`:
```yaml
---
id: mes_achats
module: core
profiles: [indep-solo-micro, sasu-solo, sasu-solo-employe, indep-creatif-tech]
required: true
---
```

`mon_juridique.md`:
```yaml
---
id: mon_juridique
module: core
profiles: [indep-solo-micro, sasu-solo, sasu-solo-employe, indep-creatif-tech]
required: true
---
```

`ma_fiscalite.md`:
```yaml
---
id: ma_fiscalite
module: core
profiles: [indep-solo-micro, sasu-solo, sasu-solo-employe, indep-creatif-tech]
required: true
---
```

`ma_banque.md`:
```yaml
---
id: ma_banque
module: core
profiles: [indep-solo-micro, sasu-solo, sasu-solo-employe, indep-creatif-tech]
required: true
---
```

`archives.md`:
```yaml
---
id: archives
module: core
profiles: [indep-solo-micro, sasu-solo, sasu-solo-employe, indep-creatif-tech]
required: true
---
```

- [ ] **Step 2: Add frontmatter to module files**

`mon_social.md`:
```yaml
---
id: mon_social
module: dirigeant-assimile-salarie
profiles: [sasu-solo, sasu-solo-employe]
required: true
---
```

`mes_assurances.md`:
```yaml
---
id: mes_assurances
module: assurances
profiles: [sasu-solo, sasu-solo-employe, indep-creatif-tech]
required: false
---
```

- [ ] **Step 3: Update `classement/__index.md` with module documentation**

Add a new section after the root folders table:

```markdown
---

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

- [ ] **Step 4: Run CLI tests**

```bash
cd packages/referentiel-cli && npm test
```

Expected: all tests pass (frontmatter is transparent to the current CLI — `walk-referentiel.ts` reads files without parsing content).

- [ ] **Step 5: Commit**

```bash
git add packages/referentiel/classement/
git commit -m "feat(referentiel): add module frontmatter to all classement files, document profiles (P2)"
```

---

## Task 10 — Create `demarrage-rapide.md` (P2)

**Context:** The audit (§6) identified the lack of an entry-point guide. A solo SASU user needs to understand in one page: which profile to choose, the resulting folder tree, and the 3-4 daily gestures.

**Files:**
- Create: `packages/referentiel/demarrage-rapide.md`
- Modify: `packages/referentiel/_index.md`

- [ ] **Step 1: Create `demarrage-rapide.md`**

```markdown
# Démarrage rapide

> Partie du [Référentiel de gestion documentaire](./_index.md) — v0

Ce guide présente le cas le plus courant : **SASU solo sans salarié** (profil `sasu-solo`). Modules activés : `core` + `dirigeant-assimile-salarie` + `assurances`.

---

## Arborescence résultante

```
📁 Ma banque/
   └── Mes relevés bancaires/
       └── [Nom banque]/
           └── [AAAA-MM]/
   └── Mes RIB/
📁 Ma fiscalité/
   └── Mes déclarations de TVA/
   └── Mes liasses fiscales/
   └── Mes avis d'imposition/
   └── Mes avis de CFE/
📁 Mes achats/
   └── Mes factures fournisseurs/
   └── Mes fournisseurs/
📁 Mes assurances/
   └── RC Pro/
   └── Mutuelle et prévoyance/
   └── Assurance locaux et matériel/
📁 Mes ventes/
   └── Mes factures clients/
   └── Mes modèles/
   └── Mes clients/
📁 Mon juridique/
   └── Mes statuts/
   └── Mes K-bis/
   └── Mes PV et décisions/
   └── Mes registres/
   └── Mes baux et domiciliation/
   └── Mes CGV et mentions légales/
📁 Mon social/
   └── Mes fiches de paie/
   └── Mes DPAE/
   └── Mes modèles de contrat de travail/
   └── Mes salariés/
   └── Mes déclarations sociales/
   └── Mes attestations URSSAF/
📁 Archives/
```

---

## 4 gestes quotidiens

| Situation | Où ranger |
|-----------|-----------|
| Tu reçois une **facture fournisseur** | `Mes achats/Mes factures fournisseurs/[AAAA-MM]/` |
| Tu envoies une **facture client** | `Mes ventes/Mes factures clients/[AAAA-MM]/` |
| Tu reçois un **relevé bancaire** | `Ma banque/Mes relevés bancaires/[Nom banque]/[AAAA-MM]/` |
| Tu reçois une **attestation URSSAF** | `Mon social/Mes attestations URSSAF/` |

---

## Initialiser l'arborescence (CLI)

```bash
# Depuis la racine du projet
npx referentiel-cli init --profile sasu-solo --target /chemin/vers/mon/drive
```

Le CLI crée tous les dossiers correspondant au profil `sasu-solo` dans le dossier cible.

---

## En savoir plus

- [Plan de classement complet](classement/__index.md)
- [Règles de nommage](regles-nommage.md)
- [Règles d'archivage](regles-archivage.md)
```

Note: remove the `\` before the triple-backtick fences in the actual file.

- [ ] **Step 2: Add link to `_index.md` sommaire**

In `packages/referentiel/_index.md`, add at the top of the Sommaire section (before the existing items):

```markdown
- [Démarrage rapide](demarrage-rapide.md) — Le profil SASU solo, l'arborescence résultante, et les 4 gestes quotidiens.
```

- [ ] **Step 3: Run CLI tests**

```bash
cd packages/referentiel-cli && npm test
```

Expected: all tests pass.

- [ ] **Step 4: Commit**

```bash
git add packages/referentiel/demarrage-rapide.md packages/referentiel/_index.md
git commit -m "feat(referentiel): add demarrage-rapide.md for SASU solo profile (P2)"
```

---

## Self-Review

### Spec coverage check

| Audit section | Plan task |
|---------------|-----------|
| §1.1 URSSAF/DSN absents | Task 3 ✓ |
| §1.2 Assurances sans dossier | Task 4 ✓ |
| §1.3 PI/licences absentes | Task 6 (Mes marques et licences/) ✓ |
| §2.1 Banque squelettique | Task 7 ✓ |
| §2.2 Juridique trop maigre | Task 6 ✓ |
| §2.3 Confusion devis/offre | Task 8 ✓ |
| §3 Incohérences de nommage | Tasks 1, 2 ✓ |
| §4 Modularité | Task 9 ✓ |
| §5 Raccourcis supprimés | Task 5 ✓ |
| §6 Démarrage rapide | Task 10 ✓ |

### No placeholders — all tasks contain actual content to write.

### Type consistency — no cross-task type references; each task is self-contained.
