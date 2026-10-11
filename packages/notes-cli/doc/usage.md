# Usage — notes-cli

## Configuration persistante

La CLI peut mémoriser les paramètres récurrents pour éviter de les passer à chaque commande.

### notes config set

```
notes config set agent <nom>         # Mémorise l'agent
notes config set bloc-notes <chemin> # Mémorise le dossier du bloc-notes
```

Un nom d'agent inconnu est refusé (code de sortie 2) avec la liste des valeurs possibles
(ex : `claude-code`). Le chemin du bloc-notes est converti en chemin absolu (`~` développé) ;
s'il n'est pas un dossier existant, il est refusé (code 2). Rien n'est écrit dans ces cas.

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
| `agent`   | string | Nom de l'adaptateur d'agent (ex : `claude-code`) |
| `bloc-notes` | string | Chemin absolu du dossier du bloc-notes |

### Exemple

```bash
notes config set agent claude-code
notes config show
# {"agent": "claude-code"}
```
