# notes-cli

CLI Python — dialogue avec un vault de notes Markdown, architecture hexagonale.
S'appuie sur le package partagé `cli-core` (ports, registre, adaptateurs communs).

## Stack

- Python ≥ 3.12
- Click (CLI), cli-core (port `ConfigStore`, registre, adaptateurs communs), port propre `Agent` (texte libre + session, dossier de travail fixé à la construction de l'adaptateur)
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
  domain/          ports.py (Agent, AgentReply, AgentError)
  application/     add_idea.py (AddIdea : compose "/add <idée>", délègue à Agent)
  adapters/agent/  claude_code.py (ClaudeCodeAgent : subprocess `claude -p`, cwd = bloc-notes)
  testing/         fakes.py (FakeAgent), contracts.py (AgentContractSuite)
  config.py        AppConfig (agent, bloc_notes)
  registry.py      default_registry (agent/claude-code, config/yaml_file)
  cli.py           notes add idea, notes config set agent|bloc-notes, notes config show
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
- Erreurs propres par port (`AgentError`, `ConfigError`…)
- URI string partout dans le domain, jamais `pathlib.Path`

### Tests

- Fakes : `InMemoryConfigStore` depuis `cli_core.testing` ; `FakeAgent` et `AgentContractSuite` depuis `notes_cli.testing`
- Aucun vrai appel à `claude` dans les tests : `subprocess.run` est remplacé
- Tests domain/application : uniquement des fakes, aucun I/O

### CLI

- Aucune logique métier dans `cli.py`
- Sortie structurée JSON sur stdout, logs sur stderr
