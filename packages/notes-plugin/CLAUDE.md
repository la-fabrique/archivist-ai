# notes-plugin

Plugin Claude Code `notes` (marketplace `archivist`, déclaré dans `.claude-plugin/marketplace.json` à la racine du dépôt). Installe la CLI `notes-cli` et expose le skill `/notes:note-add`.

## Layout

- `.claude-plugin/plugin.json` — manifeste du plugin
- `skills/note-add/SKILL.md` — skill `/notes:note-add`
- `bin/notes` — script relais vers le binaire installé (ajouté au PATH de l'outil Bash)
- `hooks/hooks.json` + `hooks/install-notes.sh` — hook SessionStart qui installe la dernière release `notes-cli/*`
- `tests/` — tests bash purs (`run.sh` lance les `test-*.sh`, fixtures dans `tests/fixtures/`)

## Tests

```bash
bash packages/notes-plugin/tests/run.sh
```

La CI ajoute `shellcheck` sur `bin/notes`, `hooks/install-notes.sh` et `tests/*.sh`.

## Point d'attention

`bin/notes` et `hooks/install-notes.sh` calculent tous deux le dossier de données (`CLAUDE_PLUGIN_DATA`, sinon `CLAUDE_CONFIG_DIR` ou `~/.claude`, puis `plugins/data/notes-archivist`), car l'outil Bash ne reçoit pas `CLAUDE_PLUGIN_DATA`. Garder les deux calculs en phase.
