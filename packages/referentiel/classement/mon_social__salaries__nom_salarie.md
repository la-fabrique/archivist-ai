---
id: mon_social.salaries.nom_salarie
folder_name: "[Nom du salarié]"
path: "Mon social/Mes salariés/[Nom du salarié]"
parent: mon_social.salaries
dynamic: true
option: dirigeant-assimile-salarie
required: true
description: "Dossier par salarié : nom lisible en français"
organization:
  type: mixed
  fixed_subdirs:
    - mon_social.salaries.nom_salarie.contrats
  free_subdirs: true
---

### `[Nom du salarié]/`

Le sous-dossier `Contrats/` est **imposé**. Le reste est libre (courriers, suivi, avenants non-contractuels).
