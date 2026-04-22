# Spec : Adaptation du référentiel — front matter par dossier

Date : 2026-04-21

## Objectif

Réorganiser `packages/referentiel/classement/` pour que chaque dossier du plan de classement ait son propre fichier `.md` avec un front matter YAML structuré. Ajouter un script CLI qui collecte tous ces front matters dans un fichier YAML unique, token-efficient, exploitable par un LLM ou du code pour générer un PDF ou un fichier de config.

---

## Règles de création d'un fichier `.md`

Un fichier `.md` est créé pour **tout dossier** qui remplit au moins un de ces critères :

- Il a des sous-dossiers (fixes ou dynamiques)
- Il a une convention de nommage des fichiers

Exception : les dossiers purement chronologiques (`[AAAA-MM]`) n'ont **pas** de `.md`. Leur organisation est décrite dans le front matter du parent.

Les dossiers dynamiques (`[Nom du client]`) ont leur propre `.md` s'ils ont des sous-dossiers ou des conventions.

---

## Structure des fichiers

Tous les `.md` sont **plats** dans `classement/`. Le séparateur `__` encode la hiérarchie dans le nom de fichier.

### Exemple complet pour `Mes ventes/`

```
classement/
├── mes_ventes.md
├── mes_ventes__factures_clients.md
├── mes_ventes__modeles.md
├── mes_ventes__modeles__contrats.md
├── mes_ventes__modeles__devis_offres.md
├── mes_ventes__clients.md
├── mes_ventes__clients__nom_client.md
├── mes_ventes__clients__nom_client__contrats.md
└── mes_ventes__clients__nom_client__devis.md
```

`[AAAA-MM]/` sous `Mes factures clients/` → pas de `.md`, info dans `mes_ventes__factures_clients.md`.

---

## Schéma du front matter

### Champs communs (tous les dossiers)

```yaml
id: mes_ventes.factures_clients        # identifiant hiérarchique pointé, unique
folder_name: "Mes factures clients"    # nom exact du dossier (tel qu'affiché dans l'OS)
path: "Mes ventes/Mes factures clients" # chemin complet depuis la racine
parent: mes_ventes                     # id du parent (absent pour les dossiers racine)
dynamic: false                         # true si le nom du dossier est variable ([Nom du client])
option: core                           # option du référentiel qui active ce dossier
required: true                         # obligatoire quand l'option est active
description: "..."                     # une ligne : rôle du dossier
```

### Champs selon le contenu

**Dossier avec organisation chronologique :**
```yaml
organization:
  type: chronological
  subfolder_pattern: "AAAA-MM"
```

**Dossier avec sous-dossiers fixes :**
```yaml
organization:
  type: subdirs
  fixed_subdirs:
    - mes_ventes.modeles.contrats
    - mes_ventes.modeles.devis_offres
```

**Dossier mixte (sous-dossiers fixes + organisation libre) :**
```yaml
organization:
  type: mixed
  fixed_subdirs:
    - mes_ventes.clients.nom_client.contrats
    - mes_ventes.clients.nom_client.devis
  free_subdirs: true
```

**Convention de nommage des fichiers :**
```yaml
file_naming:
  pattern: "[AAAA-MM]_Facture_[Nom client]_[Numero].[ext]"
  fields:
    - name: AAAA-MM
      description: "date d'émission"
    - name: Nom client
      description: "nom du client, forme lisible"
    - name: Numero
      description: "numéro tel qu'il apparaît dans le logiciel"
    - name: ext
      description: "extension du fichier (pdf, docx…)"
  example: "2026-03_Facture_Dupont_F2600003.pdf"
```

### Exemples complets

**Dossier statique avec sous-dossiers dynamiques chronologiques :**
```yaml
---
id: mes_ventes.factures_clients
folder_name: "Mes factures clients"
path: "Mes ventes/Mes factures clients"
parent: mes_ventes
dynamic: false
option: core
required: true
description: "Factures émises, classées par mois d'émission"
organization:
  type: chronological
  subfolder_pattern: "AAAA-MM"
file_naming:
  pattern: "[AAAA-MM]_Facture_[Nom client]_[Numero].[ext]"
  fields:
    - name: AAAA-MM
      description: "date d'émission"
    - name: Nom client
      description: "nom du client, forme lisible"
    - name: Numero
      description: "numéro de la facture"
    - name: ext
      description: "extension (pdf, docx…)"
  example: "2026-03_Facture_Dupont_F2600003.pdf"
---
```

**Dossier dynamique avec sous-dossiers fixes et organisation libre :**
```yaml
---
id: mes_ventes.clients.nom_client
folder_name: "[Nom du client]"
path: "Mes ventes/Mes clients/[Nom du client]"
parent: mes_ventes.clients
dynamic: true
option: core
required: true
description: "Un dossier par client, nom lisible en français"
organization:
  type: mixed
  fixed_subdirs:
    - mes_ventes.clients.nom_client.contrats
    - mes_ventes.clients.nom_client.devis
  free_subdirs: true
---
```

---

## Migration des fichiers existants

Les fichiers actuels (`mes_ventes.md`, `mes_achats.md`, etc.) sont **réécrits** :

- Le front matter est enrichi selon le nouveau schéma
- Le contenu narratif de chaque sous-section est **déplacé** dans le fichier enfant correspondant
- Le fichier parent conserve uniquement la description générale du dossier racine

Les fichiers `__index.md`, `regles-nommage.md`, `regles-archivage.md`, `_index.md`, `plan-classement.md`, `demarrage-rapide.md` ne sont **pas modifiés** (hors périmètre).

---

## Script d'export

### Localisation

Nouveau fichier : `packages/referentiel-cli/src/commands/export-frontmatters.ts`

Nouvelle commande CLI :
```bash
referentiel-cli export-frontmatters [--output <path>]
```

Valeur par défaut de `--output` : `packages/referentiel/referentiel.yaml`

### Dépendance à ajouter

`gray-matter` — parsing YAML front matter depuis les fichiers `.md`.

### Comportement

1. Glob `packages/referentiel/classement/*.md` (hors `__index.md`)
2. Parser le front matter YAML de chaque fichier avec `gray-matter`
3. Trier les entrées par `id` (ordre lexicographique = ordre hiérarchique naturel)
4. Sérialiser en YAML compact
5. Écrire dans le fichier de sortie

### Format de sortie (`referentiel.yaml`)

```yaml
- id: mes_ventes
  folder_name: "Mes ventes"
  path: "Mes ventes"
  option: core
  required: true
  description: "Relation commerciale sortante"

- id: mes_ventes.factures_clients
  folder_name: "Mes factures clients"
  path: "Mes ventes/Mes factures clients"
  parent: mes_ventes
  dynamic: false
  option: core
  required: true
  description: "Factures émises, classées par mois d'émission"
  organization:
    type: chronological
    subfolder_pattern: "AAAA-MM"
  file_naming:
    pattern: "[AAAA-MM]_Facture_[Nom client]_[Numero].[ext]"
    example: "2026-03_Facture_Dupont_F2600003.pdf"
```

Le fichier `referentiel.yaml` est **versionné** dans le repo et regénéré à la demande.

---

## Périmètre

### Dans le périmètre

- Réécriture des 7 fichiers racine dans `classement/`
- Création des fichiers enfants pour tous les sous-dossiers qui respectent les règles
- Nouveau script `export-frontmatters` dans `referentiel-cli`
- Génération initiale de `referentiel.yaml`

### Hors périmètre

- Modification des fichiers `__index.md`, `regles-*.md`, `_index.md`, `plan-classement.md`, `demarrage-rapide.md`
- Génération PDF (étape suivante)
- Modification du comportement des autres commandes CLI existantes
