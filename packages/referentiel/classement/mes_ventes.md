---
id: mes_ventes
folder_name: "Mes ventes"
path: "Mes ventes"
dynamic: false
option: core
required: true
description: "Relation commerciale sortante : factures clients, modèles, suivi client"
organization:
  type: subdirs
  fixed_subdirs:
    - mes_ventes.factures_clients
    - mes_ventes.modeles
    - mes_ventes.clients
---

# `Mes ventes/`

> [Plan de classement](__index.md) — [Référentiel](../_index.md) — v0

Relation commerciale sortante : factures clients, modèles de contrat, de devis et d'offre, offres clients, suivi client.

```
Mes ventes/
├── Mes factures clients/
│   ├── [AAAA-MM]/
│   └── ...
├── Mes modèles/
│   ├── Contrats/
│   └── Devis et offres/
└── Mes clients/
    └── [Nom du client]/
        ├── Contrats/
        ├── Devis/
        └── ...
```

**Ce qu'il faut retenir :**

- `Mes factures clients/` — factures émises, classées par mois. Voir [Mes factures clients](mes_ventes__factures_clients.md).
- `Mes modèles/` — gabarits réutilisables contrats et devis. Voir [Mes modèles](mes_ventes__modeles.md).
- `Mes clients/` — vue par client. Voir [Mes clients](mes_ventes__clients.md).
