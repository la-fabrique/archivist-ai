---
id: ma_banque.releves_bancaires
folder_name: "Mes relevés bancaires"
path: "Ma banque/Mes relevés bancaires"
parent: ma_banque
dynamic: false
option: core
required: true
description: "Relevés de compte bancaire, organisés par établissement puis par mois"
organization:
  type: per_entity
  entity_subfolder: ma_banque.releves_bancaires.nom_banque
---

## `Mes relevés bancaires/`

**Rôle :** relevés de compte bancaire reçus. Un sous-dossier par établissement, puis un sous-dossier par mois.

```
Mes relevés bancaires/
└── [Nom banque]/
    └── [AAAA-MM]/
```
