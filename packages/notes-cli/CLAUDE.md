# notes-cli

CLI Python — dialogue avec un vault de notes Markdown, architecture hexagonale.

## Stack

- Python ≥ 3.12
- Click (CLI), PyYAML (config)
- Build : hatchling
- Tests : pytest

## Commandes

```bash
uv run pytest tests/                    # tous les tests
uv run pytest tests/domain/             # tests domain uniquement
uv run pytest tests/adapters/           # tests adaptateurs + contrats
uv run pytest tests/application/        # tests use cases
uv run pytest tests/integration/        # tests intégration (I/O réel)
uv run notes --help                     # CLI
```

## Layout

```
src/notes_cli/
  domain/          models.py, ports.py
  application/     (use cases à venir)
  adapters/
    fs/            local.py
    vault/         local_markdown.py
    llm/           (à venir)
  cli.py
  config.py
  registry.py
```

## Conventions (identiques à archivist-cli)

### Imports et types

- `from __future__ import annotations` en tête de chaque fichier
- Dataclasses `frozen=True` pour les modèles du domain
- Type hints partout, pas de `Any` sauf `from_dict` de désérialisation

### Architecture hexagonale

- **domain** ne dépend que de la stdlib
- **application** dépend de domain uniquement
- **adapters** implémentent les ABC de domain
- **cli.py** câble adapters → application — seul point d'assemblage

### Ports

- Chaque port = ABC avec `VERSION: ClassVar[int]`
- Erreurs propres par port (`FilesystemError`, `VaultError`, `LlmError`…)
- URI string partout dans le domain, jamais `pathlib.Path`

### Tests

- Fakes dans `tests/fakes.py`, un fake par port
- Tests domain/application : uniquement des fakes, aucun I/O
- Tests integration : I/O réel, fichiers séparés dans `tests/integration/`

### CLI

- Aucune logique métier dans `cli.py`
- Sortie structurée JSON sur stdout, logs sur stderr

## Candidats à factorisation partagée avec archivist-cli

- `AdapterRegistry` — identique dans les deux CLIs
- `Filesystem` port + `LocalFilesystem` adapter — copie exacte
- Pattern `config.py` (platformdirs + YAML)
