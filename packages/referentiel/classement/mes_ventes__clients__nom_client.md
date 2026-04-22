---
id: mes_ventes.clients.nom_client
folder_name: "[Nom du client]"
path: "Mes ventes/Mes clients/[Nom du client]"
parent: mes_ventes.clients
dynamic: true
option: core
required: true
description: "Dossier par client : nom lisible en français"
organization:
  type: mixed
  fixed_subdirs:
    - mes_ventes.clients.nom_client.contrats
    - mes_ventes.clients.nom_client.devis
  free_subdirs: true
---

### `[Nom du client]/`

**Rôle :** regroupe les documents directement liés à un client : contrats signés, devis envoyés, notes de suivi, comptes-rendus.

Les sous-dossiers `Contrats/` et `Devis/` sont **imposés**. Le reste de l'organisation est libre par client.
