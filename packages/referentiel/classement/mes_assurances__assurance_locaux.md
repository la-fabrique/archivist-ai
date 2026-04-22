---
id: mes_assurances.assurance_locaux
folder_name: "Assurance locaux et matériel"
path: "Mes assurances/Assurance locaux et matériel"
parent: mes_assurances
dynamic: false
option: assurances
required: false
description: "Polices et attestations assurance locaux professionnels et matériel"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_[Type]_[Assureur].[ext]"
  fields:
    - name: AAAA
      description: "année de validité du document"
    - name: Type
      description: "nature du document : Police, Attestation, Echeance"
    - name: Assureur
      description: "nom de la compagnie, forme lisible"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2026_Police_MMA.pdf"
---

## `Assurance locaux et matériel/`

**Rôle :** assurance des locaux professionnels et du matériel. Structure plate.

**Exemple :** `2026_Police_MMA.pdf`
