---
id: mon_social.fiches_de_paie
folder_name: "Mes fiches de paie"
path: "Mon social/Mes fiches de paie"
parent: mon_social
dynamic: false
option: dirigeant-assimile-salarie
required: true
description: "Bulletins de paie de tous les salariés, classés par mois"
organization:
  type: chronological
  subfolder_pattern: "AAAA-MM"
file_naming:
  pattern: "[AAAA-MM]_Fiche-de-paie_[Nom salarié].[ext]"
  fields:
    - name: AAAA-MM
      description: "mois de la paie"
    - name: Nom salarié
      description: "nom du salarié, forme lisible"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2026-03_Fiche-de-paie_Dupont.pdf"
---

## `Mes fiches de paie/`

**Rôle :** bulletins de paie de tous les salariés. Un sous-dossier par mois d'émission, format `AAAA-MM`.

**Format des fichiers :** `[AAAA-MM]_Fiche-de-paie_[Nom salarié].[ext]`

**Exemple :** `2026-03_Fiche-de-paie_Dupont.pdf`
