# Architecture — `archivist-cli`

Ce document décrit l'architecture cible de la CLI `archivist-cli` à un niveau haut : périmètre, pipeline, ports, règles de dépendance, évolutivité. Il ne fixe pas les signatures précises ni les choix d'implémentation — ces points sont laissés aux plans d'implémentation et, plus tard, à des ADRs ciblés.

---

## 1. Périmètre & non-objectifs

`archivist-cli` est une CLI Python qui, étant donné un fichier dans un dossier source, en déduit son classement dans le **référentiel** (cf. package `referentiel`) puis **renomme et déplace** le fichier vers le dossier cible correspondant.

### Dans le périmètre v1
- Pipeline en quatre étapes : *Ingest → OCR → Extraction → Classement*. L'application de la décision (rename + move) est portée par l'adaptateur Filesystem cible, pas par une cinquième étape conceptuelle.
- Adaptateurs **internes** au repo, choisis par flags CLI.
- Ports stables conçus pour qu'un package tiers puisse plus tard fournir un adaptateur sans modification du cœur.
- Deux commandes secondaires liées au référentiel : `scaffold` (créer l'arborescence cible) et `audit` (vérifier sa cohérence). Elles ne traversent pas le pipeline OCR/LLM, mais valident en pratique la qualité de l'abstraction Filesystem.

### Hors périmètre v1 (l'archi ne doit pas s'y opposer)
Index/DB des décisions, validation humaine, cache OCR/LLM, profils de configuration, fichier de configuration, plugins externes publiés, batch parallèle, télémétrie distante.

### Non-objectifs (jamais)
- Servir d'API serveur. `archivist-cli` reste un binaire ligne de commande.
- Embarquer la logique du référentiel : il est consommé, pas redéfini ici.

---

## 2. Pipeline & contrats des étapes

### `classify` ✓ implémenté

```
        ┌──────────┐   ┌──────────────┐   ┌──────────────────┐   ┌────────────┐   ┌──────────┐
source ─►  Ingest  ├──►│  Backup ZIP  ├──►│ MetadataExtract  ├──►│ Classement ├──►│  Apply   │─► cible
        └────┬─────┘   └──────┬───────┘   └────────┬─────────┘   └─────┬──────┘   └────┬─────┘
             │                │                     │                    │                │
            FS               FS             MetadataExtractor       LLM + Réf.           FS
                        (_Cons. brut)        (kreuzberg)                            (+ Index noop)
```

| Étape | Entrée | Sortie | Port(s) sollicité(s) |
|---|---|---|---|
| Ingest | URI `_Réception` | liste d'URIs fichiers | `Filesystem.list_files` |
| Backup ZIP | URI fichier source | archive `.zip` horodatée dans `_Conservation brut` | `Filesystem.zip_file` |
| MetadataExtract | URI fichier source | `ExtractionResult` (texte + métadonnées) | `MetadataExtractor` |
| Classement | texte + métadonnées + référentiel | `entry_id` + champs nommage | `LanguageModel` (×2 appels) |
| Apply | `entry_id` + champs | rename + move vers dossier cible | `Filesystem`, `Index` |

> Note : pas d'étape OCR séparée. `MetadataExtractor` (kreuzberg) extrait le texte et les métadonnées en une passe. Un port `OcrEngine` dédié peut être ajouté ultérieurement sans modifier le pipeline.

### Famille « outils référentiel » — `scaffold`
Cette commande utilise uniquement les ports `Filesystem` et `Referentiel`.

### Trois propriétés du pipeline
1. **Étapes pures et typées.** Chaque étape est une fonction `(in) -> out`, sans I/O caché en dehors de ses ports déclarés.
2. **Ports injectés depuis le bord.** La CLI assemble les adaptateurs via le registre ; le cœur ne les construit jamais lui-même.
3. **Pas de raccourci entre étapes.** `MetadataExtractor` ne « sait » rien de la classification ; on peut remplacer un extracteur sans toucher à la suite.

---

## 3. Architecture en ports & adaptateurs

Trois cercles concentriques, façon hexagonale.

```
┌──────────────────────────────────────────────────────┐
│  Frontière CLI  (Click)                              │
│  ┌────────────────────────────────────────────────┐  │
│  │  Application  (use cases : classify/scaffold)   │  │
│  │  ┌──────────────────────────────────────────┐  │  │
│  │  │  Domain  (entités + ports = ABC)         │  │  │
│  │  │  FileMetadata, ExtractionResult, …       │  │  │
│  │  │  Filesystem, MetadataExtractor,          │  │  │
│  │  │  LanguageModel, Referentiel, Index       │  │  │
│  │  └──────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────┘  │
│  Adapters  (impls concrètes des ports)               │
│  fs/local, metadata/kreuzberg, llm/claude-cli,       │
│  referentiel/yaml_file, index/noop, index/duckdb     │
│  fs/s3*, llm/openai* …                               │
└──────────────────────────────────────────────────────┘
                  * = futur
```

### Règles de dépendance (la seule règle dure)
- `domain` ne dépend que de la stdlib + types.
- `application` dépend de `domain` uniquement.
- `adapters` dépendent de `domain` (pour implémenter les ABC).
- `cli` dépend de `application` + `adapters` — c'est le seul endroit où l'on **câble**.
- **Aucune flèche inverse.** Un adaptateur n'importe jamais un use case ; le domain n'importe jamais un adaptateur.

### Layout (`src/archivist_cli/`)

```
domain/          ports.py, models.py
application/     scaffold.py, classify.py
adapters/
  fs/            local.py
  metadata/      kreuzberg.py
  referentiel/   yaml_file.py
  llm/           claude_cli.py
  index/         noop.py, duckdb.py
config.py
cli.py
registry.py
```

### Pourquoi ce layout sert l'évolutivité plugins
- Les ABC du `domain` **sont le contrat public** que tout adaptateur — interne ou tiers — consommera.
- Le `registry` est le seul endroit qui changera le jour où l'on ouvrira aux plugins externes.
- Le reste du code ignore l'origine d'un adaptateur.

---

## 4. Catalogue des ports

### `Filesystem` ✓ implémenté
Stockage hiérarchique, manipulé par **URI** (`file://`, `s3://`, `gdrive://`…) — jamais par `pathlib.Path`, qui fuiterait dans le domain.
Opérations : `make_dir`, `exists`, `is_dir`, `list_files`, `zip_file`, `delete_file`.
Adaptateurs : `local` (implémenté), puis `s3`, `gdrive`, `webdav`.

### `MetadataExtractor` ✓ implémenté
Extraction des métadonnées fichier et document depuis un URI `file://`. Retourne un `FileMetadata` (mime_type, size_bytes, modified_at, title, author, page_count, language).
Adaptateurs : `kreuzberg` (implémenté — extraction synchrone via `extract_file_sync`, wrappée en async dans le use case).

### `Referentiel` ✓ implémenté
Accès au référentiel de classement. Expose les entrées avec leur `role` (`reception`, `conservation_brut`, …) pour que la CLI puisse résoudre les dossiers sans logique métier.
Adaptateurs : `yaml_file` (implémenté, pointe sur l'artefact du package `referentiel`), puis `http`, `git`, `versioned`.

### `LanguageModel` ✓ implémenté
Un seul port couvre **extraction structurée** et **classement** — deux usages, un même contrat. Le schéma de sortie attendu est porté par l'appelant ; l'adaptateur valide que la réponse y est conforme avant de la retourner.
Adaptateurs : `claude-cli` (implémenté — appelle la CLI `claude -p` en subprocess, parse JSON, valide le schéma), puis `openai`, `ollama`.

### `Index` ✓ implémenté (noop + duckdb)
Mémoire des décisions. Présent dans le pipeline dès le départ pour ne pas réécrire le câblage quand on branchera un vrai stockage.
Adaptateurs : `noop` (aucune persistance, utilisé par défaut), `duckdb` (persistance locale dans un fichier `.db`, upsert sur URI).

### `OcrEngine` — futur
Port optionnel pour l'extraction de texte depuis des bytes bruts (langues, tabulaire…). Pas encore nécessaire : `MetadataExtractor` (kreuzberg) couvre le besoin actuel.
Adaptateurs futurs : `tesseract`, `mistral-ocr`, `azure-di`.

### Règle transverse
Chaque port définit ses **erreurs propres** (`MetadataExtractorError`, `FilesystemError`, `ReferentielError`, `LlmError`, `IndexError`, …). Aucune ABC ne renvoie d'exception non documentée. Le use case décide de la politique.

---

## 5. Évolutivité plugins

Le **registre** est la seule pièce qui bougera quand on ouvrira aux tiers. Tout le reste — ports, use cases, adaptateurs — est déjà prêt.

- **v1.** Le registre est une **table interne** mappant un nom court (`claude-cli`, `local`, `kreuzberg`…) à une fabrique d'adaptateur. La CLI lit les flags, résout, injecte. Un seul fichier à modifier pour ajouter un adaptateur en interne.
- **Plus tard.** Le registre fusionne sa table interne avec une **liste découverte automatiquement** parmi les paquets Python installés. Aucun changement dans le cœur, les use cases ou les ports.

### Décision irréversible dès la v1
Le **contrat de fabrique** — comment on instancie un adaptateur à partir d'une configuration — doit être stable dès le départ.

### Versioning des ports
Chaque port porte un **numéro de version**. Un adaptateur compatible avec une version trop ancienne ou trop récente est rejeté au démarrage avec un message clair. Ça protège les futurs plugins tiers d'une évolution silencieuse du contrat.

---

## 6. Frontière CLI & configuration

**Rôle de Click :** parser les flags, résoudre les noms d'adaptateurs via le registre, instancier le use case, exécuter, formater la sortie. **Aucune logique métier dans `cli.py`.**

### Forme générale d'une commande

```
archivist <commande> [--source URI] [--target URI]
                     [--ocr NAME]   [--llm NAME]
                     [--fs NAME]    [--referentiel URI]
                     [options spécifiques à l'adaptateur]
```

### Commandes implémentées
- `archivist scaffold` — crée l'arborescence cible à partir du référentiel.
- `archivist classify` — backup → extraction métadonnées → classement LLM → renommage + déplacement.
- `archivist config set {referentiel|root|llm}` / `archivist config show` — gestion de la config persistante.

### Commandes futures
- `archivist audit` — vérifie la cohérence entre arborescence et référentiel.

### Configuration persistante
La CLI maintient un fichier `config.yaml` dans le répertoire de données utilisateur (`platformdirs.user_data_dir("archivist", "archivist")`). Les clés `referentiel`, `root` et `llm` peuvent être fixées via `archivist config set` et sont lues comme valeurs par défaut par toutes les commandes. Un flag CLI explicite prend toujours le dessus sur la config.

Le référentiel est **copié** dans le répertoire app data au moment du `config set referentiel` — la CLI travaille toujours sur sa propre copie.

### Sortie
La commande `classify` écrit sur stdout un **journal structuré** (une ligne JSON par fichier traité) décrivant la décision prise et l'action effectuée. Permet de piper, rejouer, auditer un run sans dépendre d'un index.

---

## 7. Tests & observabilité

### Testabilité garantie par l'archi
- **Domain et application testables sans I/O** via des adaptateurs *fakes* (`FakeFilesystem` en mémoire, `FakeLlm` scripté, `FakeMetadataExtractor` à contenu fixe). Aucun test unitaire ne touche disque, réseau ou modèle.
- **Suite par adaptateur réel**, isolée, validant le respect du contrat. Marquable `slow`/`integration` quand elle requiert des ressources externes.
- **Test de contrat générique**, paramétré par le port, rejoué sur **tous** les adaptateurs — built-in et, demain, tiers. C'est ce qui rend l'évolutivité plugins sûre.
- **Use cases** : tests bout-en-bout sur fakes ; c'est là que le pipeline est validé comme un tout.

### Observabilité v1 (minimale, suffisante)
- Logs structurés JSON sur stderr (un événement par étape).
- Sortie machine sur stdout (cf. §6).
- Aucun export distant en v1. Les logs passent par un **port logger** trivial : le jour où l'on veut OpenTelemetry, on remplace l'adaptateur ; le cœur ne change pas.

### Erreurs
Chaque port a ses erreurs propres (cf. §4). Politique du use case `classify` : **best-effort par fichier**. Une erreur sur un document émet un événement « échec » structuré et n'interrompt pas le run sur les autres.
