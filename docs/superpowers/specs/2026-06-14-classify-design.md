# Design — `archivist classify`

**Date:** 2026-06-14  
**Status:** approved

---

## Contexte

`archivist classify` est la commande centrale du pipeline archivist : elle lit les fichiers déposés dans `_Réception`, les sauvegarde, extrait leur contenu, les classe via un LLM, puis les déplace et renomme selon les conventions du référentiel.

Ce design couvre la v1. Il s'appuie sur l'architecture hexagonale existante (`scan`, `scaffold`) et introduit un nouveau port `LanguageModel` (ADR-005).

---

## Pipeline

```
_Réception
    │
    ▼
Ingest          — Filesystem.list_files → liste d'URIs
    │
    ▼
Backup ZIP      — Filesystem.zip_file → archive horodatée dans _Conservation brut
    │             Échec ici → fichier reste dans _Réception, événement "failed" émis
    ▼
MetadataExtract — MetadataExtractor.extract → ExtractionResult (texte + métadonnées)
    │             (kreuzberg, même adaptateur que scan)
    │             Échec ici → fichier va dans _Non classé
    ▼
LLM Classify    — LanguageModel.complete → {entry_id: str|null, reason: str}
    │             null → fichier va dans _Non classé
    ▼
LLM Extract     — LanguageModel.complete → {champ: valeur} selon file_naming.fields
fields            de l'entrée choisie
    │             Échec ici → fichier va dans _Non classé
    ▼
Apply           — Filesystem : rename selon pattern + move vers dossier cible
                  ou move (sans rename) vers _Non classé
```

### Politique d'erreur

| Situation | Destination | Comportement |
|---|---|---|
| Erreur avant/pendant backup | reste dans `_Réception` | fichier non touché, retryable |
| Erreur post-backup (metadata, LLM) | `_Non classé` | événement `failed` sur stdout |
| LLM retourne `entry_id: null` | `_Non classé` | événement `unclassified` sur stdout |
| Succès | dossier cible du référentiel | événement `classified` sur stdout |

Best-effort par fichier : une erreur n'interrompt pas le traitement des autres fichiers.

---

## Ports

### `LanguageModel` — nouveau port

```python
class LlmError(Exception):
    pass

class LanguageModel(ABC):
    VERSION: ClassVar[int] = 1

    @abstractmethod
    def complete(self, prompt: str, output_schema: dict) -> dict:
        """Envoie un prompt et retourne un dict structuré conforme au schéma.

        Lève LlmError si l'appel échoue ou si la sortie ne peut pas être parsée.
        """
        ...
```

Le schéma de sortie est porté par l'appelant (use case), pas par l'adaptateur (ADR-005). L'adaptateur est un passe-plat typé : il ne connaît pas la sémantique métier.

### Adaptateur `claude-cli`

Implémentation via subprocess vers le binaire `claude` :

```
claude -p "<prompt incluant le schéma JSON attendu>"
```

L'adaptateur :
1. Formate le prompt en incluant le schéma JSON attendu et une instruction de retourner uniquement du JSON valide
2. Appelle `claude -p` en subprocess
3. Parse le JSON de la sortie stdout
4. Lève `LlmError` si le subprocess échoue ou si le JSON est invalide

Sélectionné via `--llm claude-cli`. Utilise la session browser authentifiée de Claude Code — aucune clé API requise.

### Ports existants réutilisés

- `Filesystem` — list_files, zip_file, make_dir, et `move_file(src_uri, dest_uri)` (**nouvelle opération à ajouter au port v2**)
- `MetadataExtractor` — extract (kreuzberg, identique à scan)
- `Referentiel` — load_entries (résolution par rôle : `reception`, `conservation_brut`, `non_classe`)

---

## Appels LLM

### Appel 1 — Classification

**Entrée :** texte extrait + métadonnées + liste des entrées du référentiel ayant un `file_naming` défini (id, description, path — incluant les entrées dynamiques comme `[Nom banque]`)

**Schéma de sortie :**
```json
{
  "entry_id": "string or null",
  "reason": "string"
}
```

`entry_id: null` signifie que le LLM ne peut pas déterminer le classement avec suffisamment de certitude.

### Appel 2 — Extraction des champs (uniquement si entry_id non null)

**Entrée :** texte extrait + métadonnées + `file_naming.fields` de l'entrée choisie

**Schéma de sortie :** dict dont les clés sont les noms de champs définis dans `file_naming.fields`, les valeurs sont des strings (ou null si le champ ne peut pas être extrait).

Le use case applique ensuite le `file_naming.pattern` avec ces valeurs pour construire le nom de fichier final. Le nommage est **strictement déterministe** : aucune inventivité LLM sur la forme du nom.

### Résolution du chemin cible (Apply)

Apply est responsable de construire l'URI de destination complète avant de déplacer le fichier :

1. **Entrées dynamiques** (`dynamic: true`, path contenant `[Segment]`) — le segment est substitué par la valeur extraite par le LLM (ex. `[Nom banque]` → `Credit-Mutuel`).
2. **Organisation chronologique** (`organization.type: chronological`, `subfolder_pattern: AAAA-MM`) — un sous-dossier `AAAA-MM` est créé à partir de la valeur date extraite (ex. `2026-03`).
3. **`make_dir`** est appelé avant le déplacement pour s'assurer que le dossier cible existe (idempotent).
4. **`move_file(src_uri, dest_uri)`** déplace et renomme en une opération atomique.

---

## Référentiel — nouvelle entrée

Ajout dans `referentiel.yaml` d'une entrée système :

```yaml
- id: non_classe
  folder_name: _Non classé
  path: _Non classé
  dynamic: false
  option: core
  required: true
  role: non_classe
  description: Fichiers que le pipeline classify n'a pas pu classer (LLM incertain ou erreur post-backup)
  organization:
    type: flat
```

Cette entrée est ajoutée via `referentiel-cli` (fiche Markdown dans `classement/`) et doit passer le skill `referentiel-update`.

---

## CLI

```bash
archivist classify \
  --referentiel file:///path/to/referentiel.yaml \
  --target file:///path/to/archive \
  --llm claude-cli
```

| Flag | Requis | Description |
|---|---|---|
| `--referentiel URI` | oui | Chemin vers `referentiel.yaml` (`file:///…`) |
| `--target URI` | oui | Racine de l'archive (même convention que `scaffold`/`scan`) |
| `--llm NAME` | oui | Adaptateur LLM à utiliser (ex. `claude-cli`) |

La commande résout `_Réception`, `_Conservation brut` et `_Non classé` par leur `role` dans le référentiel — aucun chemin hardcodé.

---

## Output

### stdout — NDJSON (une ligne par fichier + résumé final)

```json
{"uri": "file:///…/facture.pdf", "name": "facture.pdf", "status": "classified", "entry_id": "mes_achats.factures_fournisseurs", "dest_name": "2026-03_Facture_OVH_F2600042.pdf", "dest_uri": "file:///…/Mes achats/Mes factures fournisseurs/2026-03/2026-03_Facture_OVH_F2600042.pdf"}
{"uri": "file:///…/unknown.pdf", "name": "unknown.pdf", "status": "unclassified", "reason": "llm_uncertain: document type not recognized"}
{"uri": "file:///…/broken.pdf", "name": "broken.pdf", "status": "failed", "reason": "metadata_error: extraction failed"}
{"scanned": 3, "classified": 1, "unclassified": 1, "failed": 1}
```

### stderr — logs structurés JSON par étape (même pattern que `scan`)

---

## Tests

### Domain / application (fakes uniquement, aucun I/O)

- `FakeLlm` scriptable : retourne une séquence de réponses prédéfinies (classification puis extraction)
- Pipeline nominal : 3 fichiers → 3 classified
- LLM retourne null → fichier dans `_Non classé`
- Erreur metadata post-backup → fichier dans `_Non classé`
- Erreur backup → fichier reste dans `_Réception`
- Erreur sur un fichier n'interrompt pas les suivants

### Adaptateur `claude-cli` (contrat)

- Suite de contrat `LanguageModel` : fake + claude-cli passent le même test
- Test d'intégration marqué `slow` : appel réel à `claude -p`, vérifie que la sortie est un JSON valide

### Intégration (I/O réel, dossier temporaire)

- Run complet sur un dossier avec 2 fichiers réels (PDF simple)

---

## ADRs liés

- **ADR-005** — Port LanguageModel unique : justifie l'approche deux appels avec schéma porté par le use case
- **ADR-011** — à rédiger : "v1 classify réutilise MetadataExtractor pour l'extraction de texte ; OcrEngine différé"
