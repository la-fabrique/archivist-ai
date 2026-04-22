---
id: ma_fiscalite.avis_imposition
folder_name: "Mes avis d'imposition"
path: "Ma fiscalité/Mes avis d'imposition"
parent: ma_fiscalite
dynamic: false
option: core
required: true
description: "Avis d'imposition reçus (IR, IS…), structure plate"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_Avis-imposition_[Type].[ext]"
  fields:
    - name: AAAA
      description: "année fiscale concernée"
    - name: Type
      description: "type d'impôt (IR, IS…)"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2025_Avis-imposition_IR.pdf"
---

## `Mes avis d'imposition/`

**Rôle :** avis d'imposition reçus (IR, IS…). Structure plate.

**Exemple :** `2025_Avis-imposition_IR.pdf`
