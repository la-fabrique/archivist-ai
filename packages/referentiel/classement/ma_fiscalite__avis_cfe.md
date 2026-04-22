---
id: ma_fiscalite.avis_cfe
folder_name: "Mes avis de CFE"
path: "Ma fiscalité/Mes avis de CFE"
parent: ma_fiscalite
dynamic: false
option: core
required: true
description: "Avis de cotisation foncière des entreprises, structure plate"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_Avis-CFE.[ext]"
  fields:
    - name: AAAA
      description: "année fiscale concernée"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2025_Avis-CFE.pdf"
---

## `Mes avis de CFE/`

**Rôle :** avis de cotisation foncière des entreprises. Structure plate, un avis par an.

**Exemple :** `2025_Avis-CFE.pdf`
