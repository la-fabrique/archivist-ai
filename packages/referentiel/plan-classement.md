# Plan de classement

> Partie du [Référentiel de gestion documentaire](._index.md) — v0

---

## Principe directeur

L'arborescence est organisée par **fonction métier et comptable**, pas par client ni par date.

Pourquoi ce choix :
- Un classement **par client** est intuitif au départ, mais il explose dès que tu as 20+ clients. Tu te retrouves avec des dizaines de dossiers au même niveau, sans cohérence entre eux.
- Un classement **par date** ne dit rien sur la nature du document. "2026-03" ne t'indique pas si tu cherches une facture, un contrat ou un relevé bancaire.
- Un classement **par fonction** reste stable même quand ton activité grandit. Les grandes catégories (ventes, achats, fiscalité…) ne changent pas.

---

## Les 8 dossiers racine

Ces dossiers se placent à la racine de ton espace de stockage (Drive, OneDrive, serveur, NAS).

| Dossier | Rôle | Contenu type |
|---------|------|-------------|
| `Mes Ventes/` | Relation commerciale sortante | Factures émises, devis, contrats clients, offres, suivi client |
| `Mes Achats/` | Dépenses de l'entreprise | Factures fournisseurs, assurances |
| `Mon Juridique/` | Entité juridique | Statuts, K-bis, PV d'AG, contrats importants |
| `Mon Social/` | Gestion du personnel | Contrats de travail, fiches de paie, DPAE |
| `Ma Fiscalité/` | Obligations fiscales | Déclarations TVA, CFE, avis d'imposition, liasses fiscales |
| `Ma Banque et Caisse/` | Trésorerie | Relevés bancaires, remises de chèques, journaux de caisse |
| `Ma Gestion Administrative/` | Courriers et divers | Courriers reçus et envoyés, documents administratifs divers |
| `Archives/` | Années closes | Archives annuelles compressées avec manifest |

**Logique de nommage :** tous les dossiers commencent par `Mon`, `Ma` ou `Mes` (sauf `Archives/`). C'est une convention volontaire — elle rappelle que ces documents t'appartiennent et crée une cohérence visuelle immédiate dans l'explorateur.

---

## Sous-structure de `Mes Ventes/`

`Mes Ventes/` est le dossier le plus fourni pour la plupart des TPE et indépendants. Son organisation est la plus détaillée.

```
Mes Ventes/
├── Factures/
│   ├── 2026-01/
│   ├── 2026-02/
│   └── 2026-03/
├── Devis/
│   ├── 2026-01/
│   └── ...
├── Contrats/
│   ├── 2026-01/
│   └── ...
├── Offres/
│   ├── formation-react/
│   └── audit-seo/
└── Gestion/
    ├── Client Dupont/    ← raccourcis uniquement
    └── Client Martin/    ← raccourcis uniquement
```

**Ce qu'il faut retenir :**

- Les documents vivent dans des **dossiers chronologiques par type** (`Factures/2026-03/`, `Devis/2026-02/`…). Ce sont les emplacements de référence.
- Les sous-dossiers mensuels (`AAAA-MM`) évitent d'avoir des centaines de fichiers au même niveau. En fin d'année, les factures de janvier et de décembre ne se côtoient pas.
- `Offres/` contient un dossier par offre ou service — ces documents sont intemporels, pas liés à un mois.
- `Gestion/` offre une **vue par client** : chaque sous-dossier ne contient que des raccourcis vers les factures, devis et contrats du client. Pas de copie. Voir [Raccourcis et liens](raccourcis-liens.md).

---

## Sous-structure de `Mes Achats/`

```
Mes Achats/
├── Factures fournisseurs/
│   ├── 2026/
│   │   ├── 2026-01/
│   │   ├── 2026-02/
│   │   └── 2026-03/
│   └── 2025/
│       ├── 2025-01/
│       └── ...
└── Assurances/
    ├── polices/
    └── attestations/
```

**Pourquoi un niveau "année" en plus ?** Les factures fournisseurs sont souvent consultées par exercice comptable. Ton comptable te demande "les achats 2025" — le dossier `2025/` répond directement. Pour `Mes Ventes/`, les mois sont suffisants car les factures émises sont consultées individuellement.

**Pourquoi les assurances dans `Mes Achats/` ?** En comptabilité, une prime d'assurance est une charge. Les polices et attestations sont les justificatifs de cette charge. Ton comptable ira chercher ça au même endroit que les factures fournisseurs.

---

## Les autres dossiers racine

`Mon Juridique/`, `Mon Social/`, `Ma Fiscalité/`, `Ma Banque et Caisse/` et `Ma Gestion Administrative/` ont une structure plus libre.

**Pourquoi pas de sous-dossiers mensuels ?** Le volume de documents est faible. Tu ne crées pas un PV d'AG chaque mois. Ces dossiers se consultent par thème, pas par date — tu cherches "les statuts" ou "le contrat de travail de Jean", pas "les documents de mars".

Quelques exemples de sous-dossiers utiles :

```
Mon Juridique/
├── statuts/
├── kbis/
└── pv-ag/

Mon Social/
├── contrats-travail/
└── fiches-paie/

Ma Fiscalité/
├── tva/
├── cfe/
└── liasses-fiscales/

Ma Banque et Caisse/
├── releves/
└── remises-cheques/
```

Ces sous-dossiers sont des suggestions. Adapte selon ton activité.

---

## `Archives/`

```
Archives/
├── 2024/
│   ├── mes-ventes-2024.zip
│   ├── mes-achats-2024.zip
│   ├── ma-fiscalite-2024.zip
│   ├── mon-social-2024.zip
│   ├── ma-banque-et-caisse-2024.zip
│   ├── ma-gestion-administrative-2024.zip
│   └── manifest.md
└── 2023/
    └── ...
```

Le détail des règles d'archivage (quoi archiver, quand, comment) est dans [Règles d'archivage](regles-archivage.md).

---

## Quand adapter ce plan

Ce plan de classement est conçu pour la majorité des TPE et indépendants, mais il n'est pas universel.

| Situation | Adaptation |
|-----------|-----------|
| Plusieurs sociétés | Un dossier racine par entité juridique, chacun avec cette même structure |
| Projets longs (BTP, conseil, agence) | Ajouter un dossier `Mes Projets/` avec un sous-dossier par projet |
| Pas de salariés | `Mon Social/` peut être réduit à la gestion de ta propre rémunération (TNS, dividendes) |
| Activité sans devis formels | Simplifier `Mes Ventes/` en retirant `Devis/` |
