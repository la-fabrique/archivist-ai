# Archiviste IA — Positionnement & Discovery

> Design validé le 2026-03-09

## Approche

**Community-first + Référentiel de règles expertes.**

Le produit n'est pas "de l'IA". Le produit c'est un **référentiel de règles expertes** que l'IA exécute fidèlement. La confiance vient de :

1. Les règles sont **visibles** (pas une boîte noire)
2. Les règles sont **co-construites** avec des experts et des utilisateurs
3. Les règles sont **simples** à comprendre
4. L'archivage légal est **automatique**

Le référentiel est à la fois le produit, le contenu marketing, et l'outil de validation.

---

## Lean Canvas

| Bloc | Contenu |
|------|---------|
| **Problème** | Les TPE/indépendants rangent leurs documents à la main, de façon improvisée. Résultat : ils perdent du temps à chercher, rien n'est cohérent, et retrouver un document précis relève de la chance. |
| **Segment client** | TPE, freelances, artisans, professions libérales — 1 à 10 personnes, pas de service IT. |
| **Proposition de valeur** | Un archiviste IA qui se branche sur votre stockage existant (OneDrive, Google Drive, serveur local) et applique des règles d'expert visibles et compréhensibles. Pas de nouveau SaaS où déposer vos fichiers. Pas de boîte noire. Vos données restent chez vous. |
| **Solution** | 1) Référentiel de règles ouvert (plan de classement, nommage, archivage). 2) Agent IA qui se connecte à votre GED et applique ces règles en place. |
| **Canaux** | Community-first : groupes TPE & indépendants. Le référentiel est le lead magnet. |
| **Sources de revenus** | À valider. Piste initiale : référentiel gratuit → agent IA payant. Modèle exact à itérer après feedback communauté. |
| **Métriques clés** | Téléchargements du référentiel, inscriptions waitlist, taux conversion référentiel → waitlist. |
| **Avantage compétitif** | 1) Méthode transparente (règles visibles) vs IA opaque. 2) Se branche sur l'existant vs nouveau silo. 3) Souveraineté des données (restent chez le client). |
| **Coûts** | Temps de création du référentiel, 100-500€ en ads ciblés, infra IA (plus tard). |

---

## Référentiel v0 — Plan de classement

### Arborescence type

```
📁 Mes Clients/
│   ├── 📁 Factures/
│   │   ├── 📁 2026-01/
│   │   │   ├── 2026-01_facture_client-dupont_001.pdf
│   │   │   └── 2026-01_facture_client-martin_002.pdf
│   │   ├── 📁 2026-02/
│   │   └── 📁 2026-03/
│   ├── 📁 Devis/
│   │   ├── 📁 2026-01/
│   │   └── 📁 2026-02/
│   ├── 📁 Contrats/
│   │   ├── 📁 2026-01/
│   │   └── 📁 2026-02/
│   └── 📁 Gestion/
│       ├── 📁 Client Dupont/
│       │   ├── 🔗 → Factures/2026-03/..._client-dupont_001.pdf
│       │   ├── 🔗 → Devis/2026-01/..._client-dupont_001.pdf
│       │   └── 🔗 → Contrats/2025-06/..._client-dupont_001.pdf
│       └── 📁 Client Martin/
│           └── 🔗 → ...
│
📁 Mes Offres/
│   ├── 📁 {Nom Offre A}/
│   └── 📁 {Nom Offre B}/
│
📁 Mes Achats/
│   └── 📁 Factures fournisseurs/
│       ├── 📁 2026/
│       │   ├── 📁 2026-01/
│       │   ├── 📁 2026-02/
│       │   └── 📁 2026-03/
│       └── 📁 2025/
│           └── 📁 2025-01/ ... 2025-12/
│
📁 Mon Entreprise/
│   ├── 📁 Juridique/
│   ├── 📁 Assurances/
│   ├── 📁 RH/
│   └── 📁 Administratif/
│
📁 Raccourcis/
│   └── 🔗 (raccourcis transversaux au besoin)
│
📁 Archives/
    └── 📁 2024/
        ├── mes-clients-2024.zip
        ├── mes-achats-2024.zip
        └── manifest.md
```

### Règles de nommage

| Règle | Format | Exemple |
|-------|--------|---------|
| Date en préfixe | `AAAA-MM` | `2026-03` |
| Type de document | après la date | `_facture_`, `_devis_`, `_contrat_` |
| Nom du tiers | après le type | `_client-dupont_` |
| Numéro séquentiel | en suffixe | `_001.pdf` |
| **Complet** | `AAAA-MM_type_tiers_num.ext` | `2026-03_facture_client-dupont_003.pdf` |

### Règles d'archivage

| Règle | Détail |
|-------|--------|
| **Dossiers par mois** | `{AAAA-MM}` pour Factures, Devis, Contrats |
| **Archivage** | On garde N et N-1 en accès direct. N-2 et plus → compression dans `Archives/` |
| **Pas de duplication** | Jamais de copie, toujours des liens symboliques |
| **Rétention légale** | Factures 10 ans, contrats 5 ans après fin, docs fiscaux 6 ans |
| **Purge** | Notification avant suppression, jamais automatique |
| **Manifest** | Fichier `manifest.md` listant le contenu de chaque archive |

### Raccourcis (liens symboliques)

Les documents vivent dans des dossiers chronologiques par type. La vue "par client" dans `Gestion/` n'est que des raccourcis. Pas de duplication, une seule source de vérité.

---

## Stratégie communauté

### Phase 1 — Le référentiel comme contenu (semaines 1-2, 0€)

**Objectif** : Publier le référentiel en contenu ouvert pour attirer et engager.

| Action | Canal | Format |
|--------|-------|--------|
| Post "Comment je range les documents de ma boîte" | LinkedIn personnel | Carrousel ou post texte long |
| Même contenu adapté | Groupes Facebook (freelances, micro-entrepreneurs, compta TPE) | Post natif avec image |
| Publication du référentiel complet | Blog / page du site ou PDF téléchargeable | Le référentiel v0 en entier |

**Le hook** : On ne parle pas d'IA. On parle de **méthode**. "Voici comment un expert archiviste rangerait les documents de votre entreprise. C'est gratuit, servez-vous."

### Phase 2 — Écouter et itérer (semaines 2-4, 0€)

**Objectif** : Récolter du feedback pour valider/ajuster les hypothèses.

| Action | Ce qu'on cherche |
|--------|-----------------|
| Répondre à chaque commentaire, poser des questions | Quels dossiers manquent ? Quelle règle semble bizarre ? |
| Identifier les "power users" qui réagissent fort | Futurs beta-testeurs et ambassadeurs |
| Infiltrer les discussions existantes sur le rangement/classement | Observer les vrais mots utilisés par la cible (= copywriting futur) |
| Proposer 3-5 interviews rapides (15 min) aux profils les plus engagés | Comprendre le workflow réel, les outils utilisés, les douleurs concrètes |

**Communautés cibles** :

- Groupes Facebook : "Freelances en France", "Micro-entrepreneurs", "Compta facile"
- LinkedIn : hashtags #freelance #tpe #gestiondocumentaire
- Reddit : r/freelanceFR, r/vosfinances
- Forums : indépendants.fr, forum des auto-entrepreneurs

### Phase 3 — Teaser produit (semaines 4-6, 100-500€)

**Objectif** : Convertir l'audience en waitlist avec un petit budget ads.

| Action | Budget |
|--------|--------|
| Post sponsorisé LinkedIn ou Facebook (retargeting + audiences similaires) | 100-300€ |
| Ads A/B sur 2 messages max | 100-200€ |
| Landing page mise à jour avec le référentiel intégré | 0€ |

**Deux messages à tester** :

1. *"Arrêtez de ranger vos fichiers. Un archiviste IA le fait pour vous, sur votre Drive."*
2. *"Des règles d'expert pour vos documents. Transparentes. Appliquées par l'IA. Sans changer d'outil."*

### Métriques par phase

| Phase | Métrique | Seuil de validation |
|-------|----------|-------------------|
| 1 | Engagement (likes, commentaires, partages) | >50 interactions |
| 1 | Téléchargements du référentiel | >100 |
| 2 | Interviews réalisées | ≥5 |
| 2 | Insights actionnables collectés | ≥3 ajustements au référentiel |
| 3 | Inscriptions waitlist | >200 |
| 3 | Coût par inscription | <2€ |

---

## Structure docs/ cible

```
packages/
├── landing/
└── referentiel/
    ├── _index.md
    ├── plan-classement.md
    ├── regles-nommage.md
    ├── regles-archivage.md
    └── raccourcis-liens.md

docs/
├── plans/
│   └── 2026-03-09-positionnement-discovery-design.md  ← ce fichier
├── lean-canvas.md
├── community/
│   ├── strategie.md
│   ├── contenus.md
│   └── feedbacks/
├── hypotheses/
│   ├── _index.md
│   └── ...
└── discovery/
    ├── communities.md
    ├── interviews/
    └── insights.md
```

---

## Prochaines étapes

1. Créer la structure `docs/` + `packages/referentiel/`
2. Rédiger le référentiel v0 dans des fichiers séparés (plan-classement, nommage, archivage, ...)
3. Rédiger la stratégie communauté détaillée
4. Préparer le premier post LinkedIn/Facebook
5. Mettre à jour la landing page avec le nouveau positionnement
