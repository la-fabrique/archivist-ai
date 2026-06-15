# Usage — archivist-cli

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
| `--referentiel URI` | oui | Chemin vers le fichier `referentiel.yaml` (format `file:///…`) |
| `--root URI` | oui | Dossier racine de l'archive où créer l'arborescence (format `file:///…`) |
| `--option NOM` | non | Option supplémentaire à inclure (répétable). `core` est toujours inclus. |
| `--dry-run` | non | Affiche les dossiers qui seraient créés, sans toucher le disque |

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
| `--referentiel URI` | oui | Chemin vers `referentiel.yaml` (`file:///…`) |
| `--root URI` | oui | Dossier racine de l'archive (même convention que `scaffold`/`scan`) |
| `--llm NAME` | oui | Adaptateur LLM. Valeur disponible : `claude-cli` |

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
