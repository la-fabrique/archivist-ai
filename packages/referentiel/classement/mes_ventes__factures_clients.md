---
id: mes_ventes.factures_clients
folder_name: "Mes factures clients"
path: "Mes ventes/Mes factures clients"
parent: mes_ventes
dynamic: false
option: core
required: true
description: "Factures émises, classées par mois d'émission"
organization:
  type: chronological
  subfolder_pattern: "AAAA-MM"
file_naming:
  pattern: "[AAAA-MM]_Facture_[Nom client]_[Numero].[ext]"
  fields:
    - name: AAAA-MM
      description: "date d'émission de la facture"
    - name: Nom client
      description: "nom du client, forme lisible"
    - name: Numero
      description: "numéro de la facture tel qu'il apparaît dans le logiciel"
    - name: ext
      description: "extension du fichier (pdf, docx…)"
  example: "2026-03_Facture_Dupont_F2600003.pdf"
---

## `Mes factures clients/`

**Rôle :** factures **émises** par ton entreprise (pas les brouillons : une fois validée et envoyée, le PDF ou l'export comptable vit ici).

**Organisation :** un sous-dossier par mois d'émission utile, format `AAAA-MM` (`Mes factures clients/2026-03/`).

**Format des fichiers :** `[AAAA-MM]_Facture_[Nom client]_[Numero].[ext]`

- `[AAAA-MM]` — date d'émission de la facture
- `[Nom client]` — nom du client, forme lisible
- `[Numero]` — numéro de la facture tel qu'il apparaît dans le logiciel de facturation
- `[ext]` — extension du fichier (`pdf`, `docx`…)

**Exemple :** `2026-03_Facture_Dupont_F2600003.pdf`
