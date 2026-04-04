# `Mes achats/`

> [Plan de classement](__index.md) — [Référentiel](../_index.md) — v0

Dépenses de l'entreprise : factures fournisseurs, assurances.

```
Mes achats/
├── factures_fournisseurs/
│   ├── 2026/
│   │   ├── 2026-01/
│   │   ├── 2026-02/
│   │   └── 2026-03/
│   └── 2025/
│       ├── 2025-01/
│       └── ...
└── assurances/
    ├── polices/
    └── attestations/
```

**Pourquoi un niveau "année" en plus ?** Les factures fournisseurs sont souvent consultées par exercice comptable. Ton comptable te demande "les achats 2025" — le dossier `2025/` répond directement. Pour `Mes ventes/`, les mois sont suffisants car les factures émises sont consultées individuellement.

**Pourquoi les assurances dans `Mes achats/` ?** En comptabilité, une prime d'assurance est une charge. Les polices et attestations sont les justificatifs de cette charge. Ton comptable ira chercher ça au même endroit que les factures fournisseurs.
