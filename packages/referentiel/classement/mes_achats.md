---
id: mes_achats
option: core
required: true
---

# `Mes achats/`

> [Plan de classement](__index.md) — [Référentiel](../_index.md) — v0

Relation commerciale entrante : factures fournisseurs, suivi fournisseurs.


```
Mes achats/
├── Mes factures fournisseurs/
│   ├── [AAAA-MM]/
│   └── ...
└── Mes fournisseurs/
    └── [Nom du fournisseur]/
        └── ...     ← organisation libre
```

**Ce qu'il faut retenir :**

- `Mes factures fournisseurs/` contient les factures **reçues**, classées dans des **sous-dossiers chronologiques** par mois (`Mes factures fournisseurs/2026-03/`). C'est l'emplacement de référence — pratique pour un export groupé (ex. envoi au comptable).
- `Mes fournisseurs/` offre une **vue par fournisseur** : chaque sous-dossier contient les documents liés à la relation avec ce fournisseur (contrats, échanges, polices d'assurance…). L'organisation à l'intérieur de chaque fournisseur est libre.

---

## `Mes factures fournisseurs/`

**Rôle :** factures **reçues** par ton entreprise (une fois validée et comptabilisée, le PDF ou le scan vit ici).

**Organisation :** un sous-dossier par mois de réception utile, format `AAAA-MM` (`Mes factures fournisseurs/2026-03/`).

**Format des fichiers:** `[AAAA-MM]_Facture_[Nom fournisseur]_[Numero].[ext]`

- `[AAAA-MM]` — date d'émission de la facture
- `[Nom fournisseur]` — nom du fournisseur, forme lisible
- `[Numero]` — numéro de la facture tel qu'il apparaît sur le document
- `[ext]` — extension du fichier (`pdf`, `docx`…)

**Exemple :** `2026-03_Facture_OVH_F2600042.pdf`

---

## `Mes fournisseurs/`

**Rôle :** **vue par fournisseur** regroupant les documents directement liés à la relation avec un fournisseur : contrats, polices d'assurance, attestations, échanges de référence. Chaque fournisseur dispose de son propre sous-dossier.

**Organisation :** un sous-dossier par fournisseur, nom en français lisible (`[Nom du fournisseur]/`). L'organisation à l'intérieur de chaque fournisseur est libre.

```
Mes fournisseurs/
└── [Nom du fournisseur]/
    └── ...          ← organisation libre
```
