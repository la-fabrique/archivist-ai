# `Mes ventes/`

> [Plan de classement](__index.md) — [Référentiel](../_index.md) — v0

Relation commerciale sortante : factures émises, devis, contrats clients, offres, suivi client.


```
Mes ventes/
├── factures/
│   ├── 2026-01/
│   └── ...
├── devis/
│   ├── 2026-01/
│   └── ...
├── contrats_modeles/
│   └── ...
├── contrats/
│   ├── 2026-01/
│   └── ...
├── offres/
│   ├── formation_react/
│   └── audit_seo/
└── gestion/
    ├── Client dupont/    ← raccourcis uniquement
    └── Client martin/    ← raccourcis uniquement
```

**Ce qu'il faut retenir :**

- Les documents vivent dans des **dossiers chronologiques par type** (`factures/2026-03/`, `devis/2026-02/`, `contrats/2026-01/`…). Ce sont les emplacements de référence.
- `contrats_modeles/` regroupe les **fichiers mères** à dupliquer et adapter (modèles types, clauses fixes) — pas les contrats signés chez le client. Les versions **client**, une fois figées ou signées, vont dans `contrats/AAAA-MM/` avec la convention de nommage décrite ci‑dessous.
- Les sous-dossiers mensuels (`AAAA-MM`) évitent d'avoir des centaines de fichiers au même niveau. En fin d'année, les factures de janvier et de décembre ne se côtoient pas.
- `offres/` contient un dossier par offre ou service — ces documents sont intemporels, pas liés à un mois.
- `gestion/` offre une **vue par client** : chaque sous-dossier ne contient que des raccourcis vers les factures, devis et contrats du client. Pas de copie. Voir [Raccourcis et liens](../raccourcis-liens.md).

---

## `factures/`

**Rôle :** factures **émises** par ton entreprise (pas les brouillons définitifs ailleurs : une fois validée et envoyée, le PDF ou l’export comptable vit ici).

**Organisation :** un sous-dossier par mois d’émission utile, format `AAAA-MM` (`factures/2026-03/`).

**Format des fichiers:** `AAAA-MM_facture_tiers_numero.ext`

**Exemple :** `2026-03_facture_client-dupont_003.pdf`

Le numéro séquentiel (`001`, `002`…) différencie plusieurs factures au même client le même mois. Il correspond idéalement au numéro de facture de ta comptabilité.

---

## `devis/`

**Rôle :** propositions chiffrées envoyées aux clients (devis, propositions commerciales assimilées), y compris les versions révisées tant qu’elles restent des **devis** (pas encore une facture).

**Organisation :** sous-dossiers mensuels `AAAA-MM`, comme pour les factures.

**Format des fichiers:** `AAAA-MM_devis_tiers_numero.ext`

**Exemple :** `2026-03_devis_client-martin_001.pdf`

Même logique que les factures : date → type `devis` → tiers normalisé → numéro d’ordre. Pour une révision du **même** devis, ajoute un suffixe `-v2`, `-v3`, etc. avant l’extension (ex. `2026-03_devis_client-martin_001-v2.pdf`) sans changer le numéro de base.

---

## `contrats_modeles/`

**Rôle :** **modèles** de contrat ou d’avenant à dupliquer, compléter puis adapter pour chaque client. Pas de document signé ni de PDF « définitif client » dans ce dossier — uniquement les gabarits réutilisables (`.docx`, `.odt`, parfois PDF guide).

**Quand tu sors un contrat ou un avenant pour un client** (fichier adapté, puis signé ou archivé comme référence client), enregistre-le sous `contrats/AAAA-MM/` — pas dans `contrats_modeles/`. Voir la section **`contrats/`** pour le nommage des fichiers client.

**Format des fichiers:** `modele-contrat_objet_vN.ext`

**Exemple :** `modele-contrat_maintenance_annuelle_v2.docx`

Pas de date « client » dans le nom : ce sont des gabarits réutilisables. Le segment **objet** décrit le type de modèle (souvent plusieurs mots liés par des underscores ou des tirets, ex. `maintenance_annuelle`). **vN** est la version du gabarit (`v1`, `v2`…), pas une version « client ».

---

## `contrats/`

**Rôle :** tout **contrat ou avenant client** une fois sorti du statut « simple brouillon générique » : négociation, versions partagées, **PDF signé**, scans. Un sous-dossier **`AAAA-MM`** regroupe les dossiers clos ou actifs selon le mois de référence que tu choisis (souvent mois de signature ou de dépôt du fichier définitif — identique au mois du préfixe `AAAA-MM-JJ` si tu suis la convention ci‑dessous).

**Format des fichiers:** `AAAA-MM-JJ_tiers_contrat_CAAAA-XX.ext` ou `AAAA-MM-JJ_tiers_avenant_CAAAA-XX.ext`

**Exemple :** `2026-04-03_societe-acme_contrat_C2026-01.pdf` (avenant : `2026-04-03_societe-acme_avenant_C2026-02.pdf`)

`AAAA-MM-JJ` est en général la **date de signature** (ou une règle unique pour toute l’entreprise : dernière version signée, enregistrement interne, etc.). Le **tiers** est le client en minuscules, sans accents ni espaces, mots liés par des tirets (`societe-acme`). **`CAAAA-XX`** est une référence maison : `C` + année de numérotation + numéro d’ordre sur deux chiffres (`C2026-01`, …). Les avenants peuvent porter une nouvelle référence ou une convention documentée à part.

**Alternative (un seul système par dossier) :** `AAAA-MM_contrat_tiers_objet.ext` — ex. `2026-03_contrat_client-dupont_maintenance.pdf` — si tu préfères un **objet** lisible à la place du code `CAAAA-XX`. Ne pas mélanger les deux conventions sans les documenter. Extension toujours explicite (`.pdf` pour l’exemplaire signé, `.docx` si tu conserves aussi la version éditable).

---

## `offres/`

**Rôle :** documents **commerciaux structurants** et réutilisables : plaquettes, descriptifs de formation, grilles prestations, argumentaires — **sans être** une facture ni un devis client nominatif. Un sous-dossier par offre ou ligne de service (`formation_react/`, `audit_seo/`) évite de mélanger les contextes.

**Format des fichiers:** `nom-offre_version.ext`

**Exemple :** `formation-react_v2.pdf`

Documents intemporels : pas de date mensuelle obligatoire dans le nom. La version (`v1`, `v2`) différencie les révisions ; la date de modification du fichier peut compléter si besoin. Le sous-dossier (`formation_react/`, etc.) situe déjà l’offre : le nom de fichier reste court et stable.

---

## `gestion/`

**Rôle :** **vues transverses par client** : uniquement des **raccourcis** (liens symboliques, raccourcis OS, ou renvois documentés) vers les vrais fichiers dans `factures/`, `devis/`, `contrats/`. Aucune copie définitive ici : une seule source de vérité dans les dossiers typés.

**Organisation :** un sous-dossier par client, nom en français lisible (`Client dupont/`). Détail dans [Raccourcis et liens](../raccourcis-liens.md).
