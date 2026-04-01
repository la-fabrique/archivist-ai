# referentiel-cli — push vers Google Drive

> **For agentic workers:** REQUIRED SUB-SKILL: Use @superpowers:subagent-driven-development (recommandé) ou @superpowers:executing-plans pour implémenter ce plan tâche par tâche. Les étapes utilisent la syntaxe checkbox (`- [ ]`) pour le suivi.

**Goal:** Ajouter le package `packages/referentiel-cli`, un CLI TypeScript qui authentifie l’utilisateur via le navigateur (OAuth Google), puis pousse le contenu de `packages/referentiel/` vers un dossier Google Drive (miroir de l’arborescence locale). La notification Discord est hors périmètre.

**Architecture:** Exécutable Node (`type: module`) avec parsing d’arguments minimal ou `commander`. OAuth 2.0 « application de bureau » : ouverture du navigateur, redirection vers `http://127.0.0.1:<port>/oauth2callback`, échange du code contre des tokens ; refresh token stocké localement. API Google Drive v3 via `googleapis`. **Racine Drive = un dossier existant** dont l’utilisateur fournit l’ID (`--parent-folder-id`, obligatoire pour `push` sauf valeur déjà persistée dans `config.json` — voir Task 6). Aucune création automatique d’un dossier racine « Archiviste ». Logique de parcours du disque et de décision « créer / mettre à jour » isolée dans des fonctions pures testables ; les appels réseau mockés en test.

**Tech Stack:** Node.js 20+, TypeScript 5.x, `googleapis`, `google-auth-library`, `open` (ou équivalent) pour ouvrir le navigateur, Vitest pour les tests, éventuellement `commander` pour les sous-commandes (`auth`, `push`).

**Décisions produit (validées 2026-04-01):**

| Sujet | Choix |
|-------|--------|
| Cible Drive | **Dossier existant uniquement** : ID fourni via `--parent-folder-id <id>` (l’utilisateur crée le dossier dans Drive et copie l’ID depuis l’URL). Optionnel : après un premier `push` réussi, persister `parentFolderId` dans `~/.config/archivist/referentiel-cli/config.json` pour ne plus passer le flag (voir Task 6). |
| Conflit fichier existant | Si le fichier distant (même nom, même chemin relatif) existe : **remplacer le contenu** si le MD5 local diffère (comparaison `md5Checksum` Drive vs hash local) ; sinon skip. |
| Contenu poussé | **Tous les fichiers** sous `packages/referentiel/` (pas seulement `.md`) : parcours récursif, exclusion des seuls fichiers « dotfile » / noms commençant par `.` (ex. `.hidden`, `.DS_Store`). Pas de `node_modules` dans ce package. |
| Contexte | **POC local, usage personnel** : pas de publication npm, pas d’audit OAuth « production » ; consentement Google en mode test / utilisateur seul suffit. |
| Secrets OAuth | Fichier JSON client secret **hors dépôt** ; chemin `--client-secret` ou `REFERENTIEL_CLI_GOOGLE_CLIENT_SECRET`. |

**Prérequis manuels (une fois par environnement):**

1. Projet Google Cloud → activer l’**API Google Drive**.
2. **POC perso :** type d’utilisateur « Externe », écran de consentement en **Testing**, ajouter **ton adresse Google** comme **utilisateur test** (sinon OAuth refuse après quelques comptes). Pas besoin de validation Google pour ce usage.
3. Identifiants → **ID client OAuth** de type **Application de bureau** → télécharger le JSON.
4. Dans Drive : créer (ou choisir) le dossier cible → copier l’**ID** (segment d’URL après `folders/`).
5. Aucun secret dans le dépôt ; README du package décrit uniquement les variables et chemins locaux.

---

## Cartographie des fichiers

| Fichier | Responsabilité |
|---------|----------------|
| `packages/referentiel-cli/package.json` | Nom, scripts `build`, `test`, `start`, dépendances, `bin` pointant vers le JS compilé |
| `packages/referentiel-cli/tsconfig.json` | Cible `ES2022`, `module` + `moduleResolution` adaptés à Node ESM |
| `packages/referentiel-cli/README.md` | Prérequis GCP, commandes `auth` / `push`, variables d’environnement |
| `packages/referentiel-cli/scripts/add-shebang.mjs` | Post-build : préfixer `dist/cli.js` avec `#!/usr/bin/env node` (tsc ne préserve pas le shebang du `.ts`) |
| `packages/referentiel-cli/src/cli.ts` | Point d’entrée : `commander`, `auth` → `runAuth`, `push` → `runPush` |
| `packages/referentiel-cli/src/commands/auth.ts` | Task 1 : stub `not implemented` ; Task 5 : flux OAuth complet |
| `packages/referentiel-cli/src/commands/push.ts` | Task 1 : stub ; Task 6 : sync Drive |
| `packages/referentiel-cli/src/auth/oauth-server.ts` | Serveur HTTP local éphémère, capture `code` & `state` |
| `packages/referentiel-cli/src/auth/token-store.ts` | Lire/écrire refresh token + métadonnées (chemin configurable, permissions 0o600) |
| `packages/referentiel-cli/src/config/runtime-config.ts` | Emplacement config XDG : `~/.config/archivist/referentiel-cli/config.json` (ou `%APPDATA%` sous Windows via lib ou logique simple) |
| `packages/referentiel-cli/src/sync/walk-referentiel.ts` | Parcours `packages/referentiel`, **tous fichiers** (hors dotfiles), chemins relatifs (pur) |
| `packages/referentiel-cli/src/sync/drive-mirror.ts` | Création des dossiers manquants, upload/update fichiers (dépend de l’API ; injecter client pour tests) |
| `packages/referentiel-cli/src/sync/content-hash.ts` | MD5 ou SHA256 fichier local pour comparaison avec Drive |
| `packages/referentiel-cli/src/lib/errors.ts` | Erreurs typées (auth manquante, quota, etc.) |
| `packages/referentiel-cli/test/walk-referentiel.test.ts` | Tests Vitest sur arbre factice |
| `packages/referentiel-cli/test/content-hash.test.ts` | Tests sur fichiers temporaires |
| `packages/referentiel-cli/test/drive-mirror.logic.test.ts` | Tests unitaires sur « quelles opérations Drive simuler » avec doubles (sans réseau) |
| Racine `package.json` | Script racine optionnel `referentiel-cli:push` qui fait `npm run push --prefix packages/referentiel-cli` |

**Scope OAuth (POC, dossier parent existant):** utiliser **`https://www.googleapis.com/auth/drive`** pour garantir l’écriture récursive sous un `parentId` choisi par l’utilisateur sans ambiguïté liée au scope `drive.file` (qui n’autorise en principe que les fichiers ouverts/créés par l’app). Pour un **POC personnel**, l’écran de consentement listera le scope « voir, modifier, créer et supprimer **tous** vos fichiers Google Drive » — acceptable tant que le client secret reste local et que l’appli n’est pas distribuée.  

**Alternative documentée dans le README :** tenter `drive.file` si tu veux limiter la surface plus tard ; si `files.create` / `files.list` échoue sur le dossier parent, revenir à `drive` pour ce dépôt jusqu’à modélisation plus fine (ex. File Picker une fois).

---

### Task 1: Empaquetage, toolchain et entrée CLI exécutable

**Files:**
- Create: `packages/referentiel-cli/package.json`
- Create: `packages/referentiel-cli/tsconfig.json`
- Create: `packages/referentiel-cli/scripts/add-shebang.mjs`
- Create: `packages/referentiel-cli/src/cli.ts`
- Create: `packages/referentiel-cli/src/commands/auth.ts` (stub)
- Create: `packages/referentiel-cli/src/commands/push.ts` (stub)
- Create: `packages/referentiel-cli/README.md` (sections prérequis + usage minimal)
- Modify: `package.json` (racine) — scripts `referentiel-cli:build`, `referentiel-cli:test`

**Ordre d’implémentation:** Cette tâche doit produire `dist/cli.js` après `npm run build`, pour que les tests manuels des Tasks 5–6 puissent invoquer `node dist/cli.js auth|push`.

- [ ] **Step 1: Créer `package.json` du package** avec `"type": "module"`, `devDependencies`: `typescript`, `vitest`, `@types/node`, `dependencies`: `googleapis`, `google-auth-library`, `open`, `commander`. Scripts : `build`: `tsc`, `postbuild`: `node scripts/add-shebang.mjs`, `test`: `vitest run`, `push`: `node dist/cli.js push`.

```json
{
  "name": "@archivist/referentiel-cli",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "bin": {
    "referentiel-cli": "./dist/cli.js"
  },
  "scripts": {
    "build": "tsc",
    "postbuild": "node scripts/add-shebang.mjs",
    "test": "vitest run",
    "test:watch": "vitest",
    "push": "node dist/cli.js push"
  }
}
```

- [ ] **Step 2: Ajouter `scripts/add-shebang.mjs`** — lire `dist/cli.js` ; si la première ligne n’est pas le shebang, préfixer `#!/usr/bin/env node\n` et réécrire le fichier (UTF-8).

- [ ] **Step 3: Ajouter `tsconfig.json`** avec `outDir: "dist"`, `rootDir: "src"`, `strict`, `declaration`, module ESM compatible Node 20+.

- [ ] **Step 4: Ajouter `src/cli.ts`** avec `commander` : programme `referentiel-cli`, sous-commandes `auth` et `push` qui importent dynamiquement `./commands/auth.js` / `./commands/push.js` et appellent `runAuth` / `runPush` (permettre arborescence plate dans `src/commands/`).

- [ ] **Step 5: Stubs** — `auth.ts` et `push.ts` exportent `runAuth` / `runPush` qui lancent une erreur explicite `not implemented` (remplacées aux Tasks 5 et 6).

- [ ] **Step 6: Vérifier le build**

```bash
cd /home/deka/sources/github/archivist-ai/packages/referentiel-cli && npm install && npm run build && head -n 1 dist/cli.js
```

Attendu : première ligne `#!/usr/bin/env node` ; `node dist/cli.js --help` affiche l’aide.

- [ ] **Step 7: Commit** (tous les nouveaux fichiers listés avec `git add`, ne pas utiliser `git commit -am` pour ce commit).

```bash
git add packages/referentiel-cli/package.json packages/referentiel-cli/tsconfig.json packages/referentiel-cli/scripts/add-shebang.mjs packages/referentiel-cli/src/cli.ts packages/referentiel-cli/src/commands/auth.ts packages/referentiel-cli/src/commands/push.ts packages/referentiel-cli/README.md package.json
git commit -m "chore(referentiel-cli): scaffold package, postbuild shebang, cli stubs"
```

---

### Task 2: Parcours local du référentiel (TDD)

**Files:**
- test: `packages/referentiel-cli/test/walk-referentiel.test.ts`
- Create: `packages/referentiel-cli/src/sync/walk-referentiel.ts`

- [ ] **Step 1: Écrire le test qui échoue**

Dans `walk-referentiel.test.ts`, créer un répertoire temporaire avec :
- `a.md`, `sub/b.md`, `sub/data.json` (ou autre fichier **non** `.md`) — le référentiel peut contenir tout type de fichier
- ignorer `.hidden` ou `.hidden.md`

Attendu : fonction exportée (ex. `walkReferentielFiles(rootDir: string)`) retourne **tous** les fichiers (toutes extensions), chemins relatifs normalisés POSIX triés, sans dotfiles.

```typescript
import { mkdtempSync, writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { describe, it, expect } from "vitest";
import { walkReferentielFiles } from "../src/sync/walk-referentiel.js";

describe("walkReferentielFiles", () => {
  it("lists all files with relative paths excluding dotfiles", () => {
    const root = mkdtempSync(join(tmpdir(), "ref-"));
    writeFileSync(join(root, "a.md"), "# a");
    mkdirSync(join(root, "Mes Ventes"));
    writeFileSync(join(root, "Mes Ventes", "b.md"), "# b");
    writeFileSync(join(root, "Mes Ventes", "readme.txt"), "hi");
    writeFileSync(join(root, ".hidden.md"), "x");

    const got = walkReferentielFiles(root);
    expect(got).toEqual(["Mes Ventes/b.md", "Mes Ventes/readme.txt", "a.md"]);
  });
});
```

- [ ] **Step 2: Lancer le test (échec attendu)**

```bash
cd /home/deka/sources/github/archivist-ai/packages/referentiel-cli && npm install && npm run test -- test/walk-referentiel.test.ts
```

Attendu : échec (`walkReferentielFiles is not defined` ou équivalent).

- [ ] **Step 3: Implémenter `walk-referentiel.ts`**

Parcours récursif avec `node:fs` ; **inclure toutes les extensions** ; exclure uniquement les entrées dont le **nom de fichier** commence par `.` (fichiers et dossiers cachés). Ne pas descendre dans des répertoires exclus si la politique est « ignorer tout chemin contenant un segment dot » — pour rester aligné avec le test, exclure seulement les noms qui commencent par `.` au niveau de chaque listing.

- [ ] **Step 4: Relancer les tests**

Attendu : PASS.

- [ ] **Step 5: Commit**

```bash
git add packages/referentiel-cli/src/sync/walk-referentiel.ts packages/referentiel-cli/test/walk-referentiel.test.ts
git commit -m "feat(referentiel-cli): walk local referentiel tree"
```

---

### Task 3: Hash contenu fichier (TDD)

**Files:**
- test: `packages/referentiel-cli/test/content-hash.test.ts`
- Create: `packages/referentiel-cli/src/sync/content-hash.ts`

- [ ] **Step 1: Test ** `fileMd5Hex(path)` retourne le même hash que `echo -n hello | md5sum` pour un petit fichier.

- [ ] **Step 2: Run test — expect FAIL**

```bash
npm run test -- test/content-hash.test.ts
```

- [ ] **Step 3: Implémenter** avec `node:crypto` `createHash("md5")` + stream ou `readFileSync` pour petits fichiers.

- [ ] **Step 4: Run test — expect PASS**

- [ ] **Step 5: Commit**

```bash
git add packages/referentiel-cli/src/sync/content-hash.ts packages/referentiel-cli/test/content-hash.test.ts
git commit -m "feat(referentiel-cli): md5 helper for drive comparison"
```

---

### Task 4: Config et stockage des tokens

**Files:**
- Create: `packages/referentiel-cli/src/config/runtime-config.ts`
- Create: `packages/referentiel-cli/src/auth/token-store.ts`
- test: `packages/referentiel-cli/test/token-store.test.ts` (lecture/écriture sur répertoire temporaire, mock home)

- [ ] **Step 1: Test ** — écrire un refresh token factice, le relire, vérifier égalité.

- [ ] **Step 2: FAIL puis implémenter** chemins :
  - `getConfigDir()` : `$XDG_CONFIG_HOME/archivist/referentiel-cli` ou `~/.config/archivist/referentiel-cli`
  - Fichiers : `tokens.json` (chmod 600), `config.json` pour `rootFolderId` et chemins par défaut

Structure `tokens.json` :

```json
{ "refresh_token": "...", "token_type": "Bearer", "expiry_date": 0 }
```

Structure `config.json` (exemple, champs optionnels sauf besoin) :

```json
{ "parentFolderId": "1abc…xyz" }
```

- [ ] **Step 3: Tests PASS + commit**

```bash
git add packages/referentiel-cli/src/config/runtime-config.ts packages/referentiel-cli/src/auth/token-store.ts packages/referentiel-cli/test/token-store.test.ts
git commit -m "feat(referentiel-cli): config dir and token store"
```

---

### Task 5: Serveur OAuth local et commande `auth`

**Files:**
- Create: `packages/referentiel-cli/src/auth/oauth-server.ts`
- Modify: `packages/referentiel-cli/src/commands/auth.ts` (remplacer le stub Task 1)
- test: `packages/referentiel-cli/test/oauth-server.test.ts` — démarrer serveur, simuler requête GET avec `code` (sans réseau Google, uniquement parsing query)

- [ ] **Step 1: Test ** `waitForOAuthCallback` résout avec `{ code }` quand un client HTTP fait **GET `/oauth2callback?code=abc&state=xyz`** sur le port choisi — **même chemin** que `redirect_uri` (`http://127.0.0.1:<port>/oauth2callback`) ; rejette si `error=` dans query.

- [ ] **Step 2: Implémenter** serveur `http.createServer`, une promesse avec timeout (ex. 120 s), fermeture du serveur après succès ; ne traiter que les URLs dont `pathname === "/oauth2callback"` (ou équivalent strict).

- [ ] **Step 3: `commands/auth.ts`** :
  - Charger client secret JSON (argument `--client-secret` ou env)
  - `OAuth2Client` de `google-auth-library`, `redirect_uri` = `http://127.0.0.1:<port>/oauth2callback`
  - `generateAuthUrl` avec `access_type: 'offline'`, `prompt: 'consent'`, scope **`https://www.googleapis.com/auth/drive`** (POC + dossier parent existant — voir section « Scope OAuth » du plan)
  - `open(authUrl)`
  - Échanger le code via `getToken`, persister refresh token via `token-store`

- [ ] **Step 4: Test manuel** (documenté dans README, pas automatisé) : après `npm run build`, `node dist/cli.js auth --client-secret /path/secret.json` → navigateur s’ouvre, connexion Google, callback → fichier token créé.

- [ ] **Step 5: Commit**

```bash
git add packages/referentiel-cli/src/auth/oauth-server.ts packages/referentiel-cli/src/commands/auth.ts packages/referentiel-cli/test/oauth-server.test.ts packages/referentiel-cli/README.md
git commit -m "feat(referentiel-cli): google oauth browser flow and auth command"
```

---

### Task 6: Miroir Drive — logique + intégration API

**Files:**
- Create: `packages/referentiel-cli/src/sync/drive-mirror.ts`
- Modify: `packages/referentiel-cli/src/commands/push.ts` (remplacer le stub Task 1)
- test: `packages/referentiel-cli/test/drive-mirror.logic.test.ts`

- [ ] **Step 1: Tests unitaires** avec un faux client Drive (objet avec compteurs `foldersCreated`, `filesUpdated`) :
  - entrée : liste de chemins relatifs + hash MD5
  - état initial simulé : dossiers/fichiers existants
  - attendu : ordre des appels cohérent (création parents avant enfants)

- [ ] **Step 2: Implémenter `push.ts`** :
  - Option **`--parent-folder-id <id>` (obligatoire)** sauf si `config.json` contient déjà `parentFolderId` (persistance après premier succès, **optionnel** : si absent du disque et du flag, quitter avec message clair). Variable d’environnement facultative `REFERENTIEL_CLI_PARENT_FOLDER_ID` documentée dans le README.
  - Option `--referentiel-root` : défaut `./packages/referentiel` quand `cwd` = racine du monorepo ; override explicite pour CI ou chemins custom.
  - Charger tokens, `OAuth2Client`, `google.drive({ version: "v3", auth })`
  - **Ne pas** créer de dossier racine « Archiviste » : le miroir commence **sous** le `parentFolderId` fourni (les sous-dossiers locaux deviennent des dossiers Drive sous ce parent).

- [ ] **Step 3: Pour chaque fichier** (Chemins relatifs) :
  - S’assurer que chaque segment de dossier existe sous la racine (cache map `path → folderId`)
  - `files.list` avec query `name = 'x' and 'parentId' in parents and trashed = false` ou créer si absent
  - Pour fichier : si absent → `files.create` multipart upload ; si présent et MD5 différent → `files.update` avec `media`

- [ ] **Step 4: Option `--dry-run`** : log uniquement les actions sans appel mutation

- [ ] **Step 5: Test manuel** (compte Google perso, dossier test dans Drive) :  
  `npm run build && node dist/cli.js push --parent-folder-id <ID_Dossier_Existant> [--client-secret ... si pas déjà authentifié]`

- [ ] **Step 6: Commit**

```bash
git add packages/referentiel-cli/src/sync/drive-mirror.ts packages/referentiel-cli/src/commands/push.ts packages/referentiel-cli/test/drive-mirror.logic.test.ts packages/referentiel-cli/README.md
git commit -m "feat(referentiel-cli): push referentiel tree to Google Drive"
```

---

### Task 7: Finitions package et README

**Files:**
- Modify: `packages/referentiel-cli/package.json` — champs `files` (`dist`, `README.md`), `engines: { "node": ">=20" }`
- Modify: `packages/referentiel-cli/README.md` — couvrir `npm run build`, flux `auth` puis `push`, `--dry-run`, erreurs typiques (consentement OAuth, scopes)

- [ ] **Step 1: Vérifier** que `npm pack --dry-run` (ou équivalent) n’inclut pas `src/` si tu publies plus tard ; pour monorepo privé, `private: true` suffit souvent — ajuster `files` en conséquence.

- [ ] **Step 2: Documenter** dans README : `auth` (une fois, navigateur) vs `push` (répétable), où sont stockés les tokens (`~/.config/archivist/referentiel-cli/`), optional screenshots GCP.

- [ ] **Step 3: `npm run test`** — tous les tests du package PASS.

- [ ] **Step 4: Commit**

```bash
git add packages/referentiel-cli/package.json packages/referentiel-cli/README.md
git commit -m "docs(referentiel-cli): package metadata and usage"
```

---

### Task 8: Hors scope explicite (référence future)

- **Discord :** aucun code ni dépendance dans ce PR ; réserver une spec ou une issue pour « notifier Discord après push ».
- **Raccourcis / fichiers spéciaux Drive :** le CLI pousse des **fichiers binaires/texte** tels quels ; reproduire des *shortcuts* Google Drive ou suivre des symlinks locaux est **hors scope** (ne pas suivre les symlinks par défaut, ou documenter « comportement indéfini »).
- **CI :** ne pas lancer `push` en CI sans secrets ; éventuellement job qui fait uniquement `npm test` dans `packages/referentiel-cli`.

---

## Références de compétences

- @superpowers:test-driven-development — pour toute nouvelle fonction métier
- @superpowers:verification-before-completion — avant de déclarer le lot terminé : `npm run test` et un `push --dry-run` manuel concluant

---

## Revue du plan

**Statut (2026-04-01):** revue sous-agent effectuée ; corrections intégrées (ordre CLI + shebang, snippet `package.json`, commits, `/oauth2callback`).

---

## Handoff exécution

Après validation de la revue : **Plan enregistré dans `docs/superpowers/plans/2026-04-01-referentiel-cli-drive.md`. Deux options d’exécution :**

1. **Subagent-driven (recommandé)** — un sous-agent frais par tâche, relecture entre les tâches ; sous-compétence @superpowers:subagent-driven-development obligatoire.
2. **Inline** — enchaîner les tâches dans cette session avec @superpowers:executing-plans et points de contrôle.

**Quelle approche préfères-tu ?**
