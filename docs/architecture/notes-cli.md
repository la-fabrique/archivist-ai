# Architecture — `notes-cli`

Ce document décrit l'architecture de la CLI `notes-cli` : son périmètre actuel, ses couches, ce qu'elle emprunte à `cli-core`, sa frontière CLI et sa configuration. Stack, commandes et conventions de code sont dans [`packages/notes-cli/CLAUDE.md`](../../packages/notes-cli/CLAUDE.md), l'usage dans [`packages/notes-cli/doc/usage.md`](../../packages/notes-cli/doc/usage.md).

---

## 1. Périmètre & non-objectifs

`notes-cli` est une CLI Python destinée à dialoguer avec un vault de notes Markdown. Comme `archivist-cli`, elle est agent-first : JSON sur stdout, logs sur stderr.

### Dans le périmètre actuel
- Le squelette hexagonal de la CLI, branché sur [`cli-core`](cli-core.md).
- La configuration persistante : `notes config set agent`, `notes config set bloc-notes` et `notes config show`.
- Le premier cas d'usage métier, `notes add idea` : capturer une idée et la confier au **bloc-notes**, un dossier de l'utilisateur (réglages, skills, hooks, commande `/add`) qui la challenge et la range. La CLI sert de pont : elle sait où est le bloc-notes et comment y lancer l'agent, pas ce qu'il advient de l'idée. L'échange se fait par tours, une invocation par tour, pour qu'un agent appelant sans terminal interactif puisse le mener.

### Hors périmètre actuel (l'archi ne doit pas s'y opposer)
- Toute logique sur le contenu des idées (critères, catégories, format d'entrée d'inbox) : elle vit dans le bloc-notes.
- La gestion de plusieurs bloc-notes, et les permissions Claude du bloc-notes (déclarées dans son `.claude/settings.json`).
- La notion de vault elle-même. Elle arrivera avec une feature de lecture et écriture de notes, avec ses ports et sa clé de config.

---

## 2. Architecture en ports & adaptateurs

Les cercles sont les mêmes que dans `archivist-cli`. Le port `Agent` et son adaptateur sont propres à notes-cli ; le registre et le config store viennent de `cli-core`.

```
┌──────────────────────────────────────────────────────┐
│  Frontière CLI  (Click)                              │
│  ┌────────────────────────────────────────────────┐  │
│  │  Application  (AddIdea)                        │  │
│  │  ┌──────────────────────────────────────────┐  │  │
│  │  │  Domain  (ports)                         │  │  │
│  │  │  Agent, AgentReply, AgentError           │  │  │
│  │  └──────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────┘  │
│  Adapters                                            │
│  agent/claude-code (notes-cli)                       │
│  config/yaml_file (cli-core)                         │
└──────────────────────────────────────────────────────┘
```

### Règles de dépendance
- `domain` ne dépend que de la stdlib.
- `application` dépend de `domain` uniquement.
- Les adaptateurs propres à notes-cli (`adapters/`) dépendent de `domain` pour implémenter ses ABC.
- `registry.py` est le seul module qui importe des adaptateurs, ceux de `cli-core` compris.
- `cli.py` câble registre → application. C'est le seul point d'assemblage.
- **Aucune flèche inverse**, et `cli-core` n'importe jamais `notes_cli`.

### Layout (`src/notes_cli/`)

```
domain/ports.py              Agent, AgentReply, AgentError
application/add_idea.py      AddIdea : compose "/add <idée>", délègue à Agent
adapters/agent/claude_code.py  ClaudeCodeAgent(workspace)
testing/                     FakeAgent, AgentContractSuite
config.py        AppConfig
registry.py      default_registry
cli.py           groupe Click `notes`
```

Un port n'entre dans `cli-core` que s'il sert à au moins deux CLIs : `Agent` n'est utilisé que par notes-cli, il vit donc dans `notes_cli.domain`. `LanguageModel` (prompt + schéma, un seul appel) reste dans `cli-core` pour archivist-cli et n'est pas utilisé ici.

### Port `Agent`

`send(message, session_id=None) -> AgentReply` envoie un message à un agent installé dans un dossier. Sans `session_id`, une nouvelle session démarre ; avec, elle est reprise. `AgentReply` porte `session_id` et `text`. Toute erreur d'appel ou de réponse inexploitable lève `AgentError`, qui porte un `session_id` optionnel pour permettre de reprendre la conversation.

Le dossier de travail est fixé à la construction de l'adaptateur (clé `workspace`), pas passé à chaque appel : le domaine ne connaît ni le chemin ni Claude. Le contrat « le bloc-notes expose `/add` » vit dans le use case `AddIdea`, pas dans le port : une future commande n'ajoute qu'un use case.

`ClaudeCodeAgent` exécute `claude -p` avec le bloc-notes comme répertoire courant. Au premier tour il génère un UUID et le passe via `--session-id` ; aux tours suivants il utilise `--resume <id>`. Le message est placé en dernier, après `--`, pour qu'un texte commençant par `-` ne soit pas lu comme une option ; stdin du sous-process est fermé (`DEVNULL`). Il retire `CLAUDECODE` de l'environnement transmis (un appelant Claude Code ne bloque pas le `claude` imbriqué), applique un délai de 600 s, et lit `result`, `session_id` et `is_error` dans le JSON renvoyé.

---

## 3. Registre

`default_registry` est une instance de `cli_core.registry.AdapterRegistry`. Il enregistre :

| Clé | Adaptateur | Configuration de la factory |
|---|---|---|
| `agent/claude-code` | `ClaudeCodeAgent` | `workspace` |
| `config/yaml_file` | `YamlFileConfigStore` | `app_name` (`"notes"`), `data_dir` optionnel |

La liste des agents acceptés par `config set agent` vient de `default_registry.names("agent")`. Ajouter un adaptateur d'agent au registre suffit à le rendre configurable.

---

## 4. Frontière CLI & configuration

**Rôle de Click :** parser les arguments, résoudre les adaptateurs via le registre, exécuter, formater la sortie. **Aucune logique métier dans `cli.py`.**

### Commandes implémentées
- `notes config set agent <nom>` valide le nom contre le registre, puis persiste la valeur. Sortie : `{"agent": "<nom>"}`.
- `notes config set bloc-notes <chemin>` normalise le chemin (`expanduser` puis `abspath`), exige un dossier existant, puis persiste. Sortie : `{"bloc-notes": "<chemin absolu>"}`.
- `notes config show` affiche la config persistée en JSON.
- `notes add idea "<idée>"` (premier tour) et `notes add idea --session <id> --reply "<réponse>"` (tours suivants) construisent `AddIdea` avec l'agent résolu depuis la config, et affichent `{session, reponse, suite}`. La CLI ne cherche pas à savoir si l'idée a été déposée.

### Configuration persistante
- **Schéma** : `AppConfig` (dataclass `frozen`), avec `agent: str | None` et `bloc_notes: str | None` (clés YAML `agent` et `bloc-notes`). `from_dict` et `to_dict` assurent la conversion avec le `dict[str, str]` opaque du `ConfigStore`.
- **Stockage** : `YamlFileConfigStore("notes")`, dans `<user_data_dir("notes", "notes")>/config.yaml`.
- **Écriture** : lecture de la config → `dataclasses.replace` → `save`. Le store remplace la config entière, et les clés que `AppConfig` ignore ne sont pas conservées.

### Sortie et erreurs
- Stdout : un objet JSON par commande.
- Nom d'adaptateur inconnu, ou chemin de bloc-notes qui n'est pas un dossier : `click.BadParameter`, code de sortie 2, rien n'est écrit.
- Mauvaise combinaison d'arguments de `add idea` : `click.UsageError`, code de sortie 2.
- Agent ou bloc-notes non configuré, dossier du bloc-notes disparu, `AgentError` : `click.ClickException`, code de sortie 1. Si l'`AgentError` porte un `session_id`, le message donne la commande pour reprendre la session.
- `ConfigError` (config illisible ou invalide, écriture impossible) : convertie en `click.ClickException`, code de sortie 1, message sur stderr.

---

## 5. Tests

- **Domain et application** : uniquement des fakes, sans aucune I/O : `InMemoryConfigStore` depuis `cli_core.testing`, `FakeAgent` (réponses scriptées, appels enregistrés avec leur `session_id`) depuis `notes_cli.testing`.
- **Contrat** : `AgentContractSuite` (`notes_cli.testing`) est un mixin pytest qui doit passer pour `FakeAgent` et pour `ClaudeCodeAgent`. Pour ce dernier, `subprocess.run` est remplacé (aucun vrai appel à `claude`) et les tests vérifient notamment `cwd` et l'absence de `CLAUDECODE` dans `env`.
- **Config** : aller-retour `AppConfig.from_dict` / `to_dict`.
- **CLI** : tests `CliRunner`, avec `_config_store` remplacé par un `InMemoryConfigStore`. Les cas d'erreur (YAML corrompu, valeur non textuelle) et le câblage du chemin passent par un `YamlFileConfigStore` sur un dossier temporaire.
- Les contrats des adaptateurs de `cli-core` sont vérifiés dans `cli-core` ; celui de l'adaptateur d'agent l'est ici.

---

## 6. Livraison

Le binaire standalone est construit avec PyInstaller (`npm run notes-cli:build` → `packages/notes-cli/dist/`). La CI tourne sur chaque modification de `packages/notes-cli/**` ou de `packages/cli-core/**`. Les releases multi-OS sont taguées `notes-cli/<MAJOR>.<DATE>.<N>`.
