---
id: ma_fiscalite.liasses_fiscales
folder_name: "Mes liasses fiscales"
path: "Ma fiscalité/Mes liasses fiscales"
parent: ma_fiscalite
dynamic: false
option: core
required: true
description: "Liasses fiscales annuelles, structure plate"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_Liasse-fiscale.[ext]"
  fields:
    - name: AAAA
      description: "exercice fiscal concerné"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2025_Liasse-fiscale.pdf"
---

## `Mes liasses fiscales/`

**Rôle :** liasses fiscales annuelles (bilan, compte de résultat, annexes). Structure plate, une liasse par exercice.

**Exemple :** `2025_Liasse-fiscale.pdf`
