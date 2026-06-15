# Usage — archivist-cli

## Configuration persistante

La CLI peut mémoriser les paramètres récurrents pour éviter de les passer à chaque commande.

### archivist config set

```
archivist config set referentiel <uri>   # Copie le référentiel et mémorise son URI
archivist config set root <uri>          # Mémorise le dossier racine de l'archive
archivist config set llm <nom>           # Mémorise l'adaptateur LLM
```

### archivist config show

Affiche la configuration persistée en JSON :

```
archivist config show
```

**Emplacement** : la config est stockée dans le dossier app data de l'utilisateur
(Linux : `~/.local/share/archivist/`, macOS : `~/Library/Application Support/archivist/`).

Une fois configuré, les options `--referentiel`, `--root` et `--llm` deviennent optionnelles
dans toutes les commandes.

---

## `archivist scaffold` — Créer l'arborescence de dossiers

Crée l'arborescence cible à partir du référentiel, prête à accueillir vos documents classés.

```bash
archivist scaffold \
  --referentiel file:///chemin/vers/referentiel.yaml \
  --root file:///chemin/vers/mon/drive
```

### Options

| Flag | Requis | Description |
|------|--------|-------------|
| `--referentiel URI` | non* | Chemin vers le fichier `referentiel.yaml` (format `file:///…`) |
| `--root URI` | non* | Dossier racine de l'archive où créer l'arborescence (format `file:///…`) |
| `--option NOM` | non | Option supplémentaire à inclure (répétable). `core` est toujours inclus. |
| `--dry-run` | non | Affiche les dossiers qui seraient créés, sans toucher le disque |

\* Requis si non configuré via `archivist config set`

### Options du référentiel

| Option | Dossiers créés | Cas d'usage |
|--------|----------------|-------------|
| `core` *(toujours actif)* | `Ma banque/`, `Ma fiscalité/`, `Mes achats/`, `Mes ventes/`, `Mon juridique/`, `Archives/` | Tous |
| `assurances` | `Mes assurances/` | RC Pro, mutuelle, assurance locaux |
| `dirigeant-assimile-salarie` | `Mon social/` | Dirigeant SASU assimilé salarié |

### Sortie

La commande écrit sur **stdout** un résumé JSON :

```json
{"created": 24, "skipped": 0, "errors": 0}
```

Le détail de chaque dossier créé ou ignoré est écrit sur **stderr**.

### Idempotence

`scaffold` peut être relancé sur un dossier existant sans risque : les dossiers déjà présents sont ignorés (`skipped`). Si un chemin existe en tant que **fichier** (conflit), l'erreur est comptée et les autres dossiers sont quand même créés.

---

## Exemples

### Installation minimale (core uniquement)

```bash
archivist scaffold \
  --referentiel file:///Users/alice/referentiel.yaml \
  --root file:///Users/alice/Documents/Mon-drive
```

### SASU avec assurances et régime salarié

```bash
archivist scaffold \
  --referentiel file:///Users/alice/referentiel.yaml \
  --root file:///Users/alice/Documents/Mon-drive \
  --option assurances \
  --option dirigeant-assimile-salarie
```

### Vérifier avant de créer

```bash
archivist scaffold \
  --referentiel file:///Users/alice/referentiel.yaml \
  --root file:///Users/alice/Documents/Mon-drive \
  --dry-run
```

Aucun dossier n'est créé. Le résumé indique le nombre de dossiers qui auraient été créés.

---

## `archivist classify` — Classer les documents via LLM

Lit les fichiers de `_Réception`, les sauvegarde dans `_Conservation brut`, les classe
via un LLM et les déplace + renomme selon les conventions du référentiel.

```bash
archivist classify \
  --referentiel file:///chemin/vers/referentiel.yaml \
  --root file:///chemin/vers/mon/drive \
  --llm claude-cli
```

### Options

| Flag | Requis | Description |
|------|--------|-------------|
| `--referentiel URI` | non* | Chemin vers `referentiel.yaml` (`file:///…`) |
| `--root URI` | non* | Dossier racine de l'archive (même convention que `scaffold`/`scan`) |
| `--llm NAME` | non* | Adaptateur LLM. Valeur disponible : `claude-cli` |

\* Requis si non configuré via `archivist config set`

### Adaptateur `claude-cli`

Utilise le binaire `claude` (Claude Code CLI) via la session browser authentifiée.
Aucune clé API requise. Le binaire `claude` doit être disponible dans le `PATH`.

### Sortie

**stdout** — NDJSON : une ligne JSON par fichier traité, puis une ligne de résumé :

```json
{"uri": "file:///…/facture.pdf", "name": "facture.pdf", "status": "classified", "entry_id": "mes_achats.factures_fournisseurs", "dest_name": "2026-03_Facture_OVH_F001.pdf", "dest_uri": "file:///…"}
{"uri": "file:///…/unknown.pdf", "name": "unknown.pdf", "status": "unclassified", "reason": "llm_uncertain: type inconnu"}
{"scanned": 2, "classified": 1, "unclassified": 1, "failed": 0}
```

Valeurs de `status` : `classified` | `unclassified` | `failed`.

**Politique d'erreur :**

| Situation | Fichier |
|---|---|
| Erreur pendant le backup | reste dans `_Réception` |
| LLM incertain (`null`) | déplacé dans `_Non classé` |
| Erreur post-backup | déplacé dans `_Non classé` |
| Succès | déplacé + renommé dans le dossier cible |

### Prérequis

L'archive cible doit contenir les dossiers `_Réception`, `_Conservation brut` et `_Non classé`.
Lancez `archivist scaffold` avant le premier `classify`.
