---
id: mes_ventes.clients.nom_client.devis
folder_name: "Devis"
path: "Mes ventes/Mes clients/[Nom du client]/Devis"
parent: mes_ventes.clients.nom_client
dynamic: false
option: core
required: true
description: "Devis et propositions commerciales envoyés au client"
organization:
  type: flat
file_naming:
  pattern: "[AAAA-MM]_Devis_[Nom client]_[Numero].[ext]"
  fields:
    - name: AAAA-MM
      description: "date d'émission du devis"
    - name: Nom client
      description: "nom du client, forme lisible"
    - name: Numero
      description: "numéro du devis tel qu'il apparaît dans le logiciel"
    - name: ext
      description: "extension du fichier (pdf, docx…)"
  example: "2026-03_Devis_Martin_D2600001.pdf"
---

### `Devis/` (client)

**Rôle :** propositions chiffrées et offres commerciales envoyées au client. Pour un indép solo, un devis IS l'offre. Structure plate.

**Format des fichiers :** `[AAAA-MM]_Devis_[Nom client]_[Numero].[ext]`

**Exemple :** `2026-03_Devis_Martin_D2600001.pdf`
