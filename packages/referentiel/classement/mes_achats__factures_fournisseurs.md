---
id: mes_achats.factures_fournisseurs
folder_name: "Mes factures fournisseurs"
path: "Mes achats/Mes factures fournisseurs"
parent: mes_achats
dynamic: false
option: core
required: true
description: "Factures reçues, classées par mois de réception"
organization:
  type: chronological
  subfolder_pattern: "AAAA-MM"
file_naming:
  pattern: "[AAAA-MM]_Facture_[Nom fournisseur]_[Numero].[ext]"
  fields:
    - name: AAAA-MM
      description: "date d'émission de la facture"
    - name: Nom fournisseur
      description: "nom du fournisseur, forme lisible"
    - name: Numero
      description: "numéro de la facture tel qu'il apparaît sur le document"
    - name: ext
      description: "extension du fichier (pdf, docx…)"
  example: "2026-03_Facture_OVH_F2600042.pdf"
---

## `Mes factures fournisseurs/`

**Rôle :** factures **reçues** par ton entreprise. Un sous-dossier par mois de réception, format `AAAA-MM`.

**Format des fichiers :** `[AAAA-MM]_Facture_[Nom fournisseur]_[Numero].[ext]`

**Exemple :** `2026-03_Facture_OVH_F2600042.pdf`
