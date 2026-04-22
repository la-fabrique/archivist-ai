---
id: mon_juridique.cgv_mentions_legales
folder_name: "Mes CGV et mentions légales"
path: "Mon juridique/Mes CGV et mentions légales"
parent: mon_juridique
dynamic: false
option: core
required: true
description: "CGV, CGU, mentions légales, politique de confidentialité"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_[Type]_v[N].[ext]"
  fields:
    - name: AAAA
      description: "année de la version"
    - name: Type
      description: "type de document : CGV, CGU, Mentions-legales, Politique-confidentialite"
    - name: N
      description: "numéro de version (1, 2…)"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2026_CGV_v2.pdf"
---

## `Mes CGV et mentions légales/`

**Rôle :** conditions générales de vente, CGU, mentions légales du site web, politique de confidentialité. Structure plate.

**Exemple :** `2026_CGV_v2.pdf`
