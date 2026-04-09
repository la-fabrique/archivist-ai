# `Mes ventes/`

> [Plan de classement](__index.md) — [Référentiel](../_index.md) — v0

Relation commerciale sortante : factures clients, modèles de contrat, de devis et d'offre, offres clients, suivi client.


```
Mes ventes/
├── Mes factures clients/
│   ├── [AAAA-MM]/
│   └── ...
├── Mes modèles/                    ← contrat + devis/offre réunis
│   ├── Contrats/
│   └── Devis et offres/
└── Mes clients/
    └── [Nom du client]/
        ├── Contrats/
        ├── Devis/                  ← inclut les propositions commerciales / offres
        └── ...     ← notes, CR, suivi libre
```

**Ce qu'il faut retenir :**

- `Mes factures clients/` contient les factures **émises**, classées dans des **sous-dossiers chronologiques** par mois (`Mes factures clients/2026-03/`). C'est l'emplacement de référence — pratique pour un export groupé (ex. envoi au comptable).
- `Mes modèles/` regroupe les **gabarits réutilisables** : sous-dossier `Contrats/` pour les modèles de contrat, sous-dossier `Devis et offres/` pour les modèles de devis et d'offre commerciale (fusionnés — pour un indep solo, un devis est une offre).
- `Mes clients/` offre une **vue par client** : chaque sous-dossier contient les contrats et devis réels du client ainsi que les documents de suivi (notes, CR…). `Contrats/` et `Devis/` sont imposés ; le reste de l'organisation est libre par client.

---

## `Mes factures clients/`

**Rôle :** factures **émises** par ton entreprise (pas les brouillons : une fois validée et envoyée, le PDF ou l'export comptable vit ici).

**Organisation :** un sous-dossier par mois d'émission utile, format `AAAA-MM` (`Mes factures clients/2026-03/`).

**Format des fichiers:** `[AAAA-MM]_Facture_[Nom client]_[Numero].[ext]`

- `[AAAA-MM]` — date d'émission de la facture
- `[Nom client]` — nom du client, forme lisible
- `[Numero]` — numéro de la facture tel qu'il apparaît dans le logiciel de facturation
- `[ext]` — extension du fichier (`pdf`, `docx`…)

**Exemple :** `2026-03_Facture_Dupont_F2600003.pdf`

---

## `Mes modèles/`

**Rôle :** gabarits réutilisables à dupliquer et adapter. Pas de document signé ni finalisé ici — uniquement les modèles types. Deux sous-dossiers fixes.

```
Mes modèles/
├── Contrats/       ← modèles de contrat et d'avenant
└── Devis et offres/  ← modèles de devis et de propositions commerciales
```

### `Contrats/` (modèles)

**Format des fichiers:** `modele-contrat_[objet]_v[N].[ext]`

- `[objet]` — type de contrat en mots séparés par des tirets (ex. `maintenance-annuelle`, `prestation-conseil`)
- `v[N]` — version du gabarit (`v1`, `v2`…)
- `[ext]` — extension du fichier (`.docx`, `.odt`…)

**Exemple :** `modele-contrat_maintenance-annuelle_v2.docx`

### `Devis et offres/` (modèles)

**Format des fichiers:** `modele-devis_[objet]_v[N].[ext]`

- `[objet]` — type de prestation ou de format (ex. `prestation-conseil`, `formation-react`)
- `v[N]` — version du gabarit (`v1`, `v2`…)
- `[ext]` — extension du fichier (`.docx`, `.odt`…)

**Exemple :** `modele-devis_prestation-conseil_v1.docx`

---

## `Mes clients/`

**Rôle :** **vue par client** regroupant les documents directement liés à la relation avec un client : contrats signés, devis envoyés, offres personnalisées, notes de suivi, comptes-rendus, échanges de référence. Chaque client dispose de son propre sous-dossier.

**Organisation :** un sous-dossier par client, nom en français lisible (`[Nom du client]/`). Les sous-dossiers `Contrats/` et `Devis/` sont imposés dans chaque client ; le reste de l'organisation est libre.

```
Mes clients/
└── [Nom du client]/
    ├── Contrats/    ← contrats et avenants réels du client
    ├── Devis/       ← devis et propositions commerciales envoyés au client
    └── ...          ← notes, CR, suivi (libre)
```

### `Contrats/` (dans chaque client)

**Rôle :** tout **contrat ou avenant** une fois sorti du statut « simple brouillon générique » : négociation, versions partagées, **PDF signé**, scans. Structure plate — pas de sous-dossiers mensuels, le volume par client reste faible.

**Format des fichiers:** `[AAAA-MM]_Contrat_[Nom client]_[Numéro-Révision].[ext]` ou `[AAAA-MM]_Avenant_[Nom client]_[Numéro-Révision].[ext]`

- `[AAAA-MM]` — date d'émission du contrat ou de l'avenant
- `[Nom client]` — nom du client, forme lisible
- `[Numéro-Révision]` — référence libre (numéro de contrat, objet, version… selon ta convention)
- `[ext]` — extension du fichier (`pdf`, `docx`…)

**Exemple :** `2026-04_Contrat_Acme_C2026-01.pdf` (avenant : `2026-04_Avenant_Acme_C2026-02.pdf`)

### `Devis/` (dans chaque client)

**Rôle :** propositions chiffrées et offres commerciales envoyées au client (devis, propositions commerciales, offres personnalisées). Pour un indep solo, un devis IS l'offre — pas de distinction nécessaire. Structure plate — pas de sous-dossiers mensuels, le volume par client reste faible.

**Format des fichiers:** `[AAAA-MM]_Devis_[Nom client]_[Numero].[ext]`

- `[AAAA-MM]` — date d'émission du devis
- `[Nom client]` — nom du client, forme lisible
- `[Numero]` — numéro du devis tel qu'il apparaît dans le logiciel
- `[ext]` — extension du fichier (`pdf`, `docx`…)

**Exemple :** `2026-03_Devis_Martin_D2600001.pdf`
