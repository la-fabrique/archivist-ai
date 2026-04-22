---
id: mes_achats
folder_name: "Mes achats"
path: "Mes achats"
dynamic: false
option: core
required: true
description: "Relation commerciale entrante : factures fournisseurs, suivi fournisseurs"
organization:
  type: subdirs
  fixed_subdirs:
    - mes_achats.factures_fournisseurs
    - mes_achats.fournisseurs
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
        └── ...
```

**Ce qu'il faut retenir :**

- `Mes factures fournisseurs/` — factures reçues, classées par mois. Voir [Mes factures fournisseurs](mes_achats__factures_fournisseurs.md).
- `Mes fournisseurs/` — vue par fournisseur. Voir [Mes fournisseurs](mes_achats__fournisseurs.md).
