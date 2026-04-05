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
    ├── Client Dupont/
    │   ├── Contrats/
    │   ├── Devis/
    │   ├── Offres/
    │   └── ...     ← notes, CR, suivi libre
    └── Client Martin/
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

**Format des fichiers:** `AAAA-MM_facture_tiers_numero.ext`

**Exemple :** `2026-03_facture_client-dupont_003.pdf`

Le numéro séquentiel (`001`, `002`…) différencie plusieurs factures au même client le même mois. Il correspond idéalement au numéro de facture de ta comptabilité.

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

**Organisation :** un sous-dossier par client, nom en français lisible (`Client Dupont/`). Les sous-dossiers `Contrats/`, `Devis/` et `Offres/` sont imposés dans chaque client ; le reste de l'organisation est libre.

```
Mes clients/
└── Client Dupont/
    ├── Contrats/    ← contrats et avenants réels du client
    ├── Devis/       ← devis envoyés au client
    ├── Offres/      ← offres personnalisées envoyées au client
    └── ...          ← notes, CR, suivi (libre)
```

### `Contrats/` (dans chaque client)

**Rôle :** tout **contrat ou avenant** une fois sorti du statut « simple brouillon générique » : négociation, versions partagées, **PDF signé**, scans. Structure plate — pas de sous-dossiers mensuels, le volume par client reste faible.

**Format des fichiers:** `AAAA-MM-JJ_tiers_contrat_CAAAA-XX.ext` ou `AAAA-MM-JJ_tiers_avenant_CAAAA-XX.ext`

**Exemple :** `2026-04-03_societe-acme_contrat_C2026-01.pdf` (avenant : `2026-04-03_societe-acme_avenant_C2026-02.pdf`)

`AAAA-MM-JJ` est en général la **date de signature**. Le **tiers** est le client en minuscules, sans accents ni espaces, mots liés par des tirets (`societe-acme`). **`CAAAA-XX`** est une référence maison : `C` + année de numérotation + numéro d'ordre sur deux chiffres (`C2026-01`, …).

**Alternative :** `AAAA-MM_contrat_tiers_objet.ext` — ex. `2026-03_contrat_client-dupont_maintenance.pdf` — si tu préfères un **objet** lisible à la place du code `CAAAA-XX`. Ne pas mélanger les deux conventions sans les documenter.

### `Devis/` (dans chaque client)

**Rôle :** propositions chiffrées envoyées au client (devis, propositions commerciales assimilées), y compris les versions révisées tant qu'elles restent des **devis** (pas encore une facture). Structure plate — pas de sous-dossiers mensuels, le volume par client reste faible.

**Format des fichiers:** `AAAA-MM-JJ_tiers_devis_numero.ext`

**Exemple :** `2026-03-15_client-martin_devis_001.pdf`

Même logique que les contrats : date de référence, tiers normalisé, numéro d'ordre. Pour une révision du **même** devis, ajoute un suffixe `-v2`, `-v3` avant l'extension (ex. `2026-03-15_client-martin_devis_001-v2.pdf`) sans changer le numéro de base.

### `Offres/` (dans chaque client)

**Rôle :** offres commerciales **personnalisées** envoyées au client (propositions adaptées à partir des modèles d'offre). Structure plate — pas de sous-dossiers mensuels, le volume par client reste faible.

**Format des fichiers:** `AAAA-MM-JJ_tiers_offre_numero.ext`

**Exemple :** `2026-03-15_client-dupont_offre_001.pdf`

Même logique que les contrats et devis : date de référence, tiers normalisé, numéro d'ordre. Pour une révision, ajoute un suffixe `-v2`, `-v3` avant l'extension.
