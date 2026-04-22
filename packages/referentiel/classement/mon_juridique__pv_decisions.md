---
id: mon_juridique.pv_decisions
folder_name: "Mes PV et décisions"
path: "Mon juridique/Mes PV et décisions"
parent: mon_juridique
dynamic: false
option: core
required: true
description: "PV d'AG et décisions de l'associé unique (SASU)"
organization:
  type: flat
file_naming:
  pattern: "[AAAA]_[Type]_[Objet].[ext]"
  fields:
    - name: AAAA
      description: "année de la décision ou de l'assemblée"
    - name: Type
      description: "PV-AG ou Decision-AU"
    - name: Objet
      description: "objet principal (approbation-comptes, dividendes, nomination-gerant…)"
    - name: ext
      description: "extension du fichier (pdf, docx…)"
  example: "2026_PV-AG_approbation-comptes.pdf"
---

## `Mes PV et décisions/`

**Rôle :** PV d'assemblée générale et décisions de l'associé unique (SASU). Structure plate.

**Exemples :** `2026_PV-AG_approbation-comptes.pdf` / `2026_Decision-AU_dividendes.pdf`
