# Usage — notes-cli

## Ajouter une idée

`notes add idea` confie une idée au **bloc-notes** : un dossier de l'utilisateur qui contient son `.claude/settings.json`, ses skills, ses hooks et une commande `/add`. C'est le bloc-notes qui challenge l'idée et la range ; la CLI ne fait que le pont, elle ne sait rien du résultat.

Prérequis : `notes config set agent claude-code` et `notes config set bloc-notes <chemin>` (voir plus bas).

### Premier tour

```
notes add idea "<texte de l'idée>"
```

La CLI lance, avec le dossier du bloc-notes comme répertoire courant :

```
claude -p "/add <idée>" --session-id <uuid> --output-format json
```

L'identifiant de session est généré par la CLI avant l'appel.

### Tours suivants

```
notes add idea --session <id> --reply "<réponse>"
```

La CLI lance, toujours dans le dossier du bloc-notes :

```
claude -p "<réponse>" --resume <id> --output-format json
```

`--session` et `--reply` vont ensemble. On fournit soit le texte de l'idée, soit `--session` avec `--reply`, jamais les deux.

### Sortie

Chaque tour affiche un objet JSON sur stdout :

```json
{
  "session": "abc123",
  "reponse": "texte brut renvoyé par le bloc-notes",
  "suite": "notes add idea --session abc123 --reply \"<ta réponse>\""
}
```

| Champ | Description |
|-------|-------------|
| `session` | Identifiant de la session, à repasser à `--session` au tour suivant |
| `reponse` | Texte brut de la réponse du bloc-notes |
| `suite` | Commande à utiliser pour répondre ; toujours présent |

La CLI ne cherche pas à savoir si l'idée a été déposée ou si le bloc-notes pose une question : c'est à l'appelant d'en juger à la lecture de `reponse`. S'il s'agit d'une question, l'appelant répond lui-même ou la remonte à l'humain, puis relance la commande indiquée par `suite`.

### Exemple de boucle question/réponse

```bash
notes add idea "Suivre les podcasts de Kristine"
# {"session": "abc123", "reponse": "C'est pour ta veille ou pour une idée de contenu ?", "suite": "notes add idea --session abc123 --reply \"<ta réponse>\""}

notes add idea --session abc123 --reply "Pour ma veille"
# {"session": "abc123", "reponse": "Idée déposée dans l'inbox.", "suite": "notes add idea --session abc123 --reply \"<ta réponse>\""}
```

### Erreurs

Les erreurs sont écrites sur stderr, sans trace d'exécution.

| Situation | Code |
|-----------|------|
| `bloc-notes` non configuré (le message indique `notes config set bloc-notes <chemin>`) | 1 |
| `agent` non configuré (le message indique `notes config set agent claude-code`) | 1 |
| Dossier du bloc-notes configuré mais introuvable au moment de l'appel | 1 |
| `claude` absent du PATH, code retour non nul, délai dépassé (600 s), JSON illisible, `is_error` vrai | 1 |
| Ni texte d'idée ni `--reply` ; texte d'idée et `--reply` ensemble ; `--reply` sans `--session` (ou inversement) ; texte d'idée vide | 2 |

Quand l'échec survient pendant l'appel à `claude` (délai dépassé, code retour non nul…), le message d'erreur donne l'identifiant de session et la commande `notes add idea --session <id> --reply "<ta réponse>"` pour reprendre la conversation, car `/add` a pu écrire dans `inbox/` avant l'interruption.

> **Permissions d'écriture.** Les autorisations d'écriture dans `inbox/` relèvent du bloc-notes, dans son `.claude/settings.json`. Or `claude -p` n'applique ce fichier que si le dossier est approuvé (« trusted ») : lancer une fois `claude` en interactif dans le dossier du bloc-notes et accepter l'invite de confiance. La CLI ne passe aucun drapeau de permission. Sans cela, `/add` peut échouer à écrire et ne le signaler que dans `reponse`.

> **Délai pour l'appelant.** Le bloc-notes peut réfléchir longtemps : la CLI attend jusqu'à 600 s (10 min) la réponse de `claude`. Un agent appelant doit lancer `notes add idea` avec un délai d'outil shell d'au moins 10 minutes.

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
notes config set bloc-notes ~/bloc-notes
notes config show
# {"agent": "claude-code", "bloc-notes": "/home/<user>/bloc-notes"}
```
