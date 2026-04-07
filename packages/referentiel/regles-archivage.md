# Règles d'archivage

> Partie du [Référentiel de gestion documentaire](./_index.md) — v0

---

## Principe directeur

L'archivage répond à deux besoins distincts :

1. **Garder l'espace de travail lisible** — tu n'as pas besoin de voir les factures de 2019 chaque jour. Les sortir de l'arborescence courante allège ta vue sans rien perdre.
2. **Respecter les obligations légales de conservation** — certains documents doivent être conservés plusieurs années. Supprimer sans vérifier peut te mettre en infraction.

**Règle absolue : on ne supprime jamais sans prévenir.** Toute action de purge est notifiée et exige une confirmation manuelle.

---

## Cycle de vie d'un document

```
Actif (N et N-1)  →  Archivé (N-2 et plus)  →  Purgeable (après durée légale)
```

| État | Définition | Emplacement |
|------|-----------|-------------|
| **Actif** | Documents des 2 dernières années — consultation fréquente | Dans l'arborescence courante (`Mes ventes/`, `Mes achats/`…) |
| **Archivé** | Documents de N-2 et plus — consultation rare mais conservés | Dans `Archives/AAAA/`, compressés |
| **Purgeable** | Durée légale expirée — peuvent être supprimés | Dans `Archives/`, signalés dans le manifest |

**Exemple :** en 2026, les documents de 2024 et 2025 restent actifs. Les documents de 2023 et avant passent en archive.

---

## Durées de conservation légales

> ⚠️ Ces durées sont des **minimums légaux**. En cas de doute, conserve plus longtemps. Vérifie toujours avec ton expert-comptable — des règles spécifiques peuvent s'appliquer à ton secteur ou à ta situation.

| Type de document | Durée | Base légale |
|-----------------|-------|-------------|
| Factures émises et reçues | **10 ans** | Code de commerce, art. L123-22 |
| Contrats commerciaux | **5 ans** après fin du contrat | Code civil, art. 2224 |
| Documents fiscaux (déclarations, TVA, CFE) | **6 ans** | Livre des procédures fiscales, art. L102 B |
| Bulletins de paie | **5 ans** | Code du travail, art. L3243-4 |
| Documents sociaux (PV d'AG, statuts en vigueur) | **5 ans** après radiation | Code de commerce |
| Relevés bancaires | **5 ans** | Code de commerce |
| Polices d'assurance | **2 ans** après fin du contrat | Code des assurances, art. L114-1 |
| Documents juridiques fondateurs (statuts, K-bis) | Durée de vie de l'entreprise + 5 ans | — |

---

## Règles par dossier

| Dossier | Accès direct | Archivage | Purge possible |
|---------|-------------|-----------|----------------|
| `Mes ventes/` | N et N-1 | N-2 → `Archives/` | 10 ans (factures), 5 ans (contrats) |
| `Mes achats/` | N et N-1 | N-2 → `Archives/` | 10 ans (factures fournisseurs) |
| `Ma fiscalité/` | N et N-1 | N-2 → `Archives/` | 6 ans |
| `Mon social/` | N et N-1 | N-2 → `Archives/` | 5 ans |
| `Ma banque et caisse/` | N et N-1 | N-2 → `Archives/` | 5 ans |
| `Mon juridique/` | Toujours actif | Jamais tant que l'entreprise existe | 5 ans après radiation |

**Cas particulier de `Mon juridique/`** : les statuts, K-bis et PV d'AG ne s'archivent pas. Ces documents définissent l'existence légale de ta structure — ils doivent rester accessibles en permanence.

---

## Structure des archives

```
Archives/
├── 2024/
│   ├── mes_ventes_2024.zip
│   ├── mes_achats_2024.zip
│   ├── ma_fiscalite_2024.zip
│   ├── mon_social_2024.zip
│   ├── ma_banque_et_caisse_2024.zip
│   └── manifest.md
└── 2023/
    ├── ...
    └── manifest.md
```

**Une archive par dossier racine et par année.** Chaque fichier zip correspond exactement à un dossier racine pour une année donnée — `mes_ventes_2024.zip` contient tout le contenu de `Mes ventes/` pour l'année 2024.

### Le manifest

Chaque dossier d'archive annuelle contient un `manifest.md` qui documente :

```markdown
# Archive 2024

Créée le : 2025-02-01

## Contenu

| Archive | Nombre de documents |
|---------|-------------------|
| mes_ventes_2024.zip | 47 |
| mes_achats_2024.zip | 23 |
| ma_fiscalite_2024.zip | 12 |
| mon_social_2024.zip | 36 |
| ma_banque_et_caisse_2024.zip | 12 |

## Dates de purge

| Archive | Purge possible à partir de |
|---------|--------------------------|
| mes_ventes_2024.zip (factures) | 2034 |
| mes_achats_2024.zip (factures) | 2034 |
| ma_fiscalite_2024.zip | 2030 |
| mon_social_2024.zip | 2029 |
| ma_banque_et_caisse_2024.zip | 2029 |
```

---

## Règles de sécurité

**Jamais de suppression automatique.** Toute opération de purge envoie une notification et attend une validation manuelle. Un document supprimé par erreur peut être irrécupérable.

**Jamais de duplication.** Un document n'existe qu'à un seul endroit physique. Les raccourcis (voir [Raccourcis et liens](raccourcis-liens.md)) ne comptent pas comme des copies.

**Vérification avant suppression.** Après la création d'une archive zip, vérifier l'intégrité du fichier compressé avant de supprimer les originaux. Ne jamais supprimer l'original sans avoir confirmé que l'archive est lisible et complète.

**Archivage par année entière.** On n'archive pas un mois isolé, ni un dossier partiel. L'unité d'archivage est l'année complète pour un dossier donné. Cela garantit la cohérence des archives et facilite les recherches ultérieures.
