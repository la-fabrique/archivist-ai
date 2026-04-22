---
id: mes_assurances.mutuelle_prevoyance
folder_name: "Mutuelle et prévoyance"
path: "Mes assurances/Mutuelle et prévoyance"
parent: mes_assurances
dynamic: false
option: assurances
required: false
description: "Polices et attestations mutuelle santé et prévoyance"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_[Type]_[Assureur].[ext]"
  fields:
    - name: AAAA
      description: "année de validité du document"
    - name: Type
      description: "nature du document : Police, Attestation, Remboursement"
    - name: Assureur
      description: "nom de la compagnie, forme lisible"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2026_Attestation_AlanSante.pdf"
---

## `Mutuelle et prévoyance/`

**Rôle :** mutuelle santé et prévoyance — police, attestations d'affiliation. Structure plate.

**Exemple :** `2026_Attestation_AlanSante.pdf`
