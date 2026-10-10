# cli-core

Package Python partagé entre `archivist-cli` et `notes-cli` : ports, adaptateurs et registre communs (architecture hexagonale). Décision : [ADR-013](../../docs/architecture/adrs/2026-10-10-ADR-013-package-partage-cli-core.md).

## Stack

- Python ≥ 3.12
- PyYAML, platformdirs
- Build : hatchling
- Tests : pytest

## Commandes

```bash
uv run pytest tests/                    # tous les tests
uv run pytest tests/adapters/           # adaptateurs + contrats
```

## Layout

```
src/cli_core/
  domain/          ports.py (LanguageModel, LlmError, ConfigStore, ConfigError)
  adapters/
    llm/           claude_cli.py
    config/        yaml_file.py
  registry.py      AdapterRegistry, UnknownAdapterError, AdapterFactory
  testing/         fakes.py, contracts.py (importables par les tests des CLIs)
```

## Règles de dépendance

- `cli_core.domain` → stdlib uniquement
- `cli_core.adapters` → `cli_core.domain` + libs tierces
- `cli_core` n'importe jamais `archivist_cli` ni `notes_cli`, et ne contient aucune notion métier (référentiel, vault, `AppConfig`)
- cli-core fournit le mécanisme, chaque CLI déclare le contenu : `ConfigStore` manipule un `dict[str, str]` opaque, `AdapterRegistry` est vide (chaque CLI construit son `default_registry`)

## Règle de factorisation

On ne factorise un port dans cli-core que lorsqu'au moins deux CLIs l'utilisent.

## Conventions

- `from __future__ import annotations` en tête de chaque fichier
- Type hints partout, pas de `Any` sauf factories du registre
- Chaque port = ABC avec `VERSION: ClassVar[int]`
- Erreurs propres par port (`LlmError`, `ConfigError`), jamais d'exception générique
- Fakes dans `cli_core.testing` (un fake par port) ; tests de contrat via mixin `*ContractSuite`
- Chaque adaptateur (built-in + fake) doit passer la suite de contrat de son port
