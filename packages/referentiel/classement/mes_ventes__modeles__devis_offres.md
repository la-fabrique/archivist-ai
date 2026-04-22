---
id: mes_ventes.modeles.devis_offres
folder_name: "Devis et offres"
path: "Mes ventes/Mes modèles/Devis et offres"
parent: mes_ventes.modeles
dynamic: false
option: core
required: true
description: "Modèles de devis et de propositions commerciales réutilisables"
organization:
  type: flat
file_naming:
  pattern: "modele-devis_[objet]_v[N].[ext]"
  fields:
    - name: objet
      description: "type de prestation ou de format (ex. prestation-conseil)"
    - name: N
      description: "version du gabarit (1, 2…)"
    - name: ext
      description: "extension du fichier (docx, odt…)"
  example: "modele-devis_prestation-conseil_v1.docx"
---

### `Devis et offres/` (modèles)

**Rôle :** modèles de devis et d'offre commerciale à dupliquer. Pour un indép solo, un devis IS l'offre.

**Format des fichiers :** `modele-devis_[objet]_v[N].[ext]`

- `[objet]` — type de prestation (`prestation-conseil`, `formation-react`)
- `v[N]` — version du gabarit (`v1`, `v2`…)
- `[ext]` — extension du fichier (`.docx`, `.odt`…)

**Exemple :** `modele-devis_prestation-conseil_v1.docx`
