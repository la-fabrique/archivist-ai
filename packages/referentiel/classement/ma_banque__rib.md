---
id: ma_banque.rib
folder_name: "Mes RIB"
path: "Ma banque/Mes RIB"
parent: ma_banque
dynamic: false
option: core
required: true
description: "RIB des comptes bancaires professionnels actifs, structure plate"
organization:
  type: flat
file_naming:
  pattern: "RIB_[Nom-banque]_[Compte].[ext]"
  fields:
    - name: Nom-banque
      description: "nom de la banque, forme lisible"
    - name: Compte
      description: "type ou libellé du compte si plusieurs chez la même banque — omettre si unique"
    - name: ext
      description: "extension du fichier (pdf…)"
  example: "RIB_Credit-Mutuel.pdf"
---

## `Mes RIB/`

**Rôle :** relevés d'identité bancaire des comptes professionnels actifs. Structure plate — un fichier par compte.

**Exemples :** `RIB_Credit-Mutuel.pdf` / `RIB_Qonto_Courant.pdf`
