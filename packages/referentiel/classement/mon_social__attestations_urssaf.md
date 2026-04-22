---
id: mon_social.attestations_urssaf
folder_name: "Mes attestations URSSAF"
path: "Mon social/Mes attestations URSSAF"
parent: mon_social
dynamic: false
option: dirigeant-assimile-salarie
required: true
description: "Attestations de vigilance et relevés de situation URSSAF"
organization:
  type: flat
file_naming:
  pattern: "[AAAA-MM]_[Type].[ext]"
  fields:
    - name: AAAA-MM
      description: "date de délivrance du document"
    - name: Type
      description: "type de document : Attestation-vigilance, Releve-situation"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2026-03_Attestation-vigilance.pdf"
---

## `Mes attestations URSSAF/`

**Rôle :** attestations de vigilance (exigées pour tout contrat > 5 000 €) et relevés de situation. Structure plate.

**Exemples :** `2026-03_Attestation-vigilance.pdf` / `2026-03_Releve-situation.pdf`
