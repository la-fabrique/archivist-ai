---
id: ma_banque.releves_bancaires.nom_banque
folder_name: "[Nom banque]"
path: "Ma banque/Mes relevés bancaires/[Nom banque]"
parent: ma_banque.releves_bancaires
dynamic: true
option: core
required: true
description: "Dossier par établissement bancaire, contenant les relevés mensuels"
organization:
  type: chronological
  subfolder_pattern: "AAAA-MM"
file_naming:
  pattern: "[AAAA-MM]_Releve_[Nom-banque]_[Numero].[ext]"
  fields:
    - name: AAAA-MM
      description: "mois couvert par le relevé"
    - name: Nom-banque
      description: "nom de la banque, forme lisible (Credit-Mutuel, BNP, Qonto…)"
    - name: Numero
      description: "numéro du relevé tel qu'il apparaît sur le document"
    - name: ext
      description: "extension du fichier (pdf, csv…)"
  example: "2026-03_Releve_Credit-Mutuel_003.pdf"
---

### `[Nom banque]/`

**Rôle :** relevés mensuels d'un établissement bancaire. Sous-dossiers chronologiques `[AAAA-MM]/`.

**Exemple :** `2026-03_Releve_Credit-Mutuel_003.pdf`
