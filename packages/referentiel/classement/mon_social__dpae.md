---
id: mon_social.dpae
folder_name: "Mes DPAE"
path: "Mon social/Mes DPAE"
parent: mon_social
dynamic: false
option: dirigeant-assimile-salarie
required: true
description: "Déclarations préalables à l'embauche, structure plate"
organization:
  type: flat
file_naming:
  pattern: "[AAAA-MM]_DPAE_[Nom salarié].[ext]"
  fields:
    - name: AAAA-MM
      description: "date de la déclaration"
    - name: Nom salarié
      description: "nom du salarié concerné, forme lisible"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2026-04_DPAE_Martin.pdf"
---

## `Mes DPAE/`

**Rôle :** déclarations préalables à l'embauche transmises à l'URSSAF. Structure plate.

**Format des fichiers :** `[AAAA-MM]_DPAE_[Nom salarié].[ext]`

**Exemple :** `2026-04_DPAE_Martin.pdf`
