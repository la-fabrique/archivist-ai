# referentiel-cli

CLI de POC pour authentifier avec Google (navigateur) et pousser le contenu de `packages/referentiel/` vers un dossier **existant** de Google Drive.

## Prérequis

- Node 20+
- Projet Google Cloud : API **Google Drive** activée, écran de consentement OAuth (mode Testing) et utilisateur test ajouté.
- Identifiant client OAuth de type **Application de bureau** ; fichier JSON hors dépôt.
- Un dossier cible dans Drive ; son ID est dans l’URL (`/folders/<ID>`).

## Variables d’environnement

| Variable | Rôle |
|----------|------|
| `REFERENTIEL_CLI_GOOGLE_CLIENT_SECRET` | Chemin vers le JSON client secret |
| `REFERENTIEL_CLI_PARENT_FOLDER_ID` | ID dossier Drive par défaut pour `push` |

Les tokens sont stockés sous `~/.config/archivist/referentiel-cli/` (voir fichier `tokens.json`).

## Commandes

Lancer les commandes depuis la **racine du monorepo** (répertoire courant = parent de `packages/`), sauf si tu passes `--referentiel-root`.

```bash
cd packages/referentiel-cli
npm install
npm run build
cd ../..
node packages/referentiel-cli/dist/cli.js auth --client-secret /chemin/vers/client_secret.json
node packages/referentiel-cli/dist/cli.js push --parent-folder-id <ID>
```

Après un `push` réussi (sans `--dry-run`), l’ID parent est enregistré dans `config.json` : les prochains `push` peuvent omettre `--parent-folder-id` s’il est déjà en config ou dans `REFERENTIEL_CLI_PARENT_FOLDER_ID`.

- **`--dry-run`** : liste les dossiers/fichiers locaux et le MD5 calculé, sans appeler Google.
- **`push`** exige le fichier client secret (flag ou env) pour rafraîchir l’accès à partir du refresh token.

Depuis la racine du dépôt : `npm run referentiel-cli:test` et `npm run referentiel-cli:build`.

## Scope OAuth

POC personnel : scope `https://www.googleapis.com/auth/drive` (accès Drive complet pour le compte autorisé). Ne pas distribuer le client secret.
