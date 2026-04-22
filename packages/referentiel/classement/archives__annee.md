---
id: archives.annee
folder_name: "[AAAA]"
path: "Archives/[AAAA]"
parent: archives
dynamic: true
option: core
required: true
description: "Dossier d'archive pour une année close : fichiers compressés + manifest"
organization:
  type: flat
file_naming:
  pattern: "[dossier-racine]_[AAAA].[ext]"
  fields:
    - name: dossier-racine
      description: "nom du dossier racine archivé, en minuscules avec tirets (mes_ventes, ma_banque…)"
    - name: AAAA
      description: "année archivée"
    - name: ext
      description: "format de compression (zip, tar.gz…)"
  example: "mes_ventes_2024.zip"
special_files:
  - name: manifest.md
    description: "liste des fichiers archivés et leur état (voir regles-archivage.md)"
---

### `[AAAA]/`

**Rôle :** dossier d'archive pour une année close. Contient un fichier compressé par dossier racine et un `manifest.md`.

**Exemple :** `Archives/2024/mes_ventes_2024.zip`
