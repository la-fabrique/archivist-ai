# Usage — archivist-cli

## `archivist scaffold` — Créer l'arborescence de dossiers

Crée l'arborescence cible à partir du référentiel, prête à accueillir vos documents classés.

```bash
archivist scaffold \
  --referentiel file:///chemin/vers/referentiel.yaml \
  --target file:///chemin/vers/mon/drive
```

### Options

| Flag | Requis | Description |
|------|--------|-------------|
| `--referentiel URI` | oui | Chemin vers le fichier `referentiel.yaml` (format `file:///…`) |
| `--target URI` | oui | Dossier cible où créer l'arborescence (format `file:///…`) |
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
  --target file:///Users/alice/Documents/Mon-drive
```

### SASU avec assurances et régime salarié

```bash
archivist scaffold \
  --referentiel file:///Users/alice/referentiel.yaml \
  --target file:///Users/alice/Documents/Mon-drive \
  --option assurances \
  --option dirigeant-assimile-salarie
```

### Vérifier avant de créer

```bash
archivist scaffold \
  --referentiel file:///Users/alice/referentiel.yaml \
  --target file:///Users/alice/Documents/Mon-drive \
  --dry-run
```

Aucun dossier n'est créé. Le résumé indique le nombre de dossiers qui auraient été créés.
