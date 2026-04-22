---
id: mon_juridique.marques_licences
folder_name: "Mes marques et licences"
path: "Mon juridique/Mes marques et licences"
parent: mon_juridique
dynamic: false
option: core
required: false
description: "Dépôts de marque INPI, licences logicielles, cessions de droits d'auteur (optionnel)"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_[Type]_[Objet].[ext]"
  fields:
    - name: AAAA
      description: "année du dépôt ou de la signature"
    - name: Type
      description: "type de document : Depot-marque, Licence, Cession-droits, Certificat"
    - name: Objet
      description: "nom de la marque, du logiciel ou de l'œuvre, forme lisible"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "2026_Depot-marque_NomDeMarque.pdf"
---

## `Mes marques et licences/`

> **Dossier optionnel** — utile pour les indépendants du numérique, du créatif ou de la tech.

**Rôle :** dépôts de marque INPI, licences logicielles, cessions de droits d'auteur. Structure plate.

**Exemples :** `2026_Depot-marque_NomDeMarque.pdf` / `2026_Licence_Figma.pdf`
