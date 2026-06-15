# Design — Configuration persistante archivist-cli

**Date :** 2026-06-15
**Statut :** validé

## Contexte

Actuellement, toutes les commandes `archivist` exigent `--referentiel`, `--root` (ex `--target`) et `--llm` à chaque invocation. L'objectif est de persister ces paramètres dans un dossier app data utilisateur afin de ne les fournir qu'une seule fois.

## Paramètres persistables

| Paramètre CLI | Clé config | Description |
|---|---|---|
| `--referentiel` | `referentiel` | URI vers la copie locale du référentiel |
| `--root` | `root` | URI du dossier racine de l'archive documentaire |
| `--llm` | `llm` | Nom de l'adaptateur LLM (ex : `claude-cli`) |

**Règle de priorité :** l'argument CLI a toujours priorité sur la valeur en config.

## Emplacement et format

**Dossier app data :** résolu via `platformdirs.user_data_dir("archivist", "archivist")`.
- Linux : `~/.local/share/archivist/`
- macOS : `~/Library/Application Support/archivist/`
- Windows : `%APPDATA%\archivist\`

**Fichier de config :** `<app_data>/config.yaml`

```yaml
referentiel: "file:///home/user/.local/share/archivist/referentiel.yaml"
root: "file:///home/user/mes-docs"
llm: "claude-cli"
```

**Référentiel installé :** toujours copié à `<app_data>/referentiel.yaml`. Son URI dans `config.yaml` pointe vers cette copie.

## Architecture — Option B retenue

Un module `src/archivist_cli/config.py` sans dépendance au domaine ni aux adapters. La config est de l'infrastructure CLI, pas un port métier — l'hexagone n'est pas étendu.

### `config.py`

```
AppConfig                         dataclass frozen=True
  referentiel: str | None
  root: str | None
  llm: str | None

app_data_dir() -> Path            résolution platformdirs
load_config() -> AppConfig        lit config.yaml, None si absent
save_config(AppConfig) -> None    écrit config.yaml, crée le dossier si besoin
install_referentiel(uri: str) -> str
                                  copie source → <app_data>/referentiel.yaml
                                  retourne l'URI de la copie
                                  lève FileNotFoundError si source absente
```

## Commandes CLI

### `archivist config set <clé> <valeur>`

- `config set referentiel <uri>` : valide l'URI `file://`, copie le fichier vers `<app_data>/referentiel.yaml`, stocke l'URI de la copie dans `config.yaml`
- `config set root <uri>` : valide l'URI `file://`, met à jour `config.yaml`
- `config set llm <nom>` : met à jour `config.yaml`

### `archivist config show`

Affiche le contenu de `config.yaml` en JSON sur stdout :

```json
{
  "referentiel": "file:///home/user/.local/share/archivist/referentiel.yaml",
  "root": "file:///home/user/mes-docs",
  "llm": "claude-cli"
}
```

Les clés absentes de `config.yaml` n'apparaissent pas dans la sortie.

## Intégration dans les commandes existantes

`--target` est renommé `--root` dans `scaffold`, `scan` et `classify` (breaking change assumé).

Tous les paramètres deviennent optionnels. Logique de résolution :

```python
cfg = load_config()
referentiel = referentiel or cfg.referentiel
root = root or cfg.root
if referentiel is None:
    raise click.UsageError(
        "--referentiel manquant. Configurez-le avec :\n"
        "  archivist config set referentiel file:///path/to/referentiel.yaml"
    )
```

## Tests

### `tests/test_config.py` (nouveau)

Utilise `tmp_path` + monkey-patch de `app_data_dir` pour isoler le dossier :

- `load_config()` retourne `AppConfig` vide si aucun fichier
- Round-trip `save_config()` / `load_config()`
- `install_referentiel()` copie le fichier et retourne l'URI correcte

### `tests/test_cli.py` (existant, étendu)

Utilise `CliRunner` + monkey-patch de `app_data_dir` :

- `config set referentiel` copie le fichier et met à jour la config
- `config set root` met à jour la config
- `config show` affiche le JSON attendu
- `scaffold` sans args utilise la config persistée
- `scaffold` avec arg CLI override la config

## Dépendance à ajouter

```
platformdirs>=4.0
```

À ajouter dans `pyproject.toml` de `archivist-cli`.
