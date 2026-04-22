---
id: mon_juridique.registres
folder_name: "Mes registres"
path: "Mon juridique/Mes registres"
parent: mon_juridique
dynamic: false
option: core
required: true
description: "Registres obligatoires SASU : mouvements de titres et décisions"
organization:
  type: subdirs
  fixed_subdirs:
    - mon_juridique.registres.mouvements_titres
    - mon_juridique.registres.decisions
---

## `Mes registres/`

**Rôle :** registres légalement obligatoires pour une SASU.

```
Mes registres/
├── Registre des mouvements de titres/
└── Registre des décisions/
```
