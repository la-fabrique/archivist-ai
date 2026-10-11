# Architecture — `cli-core`

Ce document décrit le package Python partagé `cli-core` : ce qu'il contient, ce qu'il s'interdit de contenir, et comment les CLIs le consomment. Stack, commandes et conventions de code sont dans [`packages/cli-core/CLAUDE.md`](../../packages/cli-core/CLAUDE.md).

---

## 1. Périmètre & non-objectifs

`cli-core` est une **bibliothèque**, pas une CLI : il n'a ni point d'entrée ni binaire. Il factorise les briques techniques communes à `archivist-cli` et `notes-cli`, dans la même architecture hexagonale.

### Dans le périmètre
- Ports transverses : `LanguageModel`, `ConfigStore`.
- Adaptateurs built-in de ces ports : `ClaudeCliLlm`, `YamlFileConfigStore`.
- Le mécanisme de registre d'adaptateurs : `AdapterRegistry`.
- L'outillage de test des ports : fakes et suites de contrat.

### Non-objectifs
- **Aucune notion métier** : pas de référentiel, de vault, de note ni de document. Pas non plus d'`AppConfig` : le schéma de la config appartient à chaque CLI.
- **Aucun câblage** : `cli-core` ne choisit jamais quel adaptateur utiliser.
- **Aucun port spéculatif** : un port n'est factorisé ici que lorsqu'au moins deux CLIs l'utilisent. `Filesystem`, `Referentiel`, `MetadataExtractor`, `Index` et `AuditLog` restent donc dans `archivist-cli`.

---

## 2. Principe : le mécanisme ici, le contenu dans la CLI

| Brique | `cli-core` fournit | Chaque CLI déclare |
|---|---|---|
| Registre | `AdapterRegistry` vide (`register`, `resolve`, `names`) | Son `default_registry` et les adaptateurs qu'il expose |
| Config | `ConfigStore` sur un `dict[str, str]` opaque + adaptateur YAML | Son `AppConfig` (clés, types, valeurs par défaut) et son `app_name` |
| LLM | Port `LanguageModel` + `ClaudeCliLlm` | Les prompts, les schémas de sortie et les use cases qui les appellent |

---

## 3. Dépendances

```
archivist-cli ──┐
                ├──►  cli-core   (dépendance path éditable, un uv.lock par CLI)
notes-cli ──────┘
```

### Règles de dépendance
- `cli_core.domain` → stdlib uniquement.
- `cli_core.adapters` → `cli_core.domain` + libs tierces (`pyyaml`, `platformdirs`, sous-process `claude`).
- `cli_core.registry` → stdlib uniquement ; les factories sont fournies par les CLIs.
- `cli_core.testing` → `cli_core.domain` + `pytest`.
- **Aucune flèche inverse** : `cli_core` n'importe jamais `archivist_cli` ni `notes_cli`.

Côté CLI, le domain peut **ré-exporter** les ports de `cli_core.domain`. Ils restent purement stdlib, donc la règle « le domain ne dépend que de la stdlib » tient toujours. Les adaptateurs de `cli-core` ne sont importés que par le `registry.py` de chaque CLI.

### Layout (`src/cli_core/`)

```
domain/          ports.py      LanguageModel, LlmError, ConfigStore, ConfigError
adapters/
  llm/           claude_cli.py
  config/        yaml_file.py
registry.py      AdapterRegistry, UnknownAdapterError, AdapterFactory
testing/         fakes.py, contracts.py
```

---

## 4. Catalogue des ports

Chaque port est une ABC avec `VERSION: ClassVar[int]` et une erreur qui lui est propre.

### `LanguageModel` (v1)
`complete(prompt, output_schema) -> dict` renvoie un dict conforme au schéma JSON fourni. Toute erreur d'appel ou de parsing lève `LlmError`.
- `ClaudeCliLlm` appelle `claude -p` en sous-process (timeout 60 s), retire les fences Markdown, parse le JSON puis vérifie les champs requis et les types déclarés.

### `ConfigStore` (v1)
- `load() -> dict[str, str]` renvoie `{}` si aucune config n'existe.
- `save(data)` **remplace** intégralement la config (pas de fusion).
- Toute erreur d'I/O, de format ou d'encodage lève `ConfigError`.
- `YamlFileConfigStore(app_name, data_dir=None)` stocke dans `<user_data_dir(app_name, app_name)>/config.yaml`. Fichier absent ou vide → `{}`. Une valeur `null` est ignorée. Un non-mapping, une valeur non textuelle ou un fichier non UTF-8 → `ConfigError`.

---

## 5. Registre

`AdapterRegistry` associe une clé `<port>/<nom>` (ex. `llm/claude-cli`) à une factory `dict -> adaptateur`.
- `resolve(port, nom, config)` instancie l'adaptateur. Un nom inconnu lève `UnknownAdapterError`.
- `names(port)` liste les noms enregistrés pour un port, triés. Les CLIs s'en servent pour valider une saisie utilisateur, comme `archivist config set llm`.

Le registre partagé est vide. Chaque CLI construit son `default_registry` dans `registry.py`, et c'est le seul endroit qui changera le jour où des plugins externes seront ouverts.

---

## 6. Tests

`cli_core.testing` est livré **dans le package** pour que les CLIs réutilisent les fakes au lieu de les dupliquer.
- **Fakes** : `FakeLlm` (réponses scriptées, prompts enregistrés dans `calls`, `LlmError` injectable) et `InMemoryConfigStore`.
- **Suites de contrat** : `LanguageModelContractSuite` (fixture `llm`) et `ConfigStoreContractSuite` (fixture `store`) sont des mixins pytest. Chaque adaptateur, built-in comme fake, doit passer la suite de son port.

---

## 7. Livraison

`cli-core` n'est pas publié seul. Il est embarqué dans le binaire de chaque CLI. Un changement de `cli-core` sur `main` déclenche donc une nouvelle release de chacune des CLIs qui le consomment.
