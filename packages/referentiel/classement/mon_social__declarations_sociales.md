---
id: mon_social.declarations_sociales
folder_name: "Mes déclarations sociales"
path: "Mon social/Mes déclarations sociales"
parent: mon_social
dynamic: false
option: dirigeant-assimile-salarie
required: true
description: "DSN mensuelles et bordereaux URSSAF, classés par année puis mois"
organization:
  type: chronological
  subfolder_pattern: "AAAA/AAAA-MM"
file_naming:
  pattern: "[AAAA-MM]_[Type].[ext]"
  fields:
    - name: AAAA-MM
      description: "mois de la déclaration"
    - name: Type
      description: "type de document : DSN, Bordereau-cotisations"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2026-03_DSN.pdf"
---

## `Mes déclarations sociales/`

**Rôle :** DSN mensuelles et bordereaux de cotisations URSSAF. Obligatoire pour tout dirigeant SASU.

**Organisation :** un sous-dossier par année (`[AAAA]/`), puis par mois (`[AAAA-MM]/`).

**Exemples :** `2026-03_DSN.pdf` / `2026-03_Bordereau-cotisations.pdf`
