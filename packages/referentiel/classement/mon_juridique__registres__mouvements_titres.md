---
id: mon_juridique.registres.mouvements_titres
folder_name: "Registre des mouvements de titres"
path: "Mon juridique/Mes registres/Registre des mouvements de titres"
parent: mon_juridique.registres
dynamic: false
option: core
required: true
description: "Versions successives du registre légal des mouvements de titres"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_Registre_Mouvements-titres.[ext]"
  fields:
    - name: AAAA
      description: "année de l'export ou du scan"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2026_Registre_Mouvements-titres.pdf"
---

### `Registre des mouvements de titres/`

**Rôle :** exports ou scans annuels du registre des mouvements de titres. Structure plate.

**Exemple :** `2026_Registre_Mouvements-titres.pdf`
