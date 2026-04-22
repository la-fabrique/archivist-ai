---
id: mon_juridique.baux_domiciliation
folder_name: "Mes baux et domiciliation"
path: "Mon juridique/Mes baux et domiciliation"
parent: mon_juridique
dynamic: false
option: core
required: true
description: "Baux commerciaux, sous-location, contrats de domiciliation"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_[Type]_[Bailleur].[ext]"
  fields:
    - name: AAAA
      description: "année de signature du contrat"
    - name: Type
      description: "type de document : Bail-commercial, Domiciliation, Avenant, Quittance"
    - name: Bailleur
      description: "nom du bailleur ou de la société de domiciliation, forme lisible"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2026_Domiciliation_Regus.pdf"
---

## `Mes baux et domiciliation/`

**Rôle :** baux commerciaux, contrats de sous-location, contrats de domiciliation. Structure plate.

**Exemple :** `2026_Domiciliation_Regus.pdf`
