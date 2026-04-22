---
id: mon_juridique.registres.decisions
folder_name: "Registre des décisions"
path: "Mon juridique/Mes registres/Registre des décisions"
parent: mon_juridique.registres
dynamic: false
option: core
required: true
description: "Versions successives du registre légal des décisions"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_Registre_Decisions.[ext]"
  fields:
    - name: AAAA
      description: "année de l'export ou du scan"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2026_Registre_Decisions.pdf"
---

### `Registre des décisions/`

**Rôle :** exports ou scans annuels du registre des décisions. Structure plate.

**Exemple :** `2026_Registre_Decisions.pdf`
