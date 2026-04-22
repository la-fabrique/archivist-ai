---
id: mes_ventes.modeles.contrats
folder_name: "Contrats"
path: "Mes ventes/Mes modèles/Contrats"
parent: mes_ventes.modeles
dynamic: false
option: core
required: true
description: "Modèles de contrat et d'avenant réutilisables"
organization:
  type: flat
file_naming:
  pattern: "modele-contrat_[objet]_v[N].[ext]"
  fields:
    - name: objet
      description: "type de contrat en mots séparés par des tirets (ex. maintenance-annuelle)"
    - name: N
      description: "version du gabarit (1, 2…)"
    - name: ext
      description: "extension du fichier (docx, odt…)"
  example: "modele-contrat_maintenance-annuelle_v2.docx"
---

### `Contrats/` (modèles)

**Rôle :** modèles de contrat et d'avenant à dupliquer. Pas de document signé ici.

**Format des fichiers :** `modele-contrat_[objet]_v[N].[ext]`

- `[objet]` — type de contrat en mots séparés par des tirets (`maintenance-annuelle`, `prestation-conseil`)
- `v[N]` — version du gabarit (`v1`, `v2`…)
- `[ext]` — extension du fichier (`.docx`, `.odt`…)

**Exemple :** `modele-contrat_maintenance-annuelle_v2.docx`
