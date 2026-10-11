---
name: note-add
description: Confie une idée au bloc-notes de l'utilisateur via la CLI notes, en relayant les questions du bloc-notes jusqu'au dépôt. Utiliser quand l'utilisateur veut noter, déposer ou garder une idée.
argument-hint: <idée>
allowed-tools: Bash(notes *)
---

# Déposer une idée dans le bloc-notes

Tu fais le pont entre l'utilisateur et son bloc-notes. C'est le bloc-notes qui challenge et range l'idée ; toi, tu transmets, tu montres, tu attends.

Lance chaque commande `notes add idea` avec un délai d'outil Bash de 600000 ms : le bloc-notes peut réfléchir jusqu'à 10 minutes.

## 1. Premier tour

L'idée est `$ARGUMENTS`. Si elle est vide, demande-la à l'utilisateur et attends sa réponse.

Passe le texte exact par un heredoc à délimiteur entre guillemets, pour que le shell n'interprète ni `$`, ni `"`, ni les backticks :

````
notes add idea -- "$(cat <<'IDEE'
<texte exact de l'idée>
IDEE
)"
````

Garde le `--` : sans lui, une idée qui commence par `-` serait prise pour une option. Ne reformule pas l'idée. Si le texte contient une ligne réduite à `IDEE`, choisis un autre délimiteur.

## 2. Lire le JSON

La sortie standard est un objet JSON : `session`, `reponse`, `suite`.

## 3. Montrer `reponse` telle quelle

Affiche `reponse` à l'utilisateur mot pour mot, sans la reformuler, la résumer ni la commenter.

`suite` est toujours présent : il ne dit pas si l'échange est fini. Juge à la lecture de `reponse` :

- une **question** attend une réponse de l'utilisateur ;
- une **confirmation** annonce que l'idée a été déposée ou rangée.

En cas de doute, traite `reponse` comme une question et demande à l'utilisateur.

## 4. Si c'est une question du bloc-notes

Arrête-toi et attends la réponse de l'utilisateur. Ne réponds **jamais** à sa place, même si le contexte permet de deviner la réponse.

Quand l'utilisateur a répondu, transmets son texte exact :

````
notes add idea --session <session> --reply "$(cat <<'REPONSE'
<texte exact de la réponse>
REPONSE
)"
````

Puis reprends à l'étape 2.

## 5. Si c'est une confirmation de dépôt

Termine. Ne lance pas d'autre tour.

## 6. Erreurs

En cas d'échec, le message est sur stderr. Après un `notes config set …`, ne relance le tour qu'une seule fois. Si la même erreur de configuration revient, affiche-la et arrête-toi.

Selon le code de sortie et le message :

- **Code 1, message contenant `notes config set agent`** : lance `notes config set agent claude-code` sans demander, puis relance le tour en cours.
- **Code 1, message contenant `notes config set bloc-notes`, ou indiquant que le dossier du bloc-notes n'existe plus** : demande à l'utilisateur le chemin de son bloc-notes, lance `notes config set bloc-notes "<chemin>"`, puis relance le tour en cours. Si le chemin contient `"`, `$` ou un backtick, passe-le par un heredoc à délimiteur entre guillemets comme à l'étape 1.
- **Code 1, échec pendant l'appel à l'agent (le message contient `--session`)** : affiche l'erreur et propose à l'utilisateur de reprendre avec la commande indiquée. Ne relance pas tout seul : le bloc-notes a pu écrire avant l'interruption.
- **Code 1, autre message** : affiche-le tel quel et arrête-toi.
- **Code 127, « la CLI n'est pas encore installée »** : affiche le message tel quel et arrête-toi.
- **Code 2 (usage)** : c'est un bug de ce skill. Affiche stderr et arrête-toi.
