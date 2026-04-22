---
id: mes_assurances.rc_pro
folder_name: "RC Pro"
path: "Mes assurances/RC Pro"
parent: mes_assurances
dynamic: false
option: assurances
required: false
description: "Polices, attestations et avis d'échéance RC professionnelle"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_[Type]_[Assureur].[ext]"
  fields:
    - name: AAAA
      description: "année de validité du document"
    - name: Type
      description: "nature du document : Police, Attestation, Echeance, Resiliation"
    - name: Assureur
      description: "nom de la compagnie, forme lisible"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2026_Attestation_Hiscox.pdf"
---

## `RC Pro/`

**Rôle :** responsabilité civile professionnelle — police en vigueur, attestations annuelles, avis d'échéance. Structure plate.

**Exemples :** `2026_Attestation_Hiscox.pdf` / `2026_Police_Hiscox.pdf`
