# `Mes ventes/`

> [Plan de classement](__index.md) — [Référentiel](../_index.md) — v0

Relation commerciale sortante : factures émises, devis, contrats clients, offres, suivi client.


```
Mes ventes/
├── Factures/
│   ├── 2026-01/
│   └── ...
├── Devis/
│   ├── 2026-01/
│   └── ...
├── Contrats modèles/
│   └── ...
├── Offres/
│   ├── formation_react/
│   └── audit_seo/
└── Mes clients/
    ├── Client Dupont/
    │   ├── Contrats/
    │   └── ...     ← notes, CR, suivi libre
    └── Client Martin/
        ├── Contrats/
        └── ...     ← notes, CR, suivi libre
```

**Ce qu'il faut retenir :**

- Les documents à fort volume (`Factures/`, `Devis/`) vivent dans des **dossiers chronologiques par type** (`Factures/2026-03/`, `Devis/2026-02/`…). Ce sont les emplacements de référence — pratiques pour un export groupé (ex. envoi au comptable).
- `Contrats modèles/` regroupe les **fichiers mères** à dupliquer et adapter (modèles types, clauses fixes) — pas les contrats signés. Une fois adapté et finalisé pour un client, le contrat va dans `Mes clients/[client]/Contrats/`.
- `Mes clients/` offre une **vue par client** : chaque sous-dossier contient les contrats réels du client (peu nombreux) ainsi que les documents de suivi (notes, CR…). Seul `Contrats/` est imposé ; le reste de l'organisation est libre par client.
- `Offres/` contient un dossier par offre ou service — ces documents sont intemporels, pas liés à un mois.

---

## `Factures/`

**Rôle :** factures **émises** par ton entreprise (pas les brouillons définitifs ailleurs : une fois validée et envoyée, le PDF ou l'export comptable vit ici).

**Organisation :** un sous-dossier par mois d'émission utile, format `AAAA-MM` (`Factures/2026-03/`).

**Format des fichiers:** `AAAA-MM_facture_tiers_numero.ext`

**Exemple :** `2026-03_facture_client-dupont_003.pdf`

Le numéro séquentiel (`001`, `002`…) différencie plusieurs factures au même client le même mois. Il correspond idéalement au numéro de facture de ta comptabilité.

---

## `Devis/`

**Rôle :** propositions chiffrées envoyées aux clients (devis, propositions commerciales assimilées), y compris les versions révisées tant qu'elles restent des **devis** (pas encore une facture).

**Organisation :** sous-dossiers mensuels `AAAA-MM`, comme pour les factures.

**Format des fichiers:** `AAAA-MM_devis_tiers_numero.ext`

**Exemple :** `2026-03_devis_client-martin_001.pdf`

Même logique que les factures : date → type `devis` → tiers normalisé → numéro d'ordre. Pour une révision du **même** devis, ajoute un suffixe `-v2`, `-v3`, etc. avant l'extension (ex. `2026-03_devis_client-martin_001-v2.pdf`) sans changer le numéro de base.

---

## `Contrats modèles/`

**Rôle :** **modèles** de contrat ou d'avenant à dupliquer, compléter puis adapter pour chaque client. Pas de document signé ni de PDF « définitif client » dans ce dossier — uniquement les gabarits réutilisables (`.docx`, `.odt`, parfois PDF guide).

**Quand tu sors un contrat ou un avenant pour un client** (fichier adapté, puis signé ou archivé comme référence client), enregistre-le dans `Mes clients/[client]/Contrats/` — pas dans `Contrats modèles/`. Voir la section **`Mes clients/`** pour le nommage des fichiers contrat.

**Format des fichiers:** `modele-contrat_objet_vN.ext`

**Exemple :** `modele-contrat_maintenance_annuelle_v2.docx`

Pas de date « client » dans le nom : ce sont des gabarits réutilisables. Le segment **objet** décrit le type de modèle (souvent plusieurs mots liés par des underscores ou des tirets, ex. `maintenance_annuelle`). **vN** est la version du gabarit (`v1`, `v2`…), pas une version « client ».

---

## `Offres/`

**Rôle :** documents **commerciaux structurants** et réutilisables : plaquettes, descriptifs de formation, grilles prestations, argumentaires — **sans être** une facture ni un devis client nominatif. Un sous-dossier par offre ou ligne de service (`formation_react/`, `audit_seo/`) évite de mélanger les contextes.

**Format des fichiers:** `nom-offre_version.ext`

**Exemple :** `formation-react_v2.pdf`

Documents intemporels : pas de date mensuelle obligatoire dans le nom. La version (`v1`, `v2`) différencie les révisions ; la date de modification du fichier peut compléter si besoin. Le sous-dossier (`formation_react/`, etc.) situe déjà l'offre : le nom de fichier reste court et stable.

---

## `Mes clients/`

**Rôle :** **vue par client** regroupant les documents peu nombreux et directement liés à la relation avec un client : contrats signés, notes de suivi, comptes-rendus, échanges de référence. Chaque client dispose de son propre sous-dossier.

**Organisation :** un sous-dossier par client, nom en français lisible (`Client Dupont/`). Seul le sous-dossier `Contrats/` est imposé dans chaque client ; le reste de l'organisation est libre.

```
Mes clients/
└── Client Dupont/
    ├── Contrats/    ← contrats et avenants réels du client
    └── ...          ← notes, CR, suivi (libre)
```

### `Contrats/` (dans chaque client)

**Rôle :** tout **contrat ou avenant** une fois sorti du statut « simple brouillon générique » : négociation, versions partagées, **PDF signé**, scans. Structure plate — pas de sous-dossiers mensuels, le volume par client reste faible.

**Format des fichiers:** `AAAA-MM-JJ_tiers_contrat_CAAAA-XX.ext` ou `AAAA-MM-JJ_tiers_avenant_CAAAA-XX.ext`

**Exemple :** `2026-04-03_societe-acme_contrat_C2026-01.pdf` (avenant : `2026-04-03_societe-acme_avenant_C2026-02.pdf`)

`AAAA-MM-JJ` est en général la **date de signature**. Le **tiers** est le client en minuscules, sans accents ni espaces, mots liés par des tirets (`societe-acme`). **`CAAAA-XX`** est une référence maison : `C` + année de numérotation + numéro d'ordre sur deux chiffres (`C2026-01`, …).

**Alternative :** `AAAA-MM_contrat_tiers_objet.ext` — ex. `2026-03_contrat_client-dupont_maintenance.pdf` — si tu préfères un **objet** lisible à la place du code `CAAAA-XX`. Ne pas mélanger les deux conventions sans les documenter.
