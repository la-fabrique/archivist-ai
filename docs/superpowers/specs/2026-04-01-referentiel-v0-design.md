# Référentiel v0 — Design

> Spec validée le 2026-04-01

## Contexte

Le référentiel est le produit central d'Archiviste IA : un ensemble de règles expertes de classement documentaire pour TPE et indépendants. Il sert d'abord de **spec interne** itérative, puis sera partagé publiquement comme lead magnet (format de publication à décider plus tard).

## Décisions de design

### Format : guide pratique

Chaque fichier suit la structure : contexte → règles → exemples concrets → cas limites. Ton accessible mais rigoureux. Ce format sert directement de base pour le contenu public avec peu de réécriture, et documente le "pourquoi" derrière chaque règle pour faciliter l'itération avec la communauté.

Alternatives écartées :
- **Règles pures** (trop sec, inexploitable comme contenu public)
- **Deux couches machine/humain** (over-engineering pour un v0 qui va beaucoup bouger)

### Arborescence : logique comptable

L'arborescence est organisée par **fonction comptable/métier**, pas par client ni par date. Tous les dossiers racine suivent la convention `Mon/Ma/Mes + nom`.

## Fichiers du référentiel

Cible : `packages/referentiel/`

### `_index.md` — Introduction

- Accroche : règles d'expert, simples, visibles, adaptées TPE
- Public cible : TPE, freelances, artisans, professions libérales (1-10 personnes, pas de service IT)
- 4 principes fondateurs : Visibilité, Co-construction, Simplicité, Compatibilité
- Sommaire avec liens vers les 4 fichiers
- Statut : v0, version de travail, enrichie par retours communauté

### `plan-classement.md` — Plan de classement

**Principe** : classement par fonction métier. Un classement par client explose à 20+ clients. Un classement par date ne dit rien sur la nature du document.

**8 dossiers racine :**

| Dossier | Rôle |
|---------|------|
| `Mes Ventes/` | Factures, devis, contrats, offres, suivi client |
| `Mes Achats/` | Factures fournisseurs, assurances |
| `Mon Juridique/` | Statuts, K-bis, PV d'AG |
| `Mon Social/` | Contrats de travail, fiches de paie |
| `Ma Fiscalité/` | Déclarations, TVA, CFE, avis d'imposition |
| `Ma Banque et Caisse/` | Relevés bancaires, remises de chèques, journaux de caisse |
| `Ma Gestion Administrative/` | Courriers, divers |
| `Archives/` | Années closes, compressées avec manifest |

**Sous-structure de `Mes Ventes/` :**

```
Mes Ventes/
├── Factures/
│   ├── 2026-01/
│   └── ...
├── Devis/
├── Contrats/
├── Offres/
└── Gestion/       ← raccourcis par client uniquement
```

**Sous-structure de `Mes Achats/` :**

```
Mes Achats/
├── Factures fournisseurs/
│   ├── 2026/
│   │   ├── 2026-01/
│   │   └── ...
│   └── 2025/
└── Assurances/
```

**Les autres dossiers** (`Mon Juridique/`, `Mon Social/`, `Ma Fiscalité/`, `Ma Banque et Caisse/`, `Ma Gestion Administrative/`) : pas de sous-dossiers mensuels obligatoires, le volume est faible et la consultation se fait par thème.

**Quand adapter** :
- Multi-société → un dossier racine par entité juridique
- Projets longs → ajouter `Mes Projets/`

### `regles-nommage.md` — Règles de nommage

**Socle commun :**
- Date en préfixe (toujours)
- Tout en minuscules, pas d'accents, pas d'espaces
- Tirets `-` dans un segment, underscores `_` entre segments
- Extension explicite

**Règles par dossier** (chaque dossier définit ses segments pertinents) :

| Dossier | Format | Exemple |
|---------|--------|---------|
| `Mes Ventes/Factures/` | `AAAA-MM_facture_tiers_numero` | `2026-03_facture_client-dupont_003.pdf` |
| `Mes Ventes/Devis/` | `AAAA-MM_devis_tiers_numero` | `2026-03_devis_client-martin_001.pdf` |
| `Mes Ventes/Contrats/` | `AAAA-MM_contrat_tiers_objet` | `2026-03_contrat_client-dupont_maintenance.pdf` |
| `Mes Ventes/Offres/` | `nom-offre_version` | `formation-react_v2.pdf` |
| `Mes Achats/Factures/` | `AAAA-MM_facture_fournisseur_numero` | `2026-03_facture_orange_012.pdf` |
| `Mes Achats/Assurances/` | `AAAA_type_assureur_objet` | `2026_police_axa_rcpro.pdf` |
| `Mon Social/` | `AAAA-MM_type_nom-salarie` | `2026-03_fiche-paie_dupont-jean.pdf` |
| `Ma Fiscalité/` | `AAAA-MM_type_impot` | `2026-01_declaration_tva.pdf` |
| `Ma Banque et Caisse/` | `AAAA-MM_releve_banque` | `2026-03_releve_banque-populaire.pdf` |
| `Mon Juridique/` | `AAAA_type_objet` | `2025_statuts_sas-monentreprise.pdf` |
| `Ma Gestion Administrative/` | `AAAA-MM_type_expediteur_objet` | `2026-03_courrier_urssaf_mise-en-demeure.pdf` |

**Conventions d'écriture :**
- Minuscules uniquement
- Tirets dans un segment, underscores entre segments
- Pas d'espaces, pas d'accents, pas de caractères spéciaux
- Pas d'abréviations sauf universelles (`tva`, `rh`)

**Cas particuliers :**
- Sans tiers → omettre le segment
- Sans date précise → année seule `AAAA`
- Versions → suffixe `-v2` avant l'extension
- Scans → préfixer le type avec `scan-`

### `regles-archivage.md` — Règles d'archivage

**Cycle de vie :**

```
Actif (N et N-1)  →  Archivé (N-2+)  →  Purgeable (après durée légale)
```

**Durées de conservation légales :**

| Type | Durée | Base légale |
|------|-------|-------------|
| Factures (émises et reçues) | 10 ans | Code de commerce, art. L123-22 |
| Contrats commerciaux | 5 ans après fin | Code civil, art. 2224 |
| Documents fiscaux | 6 ans | LPF, art. L102 B |
| Bulletins de paie | 5 ans | Code du travail, art. L3243-4 |
| Documents sociaux | 5 ans après radiation | Code de commerce |
| Relevés bancaires | 5 ans | Code de commerce |
| Polices d'assurance | 2 ans après fin | Code des assurances, art. L114-1 |
| Documents juridiques | Vie de l'entreprise + 5 ans | — |

**Règles par dossier :**

| Dossier | Accès direct | Archivage | Purge |
|---------|-------------|-----------|-------|
| `Mes Ventes/` | N et N-1 | N-2 → Archives | 10 ans (factures), 5 ans (contrats) |
| `Mes Achats/` | N et N-1 | N-2 → Archives | 10 ans (factures), 2 ans (assurances échues) |
| `Ma Fiscalité/` | N et N-1 | N-2 → Archives | 6 ans |
| `Mon Social/` | N et N-1 | N-2 → Archives | 5 ans |
| `Ma Banque et Caisse/` | N et N-1 | N-2 → Archives | 5 ans |
| `Mon Juridique/` | Toujours actif | Jamais tant que l'entreprise existe | 5 ans après radiation |
| `Ma Gestion Administrative/` | N et N-1 | N-2 → Archives | Au cas par cas |

**Structure des archives :**

```
Archives/
├── 2024/
│   ├── mes-ventes-2024.zip
│   ├── mes-achats-2024.zip
│   ├── ...
│   └── manifest.md
└── 2023/
```

**Manifest** : liste le nombre de documents par catégorie, date de création, date de purge la plus proche.

**Règles de sécurité :**
- Jamais de suppression automatique — notification obligatoire
- Jamais de duplication — raccourcis uniquement
- Compression avec vérification d'intégrité avant suppression de l'original
- Archivage par année entière, jamais par mois isolé

### `raccourcis-liens.md` — Raccourcis et liens

**Principe** : un document ne vit qu'à un seul endroit. Les vues alternatives (par client, par projet) utilisent des raccourcis, jamais des copies.

**Cas d'usage principal** : vue par client dans `Mes Ventes/Gestion/{Client}/` — raccourcis vers les factures, devis, contrats dispersés dans l'arborescence chronologique.

**Implémentation par système :**

| Système | Mécanisme |
|---------|-----------|
| Windows | Raccourci `.lnk` |
| macOS | Alias |
| Linux | Lien symbolique |
| Google Drive | Raccourci Drive |
| OneDrive | `.url` ou fichier `.md` avec lien |

**Règles :**
- Pas de raccourci vers un raccourci
- Même nom que l'original
- Nettoyage lors de l'archivage annuel
- Un document multi-client → un raccourci dans chaque dossier client
