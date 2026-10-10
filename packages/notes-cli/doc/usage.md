# Usage — notes-cli

## Configuration persistante

La CLI peut mémoriser les paramètres récurrents pour éviter de les passer à chaque commande.

### notes config set

```
notes config set vault <uri>   # Mémorise le chemin du vault de notes
notes config set llm <nom>     # Mémorise l'adaptateur LLM
```

### notes config show

Affiche la configuration persistée en JSON :

```
notes config show
```

**Emplacement** : la config est stockée dans le dossier app data de l'utilisateur
(Linux : `~/.local/share/notes/`, macOS : `~/Library/Application Support/notes/`).

Une fois configuré, l'option `--vault` devient optionnelle dans toutes les commandes.

### Propriétés

| Propriété | Type | Description |
|-----------|------|-------------|
| `vault`   | URI `file://` | Chemin absolu vers le dossier racine du vault de notes |
| `llm`     | string | Nom de l'adaptateur LLM (ex : `claude-cli`) |

### Exemple

```bash
notes config set vault file:///Users/alice/Notes
notes config set llm claude-cli
notes config show
# {"vault": "file:///Users/alice/Notes", "llm": "claude-cli"}
```
