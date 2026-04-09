---
id: mes_assurances
option: assurances
required: false
---

# `Mes assurances/`

> [Plan de classement](__index.md) — [Référentiel](../_index.md) — v0

Couvertures assurantielles : RC professionnelle, mutuelle et prévoyance, assurance locaux et matériel.


```
Mes assurances/
├── RC Pro/
│   └── ...
├── Mutuelle et prévoyance/
│   └── ...
└── Assurance locaux et matériel/
    └── ...
```

**Ce qu'il faut retenir :**

- `RC Pro/` contient les polices, attestations et avis d'échéance de la responsabilité civile professionnelle.
- `Mutuelle et prévoyance/` contient les polices et attestations de mutuelle santé et de prévoyance (obligatoire avec salarié).
- `Assurance locaux et matériel/` contient les polices et attestations d'assurance des locaux professionnels et du matériel.

---

## `RC Pro/`

**Rôle :** responsabilité civile professionnelle — police en vigueur, attestations annuelles, avis d'échéance, courriers compagnie.

**Organisation :** structure plate — volume faible, un ou deux documents par an.

**Format des fichiers:** `[AAAA]_[Type]_[Assureur].[ext]`

- `[AAAA]` — année de validité du document
- `[Type]` — nature du document : `Police`, `Attestation`, `Echeance`, `Resiliation`
- `[Assureur]` — nom de la compagnie d'assurance, forme lisible
- `[ext]` — extension du fichier (`pdf`…)

**Exemples :** `2026_Attestation_Hiscox.pdf` / `2026_Police_Hiscox.pdf`

---

## `Mutuelle et prévoyance/`

**Rôle :** mutuelle santé et prévoyance — police, attestations d'affiliation, relevés de remboursements si conservés.

**Organisation :** structure plate — volume faible.

**Format des fichiers:** `[AAAA]_[Type]_[Assureur].[ext]`

- `[AAAA]` — année de validité du document
- `[Type]` — nature du document : `Police`, `Attestation`, `Remboursement`
- `[Assureur]` — nom de la compagnie, forme lisible
- `[ext]` — extension du fichier (`pdf`…)

**Exemple :** `2026_Attestation_AlanSante.pdf`

---

## `Assurance locaux et matériel/`

**Rôle :** assurance des locaux professionnels (bureau, atelier) et du matériel (ordinateurs, outillage).

**Organisation :** structure plate — volume faible.

**Format des fichiers:** `[AAAA]_[Type]_[Assureur].[ext]`

- `[AAAA]` — année de validité du document
- `[Type]` — nature du document : `Police`, `Attestation`, `Echeance`
- `[Assureur]` — nom de la compagnie, forme lisible
- `[ext]` — extension du fichier (`pdf`…)

**Exemple :** `2026_Police_MMA.pdf`
