# referentiel-cli

CLI pour pousser le contenu de `packages/referentiel/` vers un dossier **existant** de Google Drive.

## Prérequis

- Node 20+
- **Compte Google perso** (ex. Gmail) : tu n’as pas besoin d’installer `gcloud`, ni d’un compte Google Cloud facturé ni d’un Workspace entreprise. Le **même** compte sert à te connecter à [Google Cloud Console](https://console.cloud.google.com/) pour créer un **projet gratuit** uniquement afin d’obtenir des identifiants OAuth pour l’API Drive.
- Dans ce projet : activer l’API **Google Drive**, configurer l’**écran de consentement OAuth** (type **Externe** ; en mode **Test**, ajouter **ton adresse** comme **utilisateur test**), puis créer un identifiant **OAuth 2.0** de type **Application de bureau** et récupérer le **fichier JSON** (à garder **hors dépôt**).
- **Alternative (optionnelle)** : si tu as le [Google Cloud SDK](https://cloud.google.com/sdk), `gcloud auth application-default login --scopes=https://www.googleapis.com/auth/drive` enregistre des identifiants par défaut ; dans ce cas le premier `push` peut fonctionner sans JSON client secret (voir `src/auth/adc-drive.ts`).
- Un dossier **déjà créé** dans ton Drive personnel ; son **ID** est dans l’URL (`/folders/<ID>`).

## Variables d’environnement

| Variable | Rôle |
|----------|------|
| `REFERENTIEL_CLI_GOOGLE_CLIENT_SECRET` | Chemin vers le JSON client secret |
| `REFERENTIEL_CLI_PARENT_FOLDER_ID` | ID dossier Drive par défaut pour `push` |

Les tokens sont stockés sous `~/.config/archivist/referentiel-cli/` (voir fichier `tokens.json`).

## Commandes

Lancer les commandes depuis la **racine du monorepo** (répertoire courant = parent de `packages/`), sauf si tu passes `--referentiel-root`.

```bash
npm run referentiel-cli:install
npm run referentiel-cli:build
node packages/referentiel-cli/dist/cli.js auth --client-secret /chemin/vers/client_secret.json
node packages/referentiel-cli/dist/cli.js push --parent-folder-id <ID>
```

Après un `push` réussi (sans `--dry-run`), l’ID parent est enregistré dans `config.json` : les prochains `push` peuvent omettre `--parent-folder-id` s’il est déjà en config ou dans `REFERENTIEL_CLI_PARENT_FOLDER_ID`.

- **`--dry-run`** : liste les dossiers/fichiers locaux et le MD5 calculé, sans appeler Google.
- **`push`** : avec le flux OAuth bureau, le fichier client secret (flag ou env) sert à rafraîchir l’accès à partir du refresh token ; avec ADC (`gcloud`), ce fichier n’est pas nécessaire.

Depuis la racine du dépôt : `npm run referentiel-cli:test` et `npm run referentiel-cli:build`.

## Scope OAuth

POC personnel : scope `https://www.googleapis.com/auth/drive` (accès Drive complet pour le compte autorisé). Ne pas distribuer le client secret.
