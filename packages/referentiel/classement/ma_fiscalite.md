# `Ma fiscalité/`

> [Plan de classement](__index.md) — [Référentiel](../_index.md) — v0

Obligations fiscales : déclarations de TVA, liasses fiscales, avis d'imposition, avis de CFE.


```
Ma fiscalité/
├── Mes déclarations de TVA/
│   ├── [AAAA-MM]/
│   └── ...
├── Mes liasses fiscales/
│   └── ...
├── Mes avis d'imposition/
│   └── ...
└── Mes avis de CFE/
    └── ...
```

**Ce qu'il faut retenir :**

- `Mes déclarations de TVA/` contient les déclarations (CA3, CA12…), classées dans des **sous-dossiers chronologiques** par mois (`Mes déclarations de TVA/2026-03/`). C'est l'emplacement de référence — pratique pour un export groupé (ex. envoi au comptable).
- `Mes liasses fiscales/` contient les liasses fiscales annuelles, en structure plate.
- `Mes avis d'imposition/` contient les avis d'imposition reçus (IR, IS…), en structure plate.
- `Mes avis de CFE/` contient les avis de cotisation foncière des entreprises, en structure plate.

---

## `Mes déclarations de TVA/`

**Rôle :** déclarations de TVA transmises à l'administration fiscale (CA3 mensuelle/trimestrielle, CA12 annuelle…).

**Organisation :** un sous-dossier par mois de déclaration, format `AAAA-MM` (`Mes déclarations de TVA/2026-03/`).

**Format des fichiers:** `[AAAA-MM]_Declaration-TVA.[ext]`

- `[AAAA-MM]` — période couverte par la déclaration
- `[ext]` — extension du fichier (`pdf`…)

**Exemple :** `2026-03_Declaration-TVA.pdf`

---

## `Mes liasses fiscales/`

**Rôle :** liasses fiscales annuelles (bilan, compte de résultat, annexes) transmises à l'administration fiscale.

**Organisation :** structure plate — pas de sous-dossiers, une liasse par exercice.

**Format des fichiers:** `[AAAA]_Liasse-fiscale.[ext]`

- `[AAAA]` — exercice fiscal concerné
- `[ext]` — extension du fichier (`pdf`…)

**Exemple :** `2025_Liasse-fiscale.pdf`

---

## `Mes avis d'imposition/`

**Rôle :** avis d'imposition reçus de l'administration fiscale (impôt sur le revenu, impôt sur les sociétés…).

**Organisation :** structure plate — pas de sous-dossiers, un avis par an et par type.

**Format des fichiers:** `[AAAA]_Avis-imposition_[Type].[ext]`

- `[AAAA]` — année fiscale concernée
- `[Type]` — type d'impôt (IR, IS…)
- `[ext]` — extension du fichier (`pdf`…)

**Exemple :** `2025_Avis-imposition_IR.pdf`

---

## `Mes avis de CFE/`

**Rôle :** avis de cotisation foncière des entreprises reçus de l'administration fiscale.

**Organisation :** structure plate — pas de sous-dossiers, un avis par an.

**Format des fichiers:** `[AAAA]_Avis-CFE.[ext]`

- `[AAAA]` — année fiscale concernée
- `[ext]` — extension du fichier (`pdf`…)

**Exemple :** `2025_Avis-CFE.pdf`
