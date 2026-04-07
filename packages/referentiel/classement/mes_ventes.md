# `Mes ventes/`

> [Plan de classement](__index.md) — [Référentiel](../_index.md) — v0

Relation commerciale sortante : factures clients, modèles de contrat, de devis et d'offre, offres clients, suivi client.


```
Mes ventes/
├── Mes factures clients/
│   ├── 2026-01/
│   └── ...
├── Mes modèles de contrat/
│   └── ...
├── Mes modèles de devis/
│   └── ...
├── Mes modèles d'offre/
│   └── ...
└── Mes clients/
    └── [Nom du client]/
        ├── Contrats/
        ├── Devis/
        ├── Offres/
        └── ...     ← notes, CR, suivi libre
```

**Ce qu'il faut retenir :**

- `Mes factures clients/` contient les factures **émises**, classées dans des **sous-dossiers chronologiques** par mois (`Mes factures clients/2026-03/`). C'est l'emplacement de référence — pratique pour un export groupé (ex. envoi au comptable).
- `Mes modèles de contrat/`, `Mes modèles de devis/` et `Mes modèles d'offre/` regroupent les **gabarits réutilisables** à dupliquer et adapter. Pas de documents signés ni finalisés ici — uniquement des modèles types.
- `Mes clients/` offre une **vue par client** : chaque sous-dossier contient les contrats, devis et offres réels du client ainsi que les documents de suivi (notes, CR…). `Contrats/`, `Devis/` et `Offres/` sont imposés ; le reste de l'organisation est libre par client.

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

## `Mes modèles de contrat/`

**Rôle :** **modèles** de contrat ou d'avenant à dupliquer, compléter puis adapter pour chaque client. Pas de document signé ni de PDF « définitif client » dans ce dossier — uniquement les gabarits réutilisables (`.docx`, `.odt`, parfois PDF guide).

**Quand tu sors un contrat pour un client** (fichier adapté, puis signé ou archivé comme référence client), enregistre-le dans `Mes clients/[client]/Contrats/` — pas dans `Mes modèles de contrat/`. Voir la section **`Mes clients/`** pour le nommage des fichiers contrat.

**Format des fichiers:** `modele-contrat_objet_vN.ext`

**Exemple :** `modele-contrat_maintenance_annuelle_v2.docx`

Pas de date « client » dans le nom : ce sont des gabarits réutilisables. Le segment **objet** décrit le type de modèle (souvent plusieurs mots liés par des underscores ou des tirets, ex. `maintenance_annuelle`). **vN** est la version du gabarit (`v1`, `v2`…), pas une version « client ».

---

## `Mes modèles de devis/`

**Rôle :** **modèles** de devis à dupliquer, compléter puis adapter pour chaque client. Pas de devis finalisé ni envoyé dans ce dossier — uniquement les gabarits réutilisables (`.docx`, `.odt`, parfois PDF guide).

**Quand tu finalises un devis pour un client** (fichier adapté et envoyé), enregistre-le dans `Mes clients/[client]/Devis/` — pas dans `Mes modèles de devis/`. Voir la section **`Mes clients/`** pour le nommage des fichiers devis.

**Format des fichiers:** `modele-devis_objet_vN.ext`

**Exemple :** `modele-devis_prestation_conseil_v1.docx`

Même logique que les modèles de contrat : pas de date client, version du gabarit uniquement.

---

## `Mes modèles d'offre/`

**Rôle :** **modèles** d'offre commerciale à dupliquer, compléter puis adapter pour chaque client. Pas d'offre finalisée ni envoyée dans ce dossier — uniquement les gabarits réutilisables : plaquettes types, descriptifs de formation, grilles prestations, argumentaires génériques (`.docx`, `.odt`, parfois PDF guide).

**Quand tu finalises une offre pour un client** (fichier adapté et envoyé), enregistre-le dans `Mes clients/[client]/Offres/` — pas dans `Mes modèles d'offre/`. Voir la section **`Mes clients/`** pour le nommage des fichiers offre.

**Format des fichiers:** `modele-offre_objet_vN.ext`

**Exemple :** `modele-offre_formation-react_v2.docx`

Même logique que les modèles de contrat et de devis : pas de date client, version du gabarit uniquement.

---

## `Mes clients/`

**Rôle :** **vue par client** regroupant les documents directement liés à la relation avec un client : contrats signés, devis envoyés, offres personnalisées, notes de suivi, comptes-rendus, échanges de référence. Chaque client dispose de son propre sous-dossier.

**Organisation :** un sous-dossier par client, nom en français lisible (`[Nom du client]/`). Les sous-dossiers `Contrats/`, `Devis/` et `Offres/` sont imposés dans chaque client ; le reste de l'organisation est libre.

```
Mes clients/
└── [Nom du client]/
    ├── Contrats/    ← contrats et avenants réels du client
    ├── Devis/       ← devis envoyés au client
    ├── Offres/      ← offres personnalisées envoyées au client
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

**Rôle :** propositions chiffrées envoyées au client (devis, propositions commerciales assimilées), y compris les versions révisées tant qu'elles restent des **devis** (pas encore une facture). Structure plate — pas de sous-dossiers mensuels, le volume par client reste faible.

**Format des fichiers:** `[AAAA-MM]_Devis_[Nom client]_[Numero].[ext]`

- `[AAAA-MM]` — date d'émission du devis
- `[Nom client]` — nom du client, forme lisible
- `[Numero]` — numéro du devis tel qu'il apparaît dans le logiciel
- `[ext]` — extension du fichier (`pdf`, `docx`…)

**Exemple :** `2026-03_Devis_Martin_D2600001.pdf`

### `Offres/` (dans chaque client)

**Rôle :** offres commerciales **personnalisées** envoyées au client (propositions adaptées à partir des modèles d'offre). Structure plate — pas de sous-dossiers mensuels, le volume par client reste faible.

**Format des fichiers:** `[AAAA-MM]_Offre_[Nom client]_[Numero].[ext]`

- `[AAAA-MM]` — date d'émission de l'offre
- `[Nom client]` — nom du client, forme lisible
- `[Numero]` — numéro de l'offre tel qu'il apparaît dans le logiciel
- `[ext]` — extension du fichier (`pdf`, `docx`…)

**Exemple :** `2026-03_Offre_Dupont_O2600001.pdf`
