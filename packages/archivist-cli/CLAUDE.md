# archivist-cli

CLI Python — classement automatique de documents via architecture hexagonale.

## Stack

- Python ≥ 3.12
- Click (CLI), PyYAML (référentiel)
- Build : hatchling
- Tests : pytest

## Commandes

```bash
uv run pytest tests/                    # tous les tests
uv run pytest tests/domain/             # tests domain uniquement
uv run pytest tests/adapters/           # tests adaptateurs + contrats
uv run pytest tests/application/        # tests use cases
uv run pytest tests/integration/        # tests intégration (I/O réel)
uv run archivist --help                 # CLI
```

## Layout

```
src/archivist_cli/
  domain/          models.py, ports.py
  application/     classify.py, scaffold.py, audit.py
  adapters/
    fs/            local.py
    ocr/           tesseract.py
    llm/           openai.py
    referentiel/   yaml_file.py
    index/         noop.py
  cli.py
  registry.py
```

## Conventions

### Imports et types

- `from __future__ import annotations` en tête de chaque fichier
- Dataclasses `frozen=True` pour les modèles du domain
- Type hints partout, pas de `Any` sauf `from_dict` de désérialisation

### Architecture hexagonale

- **domain** ne dépend que de la stdlib
- **application** dépend de domain uniquement
- **adapters** implémentent les ABC de domain
- **cli.py** câble adapters → application — seul point d'assemblage
- Aucune flèche inverse : adapter n'importe jamais un use case, domain n'importe jamais un adapter

### Ports

- Chaque port = ABC avec `VERSION: ClassVar[int]`
- Erreurs propres par port (`FilesystemError`, `OcrError`, `LlmError`…), jamais d'exception générique
- URI string partout dans le domain, jamais `pathlib.Path`

### Tests

- Fakes dans `tests/fakes.py`, un fake par port
- Tests de contrat via mixin `*ContractSuite` dans `tests/adapters/test_contracts.py`
- Chaque adaptateur (built-in + fake) doit passer la suite de contrat de son port
- Tests domain/application : uniquement des fakes, aucun I/O
- Tests integration : I/O réel, fichiers séparés dans `tests/integration/`

### CLI

- Aucune logique métier dans `cli.py`
- Sortie structurée JSON sur stdout, logs sur stderr
