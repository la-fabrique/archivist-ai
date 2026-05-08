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

### État actuel — `scan` (use case implémenté)

La commande `scan` couvre la réception et la mise en conservation brute. Elle opère sur deux dossiers du référentiel identifiés par leur `role` : `reception` et `conservation_brut`.

```
        ┌──────────┐   ┌──────────────┐   ┌───────────────────┐   ┌────────────┐
source ─►  Ingest  ├──►│  Backup ZIP  ├──►│ MetadataExtract   ├──►│   Delete   │
(_Réception)       │   │(_Cons. brut) │   │   (async ×4)      │   │ (source)   │
        └────┬─────┘   └──────┬───────┘   └────────┬──────────┘   └─────┬──────┘
             │                │                     │                    │
            FS               FS                MetadataExtractor        FS
                                               (kreuzberg)
```

| Phase | Entrée | Sortie | Port(s) sollicité(s) |
|---|---|---|---|
| Ingest | URI `_Réception` | liste d'URIs fichiers | `Filesystem.list_files` |
| Backup ZIP | URI fichier source | archive `.zip` horodatée dans `_Conservation brut` | `Filesystem.zip_file` |
| MetadataExtract | URI fichier source | `FileMetadata` (mime, taille, titre, auteur, pages, langue) | `MetadataExtractor` |
| Delete | URI fichier source | suppression du fichier de réception | `Filesystem.delete_file` |

Résultat agrégé : `ScanResult(files: list[ScannedFile], backed_up: int, deleted: int)`.

> Les phases Backup et Delete sont synchrones ; MetadataExtract est asynchrone (semaphore ×4 concurrent).

### Vision cible — `classify` (à implémenter)

```
        ┌──────────┐   ┌──────────────┐   ┌─────┐   ┌────────────┐   ┌────────────┐   ┌──────────┐
source ─►  Ingest  ├──►│  Backup ZIP  ├──►│ OCR ├──►│ Extraction ├──►│ Classement ├──►│  Apply   │─► cible
        └────┬─────┘   └──────┬───────┘   └──┬──┘   └─────┬──────┘   └─────┬──────┘   └────┬─────┘
             │                │               │             │                 │                │
            FS               FS           OcrEngine       LLM             LLM + Référentiel   FS
                        (_Cons. brut)                                                        (+ Index)
```

| Étape | Entrée | Sortie | Port(s) sollicité(s) |
|---|---|---|---|
| Ingest | URI source (dossier) | flux de `SourceDocument` | `Filesystem` |
| Backup ZIP | `SourceDocument` | archive `.zip` dans `_Conservation brut` | `Filesystem` |
| OCR | `SourceDocument` | `OcrText` | `OcrEngine` |
| Extraction | `OcrText` | `ExtractedFields` | `LanguageModel` |
| Classement | `ExtractedFields` + référentiel | `ClassificationDecision` | `LanguageModel`, `Referentiel` |
| Apply | `ClassificationDecision` + bytes | effet : rename + move | `Filesystem` (cible), `Index` (no-op v1) |

### Famille « outils référentiel » — `scaffold`, `audit`
Ces commandes n'utilisent que les ports `Filesystem` et `Referentiel`.

### Trois propriétés que la vision impose au pipeline
1. **Étapes pures et typées.** Chaque étape est une fonction `(in) -> out`, sans I/O caché en dehors de ses ports déclarés.
2. **Ports injectés depuis le bord.** La CLI assemble les adaptateurs choisis par flags ; le cœur ne les construit jamais lui-même.
3. **Pas de raccourci entre étapes.** L'OCR ne « sait » rien de la classification ; on peut remplacer un moteur sans toucher à la suite.

---

## 3. Architecture en ports & adaptateurs

Trois cercles concentriques, façon hexagonale.

```
┌──────────────────────────────────────────────────────┐
│  Frontière CLI  (Click)                              │
│  ┌────────────────────────────────────────────────┐  │
│  │  Application  (use cases : classify/scaffold/  │  │
│  │                audit)                          │  │
│  │  ┌──────────────────────────────────────────┐  │  │
│  │  │  Domain  (entités + ports = ABC)         │  │  │
│  │  │  SourceDocument, OcrText, …              │  │  │
│  │  │  Filesystem, OcrEngine, LanguageModel,   │  │  │
│  │  │  Referentiel, Index                      │  │  │
│  │  └──────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────┘  │
│  Adapters  (impls concrètes des ports)               │
│  fs/local, fs/s3*, ocr/tesseract, ocr/mistral*,      │
│  llm/openai, llm/ollama, index/noop, …               │
└──────────────────────────────────────────────────────┘
                  * = futur, pas v1
```

### Règles de dépendance (la seule règle dure)
- `domain` ne dépend que de la stdlib + types.
- `application` dépend de `domain` uniquement.
- `adapters` dépendent de `domain` (pour implémenter les ABC).
- `cli` dépend de `application` + `adapters` — c'est le seul endroit où l'on **câble**.
- **Aucune flèche inverse.** Un adaptateur n'importe jamais un use case ; le domain n'importe jamais un adaptateur.

### Layout (`src/archivist_cli/`) — état actuel + cible

```
domain/          ports.py, models.py
application/     scan.py, scaffold.py          ← implémentés
                 classify.py, audit.py         ← cible
adapters/
  fs/            local.py
  metadata/      kreuzberg.py                  ← implémenté
  referentiel/   yaml_file.py
  ocr/           tesseract.py                  ← cible
  llm/           openai.py                     ← cible
  index/         noop.py                       ← cible
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

### `OcrEngine` — cible
Extraction de texte depuis des bytes. Le port porte les **capacités** (langues, tabulaire, …) pour qu'un use case puisse rejeter tôt un moteur incompatible.
Adaptateurs : `tesseract`, puis `mistral-ocr`, `azure-di`, `gcp-docai`.

### `LanguageModel` — cible
Un seul port couvre **extraction structurée** et **classement** — deux usages, un même contrat. Le schéma de sortie attendu est porté par l'appelant, pas par l'adaptateur.
Adaptateurs : `openai` ou `ollama`, puis `mistral-api`, `anthropic`.

### `Index` — cible
Mémoire des décisions. **Port à définir, no-op à livrer.** Présent dans le pipeline dès le départ pour éviter de réécrire le câblage le jour où on branche un vrai stockage.
Adaptateurs : `noop`, puis `sqlite`, `tantivy`, `elastic`.

### Règle transverse
Chaque port définit ses **erreurs propres** (`MetadataExtractorError`, `FilesystemError`, `ReferentielError`, `OcrError`, `LlmError`, …). Aucune ABC ne renvoie d'exception non documentée. Le use case décide de la politique.

---

## 5. Évolutivité plugins

Le **registre** est la seule pièce qui bougera quand on ouvrira aux tiers. Tout le reste — ports, use cases, adaptateurs — est déjà prêt.

- **v1.** Le registre est une **table interne** mappant un nom court (`tesseract`, `local`, `openai`…) à une fabrique d'adaptateur. La CLI lit les flags, résout, injecte. Un seul fichier à modifier pour ajouter un adaptateur en interne.
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
- `archivist scan` — réception → backup ZIP dans `_Conservation brut` → extraction métadonnées (kreuzberg) → suppression source.
- `archivist scaffold` — crée l'arborescence cible à partir du référentiel.

### Commandes cibles (non livrées)
- `archivist classify` — pipeline complet OCR + LLM, déplace + renomme.
- `archivist audit` — vérifie la cohérence entre arborescence et référentiel.

### Configuration v1
**Flags CLI uniquement.** Pas de fichier, pas de profils, pas d'environnement. Une seule source de vérité tant que l'usage n'est pas stabilisé.

### Évolution prévue (non livrée)
Le jour où l'on ajoute un fichier de config ou des profils, **seule la frontière CLI change**. Les use cases reçoivent toujours des adaptateurs déjà construits ; ils n'ont pas à savoir d'où viennent les choix.

### Sortie
La commande `classify` écrit sur stdout un **journal structuré** (une ligne JSON par fichier traité) décrivant la décision prise et l'action effectuée. Permet de piper, rejouer, auditer un run sans dépendre d'un index.

---

## 7. Tests & observabilité

### Testabilité garantie par l'archi
- **Domain et application testables sans I/O** via des adaptateurs *fakes* (`FakeFilesystem` en mémoire, `FakeOcr` à texte fixe, `FakeLlm` scripté). Aucun test unitaire ne touche disque, réseau ou modèle.
- **Suite par adaptateur réel**, isolée, validant le respect du contrat. Marquable `slow`/`integration` quand elle requiert des ressources externes.
- **Test de contrat générique**, paramétré par le port, rejoué sur **tous** les adaptateurs — built-in et, demain, tiers. C'est ce qui rend l'évolutivité plugins sûre.
- **Use cases** : tests bout-en-bout sur fakes ; c'est là que le pipeline est validé comme un tout.

### Observabilité v1 (minimale, suffisante)
- Logs structurés JSON sur stderr (un événement par étape).
- Sortie machine sur stdout (cf. §6).
- Aucun export distant en v1. Les logs passent par un **port logger** trivial : le jour où l'on veut OpenTelemetry, on remplace l'adaptateur ; le cœur ne change pas.

### Erreurs
Chaque port a ses erreurs propres (cf. §4). Politique du use case `classify` : **best-effort par fichier**. Une erreur sur un document émet un événement « échec » structuré et n'interrompt pas le run sur les autres.
