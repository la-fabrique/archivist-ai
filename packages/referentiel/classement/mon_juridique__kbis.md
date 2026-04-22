---
id: mon_juridique.kbis
folder_name: "Mes K-bis"
path: "Mon juridique/Mes K-bis"
parent: mon_juridique
dynamic: false
option: core
required: true
description: "Extraits K-bis, justificatifs d'immatriculation"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_Kbis.[ext]"
  fields:
    - name: AAAA
      description: "année d'émission"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2026_Kbis.pdf"
---

## `Mes K-bis/`

**Rôle :** extraits K-bis demandés ou reçus. Structure plate.

**Exemple :** `2026_Kbis.pdf`
