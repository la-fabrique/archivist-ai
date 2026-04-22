---
id: mes_ventes.clients.nom_client.contrats
folder_name: "Contrats"
path: "Mes ventes/Mes clients/[Nom du client]/Contrats"
parent: mes_ventes.clients.nom_client
dynamic: false
option: core
required: true
description: "Contrats et avenants réels signés avec le client"
organization:
  type: flat
file_naming:
  pattern: "[AAAA-MM]_Contrat_[Nom client]_[Numero-Revision].[ext]"
  fields:
    - name: AAAA-MM
      description: "date d'émission du contrat ou de l'avenant"
    - name: Nom client
      description: "nom du client, forme lisible"
    - name: Numero-Revision
      description: "référence libre (numéro de contrat, objet, version…)"
    - name: ext
      description: "extension du fichier (pdf, docx…)"
  example: "2026-04_Contrat_Acme_C2026-01.pdf"
---

### `Contrats/` (client)

**Rôle :** tout contrat ou avenant une fois sorti du statut brouillon : versions partagées, PDF signé, scans. Structure plate.

**Format des fichiers :** `[AAAA-MM]_Contrat_[Nom client]_[Numero-Revision].[ext]`

Avenant : `[AAAA-MM]_Avenant_[Nom client]_[Numero-Revision].[ext]`

**Exemple :** `2026-04_Contrat_Acme_C2026-01.pdf`
