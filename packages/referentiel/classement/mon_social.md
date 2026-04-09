---
id: mon_social
option: dirigeant-assimile-salarie
required: true
---

# `Mon social/`

> [Plan de classement](__index.md) — [Référentiel](../_index.md) — v0

Gestion du personnel : fiches de paie, DPAE, modèles de contrat de travail, suivi salarié.


```
Mon social/
├── Mes fiches de paie/
│   ├── [AAAA-MM]/
│   └── ...
├── Mes DPAE/
│   └── ...
├── Mes modèles de contrat de travail/
│   └── ...
├── Mes salariés/
│   └── [Nom du salarié]/
│       ├── Contrats/
│       └── ...     ← avenants, courriers, suivi libre
├── Mes déclarations sociales/      ← DSN, bordereaux URSSAF
│   └── [AAAA]/
│       └── [AAAA-MM]/
└── Mes attestations URSSAF/        ← attestations de vigilance, relevés de situation
    └── ...
```

**Ce qu'il faut retenir :**

- `Mes fiches de paie/` contient les bulletins de paie de **tous les salariés**, classés dans des **sous-dossiers chronologiques** par mois (`Mes fiches de paie/2026-03/`). C'est l'emplacement de référence — pratique pour un export groupé (ex. envoi au comptable).
- `Mes DPAE/` contient les déclarations préalables à l'embauche, en structure plate.
- `Mes modèles de contrat de travail/` regroupe les **gabarits réutilisables** à dupliquer et adapter. Pas de documents signés ici — uniquement des modèles types.
- `Mes salariés/` offre une **vue par salarié** : chaque sous-dossier contient les contrats signés, avenants et documents de suivi du salarié. `Contrats/` est imposé ; le reste de l'organisation est libre par salarié.
- `Mes déclarations sociales/` regroupe les DSN mensuelles et les bordereaux de cotisations URSSAF, classés par année puis par mois.
- `Mes attestations URSSAF/` contient les attestations de vigilance (exigées par les clients pour tout contrat > 5 000 €) et les relevés de situation de compte URSSAF.

---

## `Mes fiches de paie/`

**Rôle :** bulletins de paie de tous les salariés (une fois édités, le PDF vit ici).

**Organisation :** un sous-dossier par mois d'émission, format `AAAA-MM` (`Mes fiches de paie/2026-03/`).

**Format des fichiers:** `[AAAA-MM]_Fiche-de-paie_[Nom salarié].[ext]`

- `[AAAA-MM]` — mois de la paie
- `[Nom salarié]` — nom du salarié, forme lisible
- `[ext]` — extension du fichier (`pdf`…)

**Exemple :** `2026-03_Fiche-de-paie_Dupont.pdf`

---

## `Mes DPAE/`

**Rôle :** déclarations préalables à l'embauche transmises à l'URSSAF.

**Organisation :** structure plate — pas de sous-dossiers, le volume reste faible.

**Format des fichiers:** `[AAAA-MM]_DPAE_[Nom salarié].[ext]`

- `[AAAA-MM]` — date de la déclaration
- `[Nom salarié]` — nom du salarié concerné, forme lisible
- `[ext]` — extension du fichier (`pdf`…)

**Exemple :** `2026-04_DPAE_Martin.pdf`

---

## `Mes modèles de contrat de travail/`

**Rôle :** **modèles** de contrat de travail à dupliquer, compléter puis adapter pour chaque salarié. Pas de document signé dans ce dossier — uniquement les gabarits réutilisables (`.docx`, `.odt`…).

**Quand tu sors un contrat pour un salarié** (fichier adapté, puis signé), enregistre-le dans `Mes salariés/[salarié]/Contrats/` — pas dans `Mes modèles de contrat de travail/`. Voir la section **`Mes salariés/`** pour le nommage des fichiers contrat.

**Format des fichiers:** `modele-contrat-travail_[objet]_vN.[ext]`

**Exemple :** `modele-contrat-travail_cdi_v1.docx`

Pas de date « salarié » dans le nom : ce sont des gabarits réutilisables. **vN** est la version du gabarit (`v1`, `v2`…), pas une version « salarié ».

---

## `Mes salariés/`

**Rôle :** **vue par salarié** regroupant les documents directement liés à la relation avec un salarié : contrats signés, avenants, courriers, suivi individuel. Chaque salarié dispose de son propre sous-dossier.

**Organisation :** un sous-dossier par salarié, nom en français lisible (`[Nom du salarié]/`). Le sous-dossier `Contrats/` est imposé dans chaque salarié ; le reste de l'organisation est libre.

```
Mes salariés/
└── [Nom du salarié]/
    ├── Contrats/    ← contrats et avenants signés du salarié
    └── ...          ← courriers, suivi (libre)
```

### `Contrats/` (dans chaque salarié)

**Rôle :** tout **contrat de travail ou avenant** signé : CDI, CDD, avenants de modification. Structure plate — pas de sous-dossiers, le volume par salarié reste faible.

**Format des fichiers:** `[AAAA-MM]_Contrat_[Nom salarié]_[Référence].[ext]` ou `[AAAA-MM]_Avenant_[Nom salarié]_[Référence].[ext]`

- `[AAAA-MM]` — date de signature du contrat ou de l'avenant
- `[Nom salarié]` — nom du salarié, forme lisible
- `[Référence]` — référence libre (type de contrat, numéro… selon ta convention)
- `[ext]` — extension du fichier (`pdf`, `docx`…)

**Exemple :** `2026-01_Contrat_Dupont_CDI.pdf` (avenant : `2026-06_Avenant_Dupont_teletravail.pdf`)

---

## `Mes déclarations sociales/`

**Rôle :** déclarations sociales transmises à l'URSSAF — DSN mensuelles et bordereaux de cotisations. Obligatoire pour tout dirigeant SASU (assimilé salarié) même sans salarié.

**Organisation :** un sous-dossier par année (`[AAAA]/`), puis un sous-dossier par mois (`[AAAA-MM]/`). La DSN est mensuelle ; le volume justifie cette double hiérarchie.

**Format des fichiers:** `[AAAA-MM]_[Type].[ext]`

- `[AAAA-MM]` — mois de la déclaration
- `[Type]` — type de document : `DSN`, `Bordereau-cotisations`
- `[ext]` — extension du fichier (`pdf`…)

**Exemples :** `2026-03_DSN.pdf` / `2026-03_Bordereau-cotisations.pdf`

---

## `Mes attestations URSSAF/`

**Rôle :** attestations de vigilance délivrées par l'URSSAF (exigées par les clients pour tout contrat > 5 000 €) et relevés de situation de compte URSSAF.

**Organisation :** structure plate — volume faible (une attestation par trimestre environ).

**Format des fichiers:** `[AAAA-MM]_[Type].[ext]`

- `[AAAA-MM]` — date de délivrance du document
- `[Type]` — type de document : `Attestation-vigilance`, `Releve-situation`
- `[ext]` — extension du fichier (`pdf`…)

**Exemples :** `2026-03_Attestation-vigilance.pdf` / `2026-03_Releve-situation.pdf`
