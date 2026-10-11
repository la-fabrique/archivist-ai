# notes-cli

CLI Python — dialogue avec un vault de notes Markdown, architecture hexagonale.
S'appuie sur le package partagé `cli-core` (ports, registre, adaptateurs communs).

## Stack

- Python ≥ 3.12
- Click (CLI), cli-core (ports `LanguageModel`/`ConfigStore`, registre, adaptateurs)
- Build : hatchling
- Tests : pytest

## Commandes

```bash
uv run pytest tests/                    # tous les tests
uv run notes --help                     # CLI
```

## Layout

```
src/notes_cli/
  domain/          ports.py (ré-export LanguageModel, LlmError depuis cli_core)
  application/     (use cases à venir)
  config.py        AppConfig (agent, bloc-notes)
  registry.py      default_registry (agent/claude-code, config/yaml_file)
  cli.py
```

## Conventions (identiques à archivist-cli)

### Imports et types

- `from __future__ import annotations` en tête de chaque fichier
- Dataclasses `frozen=True` pour les modèles du domain
- Type hints partout, pas de `Any` sauf `from_dict` de désérialisation

### Architecture hexagonale

- **domain** ne dépend que de la stdlib et des ports stdlib ré-exportés depuis `cli_core.domain`
- **application** dépend de domain uniquement
- **adapters** implémentent les ABC de domain
- **cli.py** câble adapters → application — seul point d'assemblage

### Ports

- Chaque port = ABC avec `VERSION: ClassVar[int]`
- Erreurs propres par port (`LlmError`, `ConfigError`…)
- URI string partout dans le domain, jamais `pathlib.Path`

### Tests

- Fakes importés depuis `cli_core.testing` (ex : `InMemoryConfigStore`)
- Tests domain/application : uniquement des fakes, aucun I/O

### CLI

- Aucune logique métier dans `cli.py`
- Sortie structurée JSON sur stdout, logs sur stderr
