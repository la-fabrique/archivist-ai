---
id: mon_social.modeles_contrat_travail
folder_name: "Mes modèles de contrat de travail"
path: "Mon social/Mes modèles de contrat de travail"
parent: mon_social
dynamic: false
option: dirigeant-assimile-salarie
required: true
description: "Gabarits de contrat de travail réutilisables (pas de documents signés)"
organization:
  type: flat
file_naming:
  pattern: "modele-contrat-travail_[objet]_v[N].[ext]"
  fields:
    - name: objet
      description: "type de contrat (cdi, cdd, alternance…)"
    - name: N
      description: "version du gabarit (1, 2…)"
    - name: ext
      description: "extension du fichier (docx, odt…)"
  example: "modele-contrat-travail_cdi_v1.docx"
---

## `Mes modèles de contrat de travail/`

**Rôle :** gabarits de contrat de travail à dupliquer et compléter. Pas de document signé ici. Les contrats signés vont dans `Mes salariés/[salarié]/Contrats/`.

**Format des fichiers :** `modele-contrat-travail_[objet]_vN.[ext]`

**Exemple :** `modele-contrat-travail_cdi_v1.docx`
