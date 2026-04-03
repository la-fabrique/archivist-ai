# `mes_ventes/`

> [Plan de classement](__index.md) — [Référentiel](../_index.md) — v0

Relation commerciale sortante : factures émises, devis, contrats clients, offres, suivi client.


```
mes_ventes/
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
    ├── client_dupont/    ← raccourcis uniquement
    └── client_martin/    ← raccourcis uniquement
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

**Nommage des fichiers :** voir [Règles de nommage — `mes_ventes/factures`](../regles-nommage.md#mes_ventesfactures). L’essentiel : date → type `facture` → client normalisé → numéro (souvent aligné sur la compta).

---

## `devis/`

**Rôle :** propositions chiffrées envoyées aux clients (devis, propositions commerciales assimilées), y compris les versions révisées tant qu’elles restent des **devis** (pas encore une facture).

**Organisation :** sous-dossiers mensuels `AAAA-MM`, comme pour les factures.

**Nommage :** [Règles — `mes_ventes/devis`](../regles-nommage.md#mes_ventesdevis). Un suffixe `-v2`, `-v3`, etc. distingue les révisions du même devis.

---

## `contrats_modeles/`

**Rôle :** **modèles** de contrat ou d’avenant à dupliquer, compléter puis adapter pour chaque client. Pas de document signé ni de PDF « définitif client » dans ce dossier — uniquement les gabarits réutilisables (`.docx`, `.odt`, parfois PDF guide).

**Nommage des modèles :** sans date client ; versionner le gabarit (`modele-contrat_maintenance-v2.docx`). Détail : [Règles — modèles](../regles-nommage.md#mes_ventescontrats_modeles).

**Quand tu sors un contrat ou un avenant pour un client** (fichier adapté, puis signé ou archivé comme référence client), enregistre-le sous `contrats/AAAA-MM/` avec le format ci‑dessous — pas dans `contrats_modeles/`.

### Convention pour un contrat ou avenant **client** (dans `contrats/AAAA-MM/`)

Les crochets `[ ]` ci‑dessous indiquent des **composantes du nom**, pas des caractères à mettre dans le fichier.

| Composante | Signification |
|------------|----------------|
| **`AAAA-MM-JJ`** | Date de référence du document : en général **date de signature** ; si tu préfères la date de **dernière version signée** ou d’enregistrement interne, garde la même règle pour toute l’entreprise. Format jour entier pour lever l’ambiguïté entre deux actes le même mois. |
| **`_` (underscore)** | Séparateur entre **grands blocs** du nom (aligné sur le [socle commun](../regles-nommage.md#socle-commun-fichiers)). |
| **`nom-client`** | Tiers identifié, en **minuscules, sans accents, sans espaces**, mots liés par des tirets (ex. `societe-acme`, `dupont-jean`). Même logique que pour factures et devis. |
| **`contrat` ou `avenant`** | Nature du document : contrat initial vs avenant qui modifie ou complète un contrat existant. |
| **`_`** | Encore un underscore avant le code métier. |
| **`CAAAA-XX`** | **Référence contrat** maison : `C` = préfixe fixe « contrat » (homogénéise les tris et les recherches) ; `AAAA` = année de **numérotation** ou d’engagement (souvent l’année civile du dossier) ; `XX` = numéro d’ordre sur **deux chiffres** (`01` … `99`) pour ce millésime. Ex. `C2026-01` = premier contrat référencé en 2026. Les avenants peuvent réutiliser la base du contrat + suffixe de version si tu le documentes ailleurs, ou une ligne `C2026-02` — à figer en interne. |
| **`.extension`** | Toujours explicite : `.pdf` pour l’exemplaire signé, `.docx` pour la version éditable si tu la conserves à côté. |

**Forme résumée :**

```text
AAAA-MM-JJ_nom-du-client_contrat_CAAAA-XX.ext
AAAA-MM-JJ_nom-du-client_avenant_CAAAA-XX.ext
```

**Exemples :**

- `2026-04-03_societe-acme_contrat_C2026-01.pdf`
- `2026-04-03_societe-acme_avenant_C2026-02.pdf`

---

## `contrats/`

**Rôle :** tout **contrat ou avenant client** une fois sorti du statut « simple brouillon générique » : négociation, versions partagées, **PDF signé**, scans. Un sous-dossier **`AAAA-MM`** regroupe les dossiers clos ou actifs selon le mois de référence que tu choisis (souvent mois de signature ou de dépôt du fichier définitif — identique à la date du préfixe du nom si tu appliques la convention ci‑dessus).

**Nommage :** [Règles — `mes_ventes/contrats`](../regles-nommage.md#mes_ventescontrats). La **table segment par segment** pour un contrat ou un avenant client figure dans la section **`contrats_modeles/`** ci‑dessus (même convention ; les fichiers signés vivent ici, dans `contrats/`, pas dans les modèles).

---

## `offres/`

**Rôle :** documents **commerciaux structurants** et réutilisables : plaquettes, descriptifs de formation, grilles prestations, argumentaires — **sans être** une facture ni un devis client nominatif. Un sous-dossier par offre ou ligne de service (`formation_react/`, `audit_seo/`) évite de mélanger les contextes.

**Nommage :** souvent **sans date dans le nom** ; version logique (`v2`). Voir [Règles — offres](../regles-nommage.md#mes_ventesoffres).

---

## `gestion/`

**Rôle :** **vues transverses par client** : uniquement des **raccourcis** (liens symboliques, raccourcis OS, ou renvois documentés) vers les vrais fichiers dans `factures/`, `devis/`, `contrats/`. Aucune copie définitive ici : une seule source de vérité dans les dossiers typés.

**Organisation :** un sous-dossier par client, nom snake case (`client_dupont/`). Détail dans [Raccourcis et liens](../raccourcis-liens.md).
