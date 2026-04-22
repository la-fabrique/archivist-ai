---
id: mon_juridique.statuts
folder_name: "Mes statuts"
path: "Mon juridique/Mes statuts"
parent: mon_juridique
dynamic: false
option: core
required: true
description: "Statuts constitutifs et mises à jour successives"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_Statuts_[Objet].[ext]"
  fields:
    - name: AAAA
      description: "année de signature ou d'enregistrement"
    - name: Objet
      description: "nature du document (constitution, modification-objet-social…)"
    - name: ext
      description: "extension du fichier (pdf, docx…)"
  example: "2026_Statuts_constitution.pdf"
---

## `Mes statuts/`

**Rôle :** statuts constitutifs et leurs mises à jour. Structure plate.

**Exemple :** `2026_Statuts_constitution.pdf`
