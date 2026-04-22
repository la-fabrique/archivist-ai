---
id: mes_ventes.clients
folder_name: "Mes clients"
path: "Mes ventes/Mes clients"
parent: mes_ventes
dynamic: false
option: core
required: true
description: "Vue par client : contrats, devis et suivi libre"
organization:
  type: per_entity
  entity_subfolder: mes_ventes.clients.nom_client
---

## `Mes clients/`

**Rôle :** vue par client regroupant les documents directement liés à la relation commerciale. Chaque client dispose de son propre sous-dossier.

**Organisation :** un sous-dossier par client, nom en français lisible (`[Nom du client]/`).

```
Mes clients/
└── [Nom du client]/
    ├── Contrats/
    ├── Devis/
    └── ...
```
