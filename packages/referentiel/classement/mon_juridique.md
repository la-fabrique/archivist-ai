---
id: mon_juridique
option: core
required: true
---

# `Mon juridique/`

> [Plan de classement](__index.md) — [Référentiel](../_index.md) — v0

Entité juridique : statuts, K-bis, procès-verbaux d'assemblée générale.


```
Mon juridique/
├── Mes statuts/
│   └── ...
├── Mes K-bis/
│   └── ...
├── Mes PV et décisions/            ← PV d'AG + décisions de l'associé unique (SASU)
│   └── ...
├── Mes registres/
│   ├── Registre des mouvements de titres/
│   └── Registre des décisions/
├── Mes baux et domiciliation/
│   └── ...
├── Mes CGV et mentions légales/
│   └── ...
└── Mes marques et licences/        ← optionnel : indépendants numérique/créatif
    └── ...
```

**Ce qu'il faut retenir :**

- `Mes statuts/` contient les statuts constitutifs et leurs mises à jour successives.
- `Mes K-bis/` contient les extraits K-bis demandés ou reçus.
- `Mes PV et décisions/` contient les PV d'assemblée générale ET les décisions de l'associé unique (SASU). En SASU, les décisions importantes remplacent les délibérations collectives.
- `Mes registres/` contient les registres obligatoires pour une SASU : mouvements de titres et registre des décisions.
- `Mes baux et domiciliation/` contient les baux commerciaux et contrats de domiciliation.
- `Mes CGV et mentions légales/` contient les conditions générales de vente, CGU, mentions légales et politique de confidentialité.
- `Mes marques et licences/` (optionnel) contient les dépôts de marque INPI, licences logicielles et cessions de droits d'auteur.

---

## `Mes statuts/`

**Rôle :** statuts constitutifs de la société et leurs mises à jour (modification d'objet social, changement de siège, augmentation de capital…).

**Organisation :** structure plate — pas de sous-dossiers, le volume reste faible.

**Format des fichiers:** `[AAAA]_Statuts_[Objet].[ext]`

- `[AAAA]` — année de signature ou d'enregistrement
- `[Objet]` — nature du document (constitution, modification objet social…)
- `[ext]` — extension du fichier (`pdf`, `docx`…)

**Exemple :** `2026_Statuts_constitution.pdf`

---

## `Mes K-bis/`

**Rôle :** extraits K-bis (ou équivalent pour les entreprises individuelles) demandés ou reçus, servant de justificatif d'immatriculation.

**Organisation :** structure plate — pas de sous-dossiers, le volume reste faible.

**Format des fichiers:** `[AAAA]_Kbis.[ext]`

- `[AAAA]` — année d'émission du K-bis
- `[ext]` — extension du fichier (`pdf`…)

**Exemple :** `2026_Kbis.pdf`

---

## `Mes PV et décisions/`

**Rôle :** procès-verbaux d'assemblée générale (AGO/AGE) et décisions de l'associé unique (SASU). En SASU, les décisions importantes de l'associé unique ont la même valeur juridique qu'un PV d'AG.

**Organisation :** structure plate — pas de sous-dossiers, le volume reste faible.

**Format des fichiers:** `[AAAA]_[Type]_[Objet].[ext]`

- `[AAAA]` — année de la décision ou de l'assemblée
- `[Type]` — `PV-AG` (assemblée générale) ou `Decision-AU` (décision associé unique)
- `[Objet]` — objet principal (approbation-comptes, dividendes, nomination-gerant…)
- `[ext]` — extension du fichier (`pdf`, `docx`…)

**Exemples :** `2026_PV-AG_approbation-comptes.pdf` / `2026_Decision-AU_dividendes.pdf`

---

## `Mes registres/`

**Rôle :** registres obligatoires pour une SASU — le registre des mouvements de titres et le registre des décisions sont légalement requis et doivent être tenus à jour.

**Organisation :** deux sous-dossiers fixes. Chaque registre est un document mis à jour en continu ; on conserve les versions successives (PDF exporté ou scan du registre papier).

```
Mes registres/
├── Registre des mouvements de titres/
└── Registre des décisions/
```

**Format des fichiers:** `[AAAA]_Registre_[Type].[ext]`

- `[AAAA]` — année de l'export ou du scan
- `[Type]` — `Mouvements-titres`, `Decisions`
- `[ext]` — extension du fichier (`pdf`…)

**Exemple :** `2026_Registre_Decisions.pdf`

---

## `Mes baux et domiciliation/`

**Rôle :** baux commerciaux, contrats de sous-location, contrats de domiciliation. Inclut les avenants et les quittances de loyer si conservées.

**Organisation :** structure plate — volume faible.

**Format des fichiers:** `[AAAA]_[Type]_[Bailleur].[ext]`

- `[AAAA]` — année de signature du contrat
- `[Type]` — type de document : `Bail-commercial`, `Domiciliation`, `Avenant`, `Quittance`
- `[Bailleur]` — nom du bailleur ou de la société de domiciliation, forme lisible
- `[ext]` — extension du fichier (`pdf`…)

**Exemple :** `2026_Domiciliation_Regus.pdf`

---

## `Mes CGV et mentions légales/`

**Rôle :** conditions générales de vente (CGV), conditions générales d'utilisation (CGU), mentions légales du site web, politique de confidentialité. Documents contractuels qui régissent la relation avec les clients et les obligations légales d'affichage.

**Organisation :** structure plate — volume faible, une version par année.

**Format des fichiers:** `[AAAA]_[Type]_v[N].[ext]`

- `[AAAA]` — année de la version
- `[Type]` — type de document : `CGV`, `CGU`, `Mentions-legales`, `Politique-confidentialite`
- `v[N]` — numéro de version (`v1`, `v2`…)
- `[ext]` — extension du fichier (`pdf`…)

**Exemple :** `2026_CGV_v2.pdf`

---

## `Mes marques et licences/`

> **Dossier optionnel** — utile pour les indépendants du numérique, du créatif ou de la tech.

**Rôle :** dépôts de marque INPI, certificats d'enregistrement, licences logicielles (SaaS, perpétuelles), contrats de cession ou de licence de droits d'auteur.

**Organisation :** structure plate — volume variable selon l'activité.

**Format des fichiers:** `[AAAA]_[Type]_[Objet].[ext]`

- `[AAAA]` — année du dépôt, de la signature ou du début de validité
- `[Type]` — type de document : `Depot-marque`, `Licence`, `Cession-droits`, `Certificat`
- `[Objet]` — nom de la marque, du logiciel ou de l'œuvre concerné, forme lisible
- `[ext]` — extension du fichier (`pdf`…)

**Exemples :** `2026_Depot-marque_NomDeMarque.pdf` / `2026_Licence_Figma.pdf`
