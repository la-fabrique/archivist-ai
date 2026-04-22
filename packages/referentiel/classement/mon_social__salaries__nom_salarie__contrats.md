---
id: mon_social.salaries.nom_salarie.contrats
folder_name: "Contrats"
path: "Mon social/Mes salariés/[Nom du salarié]/Contrats"
parent: mon_social.salaries.nom_salarie
dynamic: false
option: dirigeant-assimile-salarie
required: true
description: "Contrats de travail et avenants signés du salarié"
organization:
  type: flat
file_naming:
  pattern: "[AAAA-MM]_Contrat_[Nom salarié]_[Référence].[ext]"
  fields:
    - name: AAAA-MM
      description: "date de signature"
    - name: Nom salarié
      description: "nom du salarié, forme lisible"
    - name: Référence
      description: "type de contrat ou référence libre (CDI, CDD…)"
    - name: ext
      description: "extension du fichier (pdf, docx…)"
  example: "2026-01_Contrat_Dupont_CDI.pdf"
---

### `Contrats/` (salarié)

**Rôle :** contrats de travail et avenants signés. Structure plate.

Avenant : `[AAAA-MM]_Avenant_[Nom salarié]_[Référence].[ext]`

**Exemple :** `2026-01_Contrat_Dupont_CDI.pdf`
