# Scan Command — Design Spec

**Date:** 2026-05-04  
**Scope:** Step 1 — scan d'un dossier et log des fichiers trouvés  
**Package:** `packages/archivist-cli`

---

## Contexte

Première étape du pipeline OCR/classement. La commande `scan` itère les fichiers d'un dossier source et logge chaque nom de fichier. Aucune logique OCR ni classement dans ce step — uniquement le parcours du dossier et la remontée structurée des fichiers trouvés.

---

## Commande CLI

```
archivist scan --source file:///path/to/docs
```

**Paramètre :**
- `--source` (requis) : URI `file://` pointant vers un dossier.

**Validations (dans `cli.py`) :**
1. L'URI doit avoir le scheme `file://` — sinon `BadParameter` explicite.
2. La cible doit être un dossier (`filesystem.is_dir`) — sinon `BadParameter` : `"<uri> n'est pas un dossier valide."`.

**Sortie stdout (JSON) :**
```json
{"scanned": 3, "files": ["facture.pdf", "contrat.pdf", "releve.png"]}
```

**Sortie stderr (logs) :**
```
INFO scanning facture.pdf
INFO scanning contrat.pdf
INFO scanning releve.png
INFO scan terminé : 3 fichier(s) traité(s)
```

**Exit codes :**
- `0` : succès (dossier vide compris)
- `2` : paramètre invalide (Click standard)

---

## Architecture

### `domain/ports.py` — Extension de `Filesystem`

Nouvelle méthode abstraite sur le port existant :

```python
@abstractmethod
def list_files(self, uri: str) -> list[str]:
    """Retourne les URIs file:// des fichiers directs du dossier (non récursif).
    
    Ne retourne pas les sous-dossiers. Lève FilesystemError si l'URI est invalide.
    """
    ...
```

`VERSION` reste à `1` — la méthode est ajoutée au contrat existant (pas de versioning incrémental pour ce patch).

### `adapters/fs/local.py` — `LocalFilesystem.list_files`

Implémentation avec `pathlib` :
- Parse l'URI `file://` → `Path`
- Itère les entrées du dossier, garde uniquement les fichiers (`entry.is_file()`)
- Retourne leurs URIs `file://` sous forme de strings
- Lève `FilesystemError` si le chemin n'existe pas ou n'est pas lisible

### `application/scan.py` — Use case

```python
@dataclass(frozen=True)
class ScanResult:
    files: list[str]

def scan(filesystem: Filesystem, source_uri: str) -> ScanResult:
    files = filesystem.list_files(source_uri)
    for uri in files:
        logger.info("scanning %s", Path(uri).name)
    return ScanResult(files=files)
```

- Aucune logique I/O directe
- Log du nom de fichier seul (pas l'URI complète)
- Le log de fin est émis par `cli.py` après réception du résultat

### `cli.py` — Commande `scan`

```python
@main.command(name="scan")
@click.option("--source", required=True, help="URI du dossier source (file:///path/to/docs).")
def scan_cmd(source: str) -> None:
    _require_file_uri(source, "source")
    fs = default_registry.resolve("fs", "local", {})
    if not fs.is_dir(source):
        raise click.BadParameter(
            f"{source!r} n'est pas un dossier valide.",
            param_hint="'--source'",
        )
    result = scan(filesystem=fs, source_uri=source)
    logger.info("scan terminé : %d fichier(s) traité(s)", len(result.files))
    click.echo(json.dumps({"scanned": len(result.files), "files": [Path(f).name for f in result.files]}))
```

---

## Tests

### `tests/application/test_scan.py`

Utilise `FakeFilesystem` (de `tests/fakes.py`) :
- Dossier avec N fichiers → `ScanResult.files` contient les bons URIs
- Dossier vide → `ScanResult(files=[])`

### `tests/adapters/test_contracts.py` — Extension `FilesystemContractSuite`

Nouveau test `test_list_files` :
- Crée un dossier avec 2 fichiers et 1 sous-dossier
- Vérifie que `list_files` retourne exactement les 2 fichiers (pas le sous-dossier)

### `tests/adapters/test_fs_local.py`

`LocalFilesystem` hérite de `FilesystemContractSuite` — le nouveau test `test_list_files` s'applique automatiquement.

### `tests/integration/test_scan_real.py`

Via `CliRunner` avec `tmp_path` pytest :
- Dossier avec 2 fichiers → stdout JSON valide, exit code 0
- URI pointant vers un fichier (pas un dossier) → exit code 2, message d'erreur explicite
- Dossier vide → `{"scanned": 0, "files": []}`, exit code 0

### `tests/fakes.py` — Extension `FakeFilesystem`

`list_files` retourne une liste configurable à l'init (défaut : `[]`).

---

## Ce qui est hors scope (Step 1)

- Scan récursif
- Filtrage par extension
- OCR / classement
- Déduplication
- Gestion des fichiers non lisibles (permissions)
