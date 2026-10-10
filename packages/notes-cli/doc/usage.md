# Usage — notes-cli

## Configuration persistante

La CLI peut mémoriser les paramètres récurrents pour éviter de les passer à chaque commande.

### notes config set

```
notes config set llm <nom>     # Mémorise l'adaptateur LLM
```

Un nom inconnu est refusé (code de sortie 2) avec la liste des valeurs possibles
(ex : `claude-cli`). Rien n'est écrit dans ce cas.

### notes config show

Affiche la configuration persistée en JSON :

```
notes config show
```

**Emplacement** : la config est stockée dans le dossier app data de l'utilisateur
(Linux : `~/.local/share/notes/`, macOS : `~/Library/Application Support/notes/`).

### Propriétés

| Propriété | Type | Description |
|-----------|------|-------------|
| `llm`     | string | Nom de l'adaptateur LLM (ex : `claude-cli`) |

### Exemple

```bash
notes config set llm claude-cli
notes config show
# {"llm": "claude-cli"}
```
