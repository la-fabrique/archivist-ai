# notes — plugin Claude Code

Plugin Claude Code qui permet de confier une idée au bloc-notes depuis une session, via la CLI `notes`.

## Installation

Dans Claude Code :

```
/plugin marketplace add la-fabrique/archivist-ai
/plugin install notes@archivist
```

Redémarre ensuite la session : au démarrage, le plugin télécharge la dernière version de la CLI `notes` (release `notes-cli/*`). Tant que la session n'a pas redémarré, la commande `notes` répond qu'elle n'est pas encore installée.

## Usage

```
/notes:note-add <idée>
```

Le bloc-notes challenge l'idée par des questions, puis la range. Claude transmet chaque question telle quelle et attend ta réponse avant de continuer.

Exemple :

```
> /notes:note-add Un export PDF des fiches du référentiel

Quel est le besoin derrière cet export : lecture hors ligne ou diffusion à des tiers ?

> Diffusion à des tiers

L'idée a été déposée dans le bloc-notes : « Export PDF des fiches ».
```

## Configuration

La configuration se fait à la demande : si l'agent ou le dossier du bloc-notes n'est pas défini, le skill lance `notes config set agent claude-code` ou te demande le chemin du bloc-notes, puis relance l'échange. Tu peux aussi la faire à la main :

```bash
notes config set agent claude-code
notes config set bloc-notes "<chemin du bloc-notes>"
notes config show
```

## Plateformes prises en charge

- Linux x86_64
- macOS arm64

Sur les autres plateformes, aucune CLI n'est installée.

## Emplacement du binaire

`~/.claude/plugins/data/notes-archivist/` (ou `$CLAUDE_CONFIG_DIR/plugins/data/notes-archivist/`). Ce dossier contient le binaire `notes` et un fichier `version` (tag de la release installée). Le script `bin/notes` du plugin relaie vers ce binaire.

## Tests

```bash
bash packages/notes-plugin/tests/run.sh
```
