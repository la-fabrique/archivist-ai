# Architecture — `notes-cli`

Ce document décrit l'architecture de la CLI `notes-cli` : son périmètre actuel, ses couches, ce qu'elle emprunte à `cli-core`, sa frontière CLI et sa configuration. Stack, commandes et conventions de code sont dans [`packages/notes-cli/CLAUDE.md`](../../packages/notes-cli/CLAUDE.md), l'usage dans [`packages/notes-cli/doc/usage.md`](../../packages/notes-cli/doc/usage.md).

---

## 1. Périmètre & non-objectifs

`notes-cli` est une CLI Python destinée à dialoguer avec un vault de notes Markdown. Comme `archivist-cli`, elle est agent-first : JSON sur stdout, logs sur stderr.

### Dans le périmètre actuel
- Le squelette hexagonal de la CLI, branché sur [`cli-core`](cli-core.md).
- La configuration persistante du LLM : `notes config set llm` et `notes config show`.

### Hors périmètre actuel (l'archi ne doit pas s'y opposer)
- Toute commande métier : vault, lecture et écriture de notes, dialogue avec le LLM.
- La notion de vault elle-même. Elle arrivera avec la première feature métier, avec ses ports (accès aux notes, par exemple) et sa clé de config.

---

## 2. Architecture en ports & adaptateurs

Les cercles sont les mêmes que dans `archivist-cli`. Les ports et adaptateurs utilisés aujourd'hui viennent tous de `cli-core`.

```
┌──────────────────────────────────────────────────────┐
│  Frontière CLI  (Click)                              │
│  ┌────────────────────────────────────────────────┐  │
│  │  Application  (use cases — à venir)            │  │
│  │  ┌──────────────────────────────────────────┐  │  │
│  │  │  Domain  (ports ré-exportés)             │  │  │
│  │  │  LanguageModel, LlmError                 │  │  │
│  │  └──────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────┘  │
│  Adapters  (fournis par cli-core)                    │
│  llm/claude-cli, config/yaml_file                    │
└──────────────────────────────────────────────────────┘
```

### Règles de dépendance
- `domain` ne dépend que de la stdlib et des ports stdlib ré-exportés depuis `cli_core.domain`.
- `application` dépend de `domain` uniquement.
- Les adaptateurs propres à notes-cli, quand il y en aura, dépendront de `domain` pour implémenter ses ABC.
- `registry.py` est le seul module qui importe des adaptateurs, ceux de `cli-core` compris.
- `cli.py` câble registre → application. C'est le seul point d'assemblage.
- **Aucune flèche inverse**, et `cli-core` n'importe jamais `notes_cli`.

### Layout (`src/notes_cli/`)

```
domain/          ports.py      ré-export LanguageModel, LlmError depuis cli_core
application/                   use cases à venir
config.py        AppConfig
registry.py      default_registry
cli.py           groupe Click `notes`
```

Tant qu'aucune feature métier n'existe, le dossier `adapters/` n'existe pas non plus. Un port n'entre dans `cli-core` que s'il sert à au moins deux CLIs : les ports propres au vault vivront donc d'abord dans `notes_cli.domain`.

---

## 3. Registre

`default_registry` est une instance de `cli_core.registry.AdapterRegistry`. Il enregistre :

| Clé | Adaptateur | Configuration de la factory |
|---|---|---|
| `llm/claude-cli` | `ClaudeCliLlm` | — |
| `config/yaml_file` | `YamlFileConfigStore` | `app_name` (`"notes"`), `data_dir` optionnel |

La liste des LLM acceptés par `config set llm` vient de `default_registry.names("llm")`. Ajouter un adaptateur LLM au registre suffit à le rendre configurable.

---

## 4. Frontière CLI & configuration

**Rôle de Click :** parser les arguments, résoudre les adaptateurs via le registre, exécuter, formater la sortie. **Aucune logique métier dans `cli.py`.**

### Commandes implémentées
- `notes config set llm <nom>` valide le nom contre le registre, puis persiste la valeur. Sortie : `{"llm": "<nom>"}`.
- `notes config show` affiche la config persistée en JSON.

### Configuration persistante
- **Schéma** : `AppConfig` (dataclass `frozen`), qui ne contient pour l'instant que `llm: str | None`. `from_dict` et `to_dict` assurent la conversion avec le `dict[str, str]` opaque du `ConfigStore`.
- **Stockage** : `YamlFileConfigStore("notes")`, dans `<user_data_dir("notes", "notes")>/config.yaml`.
- **Écriture** : lecture de la config → `dataclasses.replace` → `save`. Le store remplace la config entière, et les clés que `AppConfig` ignore ne sont pas conservées.

### Sortie et erreurs
- Stdout : un objet JSON par commande.
- Nom d'adaptateur inconnu : `click.BadParameter`, code de sortie 2, rien n'est écrit.
- `ConfigError` (config illisible ou invalide, écriture impossible) : convertie en `click.ClickException`, code de sortie 1, message sur stderr.

---

## 5. Tests

- **Domain et application** : uniquement des fakes importés depuis `cli_core.testing` (`InMemoryConfigStore`, `FakeLlm`), sans aucune I/O.
- **Config** : aller-retour `AppConfig.from_dict` / `to_dict`.
- **CLI** : tests `CliRunner`, avec `_config_store` remplacé par un `InMemoryConfigStore`. Les cas d'erreur (YAML corrompu, valeur non textuelle) et le câblage du chemin passent par un `YamlFileConfigStore` sur un dossier temporaire.
- Les contrats des adaptateurs sont vérifiés dans `cli-core`, pas ici.

---

## 6. Livraison

Le binaire standalone est construit avec PyInstaller (`npm run notes-cli:build` → `packages/notes-cli/dist/`). La CI tourne sur chaque modification de `packages/notes-cli/**` ou de `packages/cli-core/**`. Les releases multi-OS sont taguées `notes-cli/<MAJOR>.<DATE>.<N>`.
