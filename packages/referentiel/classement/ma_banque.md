# `Ma banque/`

> [Plan de classement](__index.md) — [Référentiel](../_index.md) — v0

Trésorerie : relevés bancaires et RIB.


```
Ma banque/
├── Mes relevés bancaires/
│   └── [Nom banque]/               ← un sous-dossier par établissement
│       └── [AAAA-MM]/
└── Mes RIB/
    └── ...
```

**Ce qu'il faut retenir :**

- `Mes relevés bancaires/` contient les relevés de compte reçus de ta banque, organisés par établissement puis par mois. Si tu n'as qu'un seul compte, crée un seul sous-dossier `[Nom banque]/`.
- `Mes RIB/` contient les RIB actifs de chaque compte bancaire — demandés en permanence par les clients, fournisseurs et administrations.

---

## `Mes relevés bancaires/`

**Rôle :** relevés de compte bancaire reçus (PDF ou export depuis l'espace en ligne).

**Organisation :** un sous-dossier par établissement bancaire (`[Nom banque]/`), puis un sous-dossier par mois (`[AAAA-MM]/`). Si tu n'as qu'un seul compte, l'organisation reste la même — un seul sous-dossier banque.

**Format des fichiers:** `[AAAA-MM]_Releve_[Nom-banque]_[Numero].[ext]`

- `[AAAA-MM]` — mois couvert par le relevé
- `[Nom-banque]` — nom de la banque, forme lisible (ex. `Credit-Mutuel`, `BNP`, `Qonto`)
- `[Numero]` — numéro du relevé tel qu'il apparaît sur le document
- `[ext]` — extension du fichier (`pdf`, `csv`…)

**Exemple :** `2026-03_Releve_Credit-Mutuel_003.pdf`

---

## `Mes RIB/`

**Rôle :** relevés d'identité bancaire (RIB) de chaque compte professionnel actif. Documents demandés en permanence — clients, fournisseurs, URSSAF, administrations.

**Organisation :** structure plate — un fichier par compte bancaire. Le RIB ne change que si le compte change ; pas de sous-dossiers chronologiques.

**Format des fichiers:** `RIB_[Nom-banque]_[Compte].[ext]`

- `[Nom-banque]` — nom de la banque, forme lisible
- `[Compte]` — type ou libellé du compte si plusieurs comptes chez la même banque (`Courant`, `Epargne-pro`…) — omettre si un seul compte
- `[ext]` — extension du fichier (`pdf`…)

**Exemples :** `RIB_Credit-Mutuel.pdf` / `RIB_Qonto_Courant.pdf`
