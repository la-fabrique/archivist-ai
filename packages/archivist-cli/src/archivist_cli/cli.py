from __future__ import annotations

import json
import logging
from pathlib import Path
from urllib.parse import urlparse

import click

from archivist_cli.adapters.index.noop import NoopIndex
from archivist_cli.application.apply import apply
from archivist_cli.application.classify import ClassifyConfig, ClassifyUseCase
from archivist_cli.application.scaffold import scaffold
from archivist_cli.application.scan import scan
from archivist_cli.config import AppConfig, install_referentiel, load_config, save_config
from archivist_cli.registry import default_registry

logger = logging.getLogger(__name__)


_SUPPORTED_REFERENTIEL_SCHEMES = {"file", "http", "https"}


def _find_role_in_entries(entries: list, role: str) -> str:
    matches = [e for e in entries if e.role == role]
    if len(matches) != 1:
        raise click.UsageError(
            f"Le référentiel contient {len(matches)} entrée(s) role={role!r} — exactement 1 attendue"
        )
    return matches[0].path


def _require_referentiel_uri(value: str, param_name: str) -> None:
    if urlparse(value).scheme not in _SUPPORTED_REFERENTIEL_SCHEMES:
        raise click.BadParameter(
            f"{value!r} n'est pas un URI valide. Utilisez file://, http:// ou https://.",
            param_hint=f"'--{param_name}'",
        )


def _require_file_uri(value: str, param_name: str) -> None:
    if urlparse(value).scheme != "file":
        raise click.BadParameter(
            f"{value!r} n'est pas un URI valide. Utilisez un URI absolu, ex: file:///chemin/vers/{param_name}",
            param_hint=f"'--{param_name}'",
        )


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx: click.Context) -> None:
    """archivist — OCR et classement de documents."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@main.group(name="config")
def config_group() -> None:
    """Gère la configuration persistante de la CLI."""


@config_group.group(name="set")
def config_set() -> None:
    """Définit un paramètre de configuration."""


@config_set.command(name="referentiel")
@click.argument("uri")
def config_set_referentiel(uri: str) -> None:
    """Installe le référentiel (file://, http://, https://) et enregistre son URI."""
    _require_referentiel_uri(uri, "referentiel")
    try:
        installed_uri = install_referentiel(uri)
    except (FileNotFoundError, ValueError) as e:
        raise click.ClickException(str(e))
    cfg = load_config()
    save_config(AppConfig(referentiel=installed_uri, root=cfg.root, llm=cfg.llm))
    click.echo(json.dumps({"referentiel": installed_uri}))


@config_set.command(name="root")
@click.argument("uri")
def config_set_root(uri: str) -> None:
    """Enregistre le dossier racine de l'archive dans la config."""
    _require_file_uri(uri, "root")
    cfg = load_config()
    save_config(AppConfig(referentiel=cfg.referentiel, root=uri, llm=cfg.llm))
    click.echo(json.dumps({"root": uri}))


@config_set.command(name="llm")
@click.argument("nom")
def config_set_llm(nom: str) -> None:
    """Enregistre l'adaptateur LLM dans la config."""
    cfg = load_config()
    save_config(AppConfig(referentiel=cfg.referentiel, root=cfg.root, llm=nom))
    click.echo(json.dumps({"llm": nom}))


@config_group.command(name="show")
def config_show() -> None:
    """Affiche la configuration persistée en JSON."""
    cfg = load_config()
    data: dict[str, str] = {}
    if cfg.referentiel is not None:
        data["referentiel"] = cfg.referentiel
    if cfg.root is not None:
        data["root"] = cfg.root
    if cfg.llm is not None:
        data["llm"] = cfg.llm
    click.echo(json.dumps(data))


@main.command(name="scaffold")
@click.option(
    "--referentiel",
    default=None,
    help="URI du fichier référentiel (file:///path/to/referentiel.yaml).",
)
@click.option(
    "--root",
    default=None,
    help="URI du dossier racine de l'archive (file:///path/to/archive).",
)
@click.option(
    "--option",
    "extra_options",
    multiple=True,
    help="Options supplémentaires à inclure (répétable). 'core' est toujours inclus.",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Affiche les dossiers qui seraient créés sans les créer.",
)
def scaffold_cmd(
    referentiel: str | None,
    root: str | None,
    extra_options: tuple[str, ...],
    dry_run: bool,
) -> None:
    """Crée l'arborescence de dossiers cible à partir du référentiel."""
    if referentiel is None or root is None:
        cfg = load_config()
        referentiel = referentiel or cfg.referentiel
        root = root or cfg.root
    if referentiel is None:
        raise click.UsageError(
            "--referentiel manquant. Configurez-le avec :\n"
            "  archivist config set referentiel file:///path/to/referentiel.yaml"
        )
    if root is None:
        raise click.UsageError(
            "--root manquant. Configurez-le avec :\n"
            "  archivist config set root file:///path/to/archive"
        )
    _require_file_uri(referentiel, "referentiel")
    _require_file_uri(root, "root")
    options = {"core"} | set(extra_options)
    ref = default_registry.resolve("referentiel", "yaml_file", {"uri": referentiel})
    fs = default_registry.resolve("fs", "local", {})

    result = scaffold(
        referentiel=ref,
        filesystem=fs,
        target_uri=root,
        options=options,
        dry_run=dry_run,
    )

    summary = {"created": result.created, "skipped": result.skipped, "errors": result.errors}
    click.echo(json.dumps(summary))

    if result.errors > 0:
        raise SystemExit(1)


@main.command(name="scan")
@click.option(
    "--referentiel",
    default=None,
    help="URI du fichier référentiel (file:///path/to/referentiel.yaml).",
)
@click.option(
    "--root",
    default=None,
    help="URI du dossier racine de l'archive (file:///path/to/archive).",
)
def scan_cmd(referentiel: str | None, root: str | None) -> None:
    """Sauvegarde les fichiers de _Réception dans _Conservation brut et extrait les métadonnées.

    Les fichiers restent dans _Réception après scan. Utilisez classify puis apply pour les classer.
    """
    if referentiel is None or root is None:
        cfg = load_config()
        referentiel = referentiel or cfg.referentiel
        root = root or cfg.root
    if referentiel is None:
        raise click.UsageError(
            "--referentiel manquant. Configurez-le avec :\n"
            "  archivist config set referentiel file:///path/to/referentiel.yaml"
        )
    if root is None:
        raise click.UsageError(
            "--root manquant. Configurez-le avec :\n"
            "  archivist config set root file:///path/to/archive"
        )
    _require_file_uri(referentiel, "referentiel")
    _require_file_uri(root, "root")

    ref = default_registry.resolve("referentiel", "yaml_file", {"uri": referentiel})
    fs = default_registry.resolve("fs", "local", {})
    extractor = default_registry.resolve("metadata", "kreuzberg", {})

    entries = ref.load_entries()

    reception_path = _find_role_in_entries(entries, "reception")
    backup_path = _find_role_in_entries(entries, "conservation_brut")

    root_base = root.rstrip("/")
    reception_uri = f"{root_base}/{reception_path}"
    backup_uri = f"{root_base}/{backup_path}"

    if not fs.is_dir(reception_uri):
        raise click.UsageError(
            f"Dossier _Réception introuvable à {reception_uri!r} — lancez scaffold d'abord"
        )
    if not fs.is_dir(backup_uri):
        raise click.UsageError(
            f"Dossier _Conservation brut introuvable à {backup_uri!r} — lancez scaffold d'abord"
        )

    result = scan(filesystem=fs, reception_uri=reception_uri, backup_uri=backup_uri, extractor=extractor, index=NoopIndex())

    logger.info("scan terminé : %d fichier(s) traité(s)", len(result.files))
    files_out = [
        {
            "name": f.name,
            "uri": f.uri,
            "metadata": dict(f.metadata) if f.metadata is not None else None,
        }
        for f in result.files
    ]
    click.echo(json.dumps({
        "scanned": len(result.files),
        "backed_up": result.backed_up,
        "files": files_out,
    }))


@main.command(name="classify")
@click.option(
    "--referentiel",
    default=None,
    help="URI du fichier référentiel (file:///path/to/referentiel.yaml).",
)
@click.option(
    "--root",
    default=None,
    help="URI du dossier racine de l'archive (file:///path/to/archive).",
)
@click.option(
    "--llm",
    "llm_name",
    default=None,
    help="Adaptateur LLM à utiliser (ex: claude-cli). Sans LLM, tous les fichiers sont marqués non classés.",
)
def classify_cmd(referentiel: str | None, root: str | None, llm_name: str | None) -> None:
    """Propose un classement LLM pour les fichiers de _Réception. N'effectue aucun déplacement.

    Sans LLM configuré, tous les fichiers sont déclarés non classés.
    Redirigez la sortie vers un fichier manifeste, puis lancez apply --manifest <fichier>.
    """
    if referentiel is None or root is None or llm_name is None:
        cfg = load_config()
        referentiel = referentiel or cfg.referentiel
        root = root or cfg.root
        llm_name = llm_name or cfg.llm
    if referentiel is None:
        raise click.UsageError(
            "--referentiel manquant. Configurez-le avec :\n"
            "  archivist config set referentiel file:///path/to/referentiel.yaml"
        )
    if root is None:
        raise click.UsageError(
            "--root manquant. Configurez-le avec :\n"
            "  archivist config set root file:///path/to/archive"
        )
    _require_file_uri(referentiel, "referentiel")
    _require_file_uri(root, "root")

    ref = default_registry.resolve("referentiel", "yaml_file", {"uri": referentiel})
    fs = default_registry.resolve("fs", "local", {})
    extractor = default_registry.resolve("metadata", "kreuzberg", {})
    llm = default_registry.resolve("llm", llm_name or "null", {})

    entries = ref.load_entries()

    reception_path = _find_role_in_entries(entries, "reception")
    reception_uri = f"{root.rstrip('/')}/{reception_path}"
    if not fs.is_dir(reception_uri):
        raise click.UsageError(
            f"Dossier _Réception introuvable à {reception_uri!r} — lancez scaffold d'abord"
        )

    if llm_name is None:
        logger.warning("Aucun LLM configuré — tous les fichiers seront marqués non classés")

    uc = ClassifyUseCase(
        fs=fs,
        referentiel=ref,
        extractor=extractor,
        llm=llm,
    )
    result = uc.run(ClassifyConfig(referentiel_uri=referentiel, target_uri=root))

    for event in result.events:
        row = {
            "uri": event.uri,
            "name": event.name,
            "status": event.status.value,
        }
        if event.entry_id is not None:
            row["entry_id"] = event.entry_id
        if event.dest_name is not None:
            row["dest_name"] = event.dest_name
        if event.dest_uri is not None:
            row["dest_uri"] = event.dest_uri
        if event.reason is not None:
            row["reason"] = event.reason
        click.echo(json.dumps(row, ensure_ascii=False))

    summary = {
        "scanned": result.scanned,
        "classified": result.classified,
        "unclassified": result.unclassified,
        "failed": result.failed,
    }
    click.echo(json.dumps(summary))


@main.command(name="apply")
@click.option(
    "--manifest",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="Fichier manifeste JSON issu de la commande classify.",
)
@click.option(
    "--referentiel",
    default=None,
    help="URI du fichier référentiel (file:///path/to/referentiel.yaml).",
)
@click.option(
    "--root",
    default=None,
    help="URI du dossier racine de l'archive (file:///path/to/archive).",
)
def apply_cmd(manifest: str, referentiel: str | None, root: str | None) -> None:
    """Déplace les fichiers de _Réception vers leur destination selon le manifeste classify.

    Les fichiers classifiés sont déplacés vers leur dossier cible.
    Les fichiers non classés ou en erreur sont déplacés vers _Non classé.
    Les fichiers déjà absents sont signalés comme skipped sans erreur.
    """
    if referentiel is None or root is None:
        cfg = load_config()
        referentiel = referentiel or cfg.referentiel
        root = root or cfg.root
    if referentiel is None:
        raise click.UsageError(
            "--referentiel manquant. Configurez-le avec :\n"
            "  archivist config set referentiel file:///path/to/referentiel.yaml"
        )
    if root is None:
        raise click.UsageError(
            "--root manquant. Configurez-le avec :\n"
            "  archivist config set root file:///path/to/archive"
        )
    _require_file_uri(referentiel, "referentiel")
    _require_file_uri(root, "root")

    ref = default_registry.resolve("referentiel", "yaml_file", {"uri": referentiel})
    fs = default_registry.resolve("fs", "local", {})

    entries = ref.load_entries()

    non_classe_path = _find_role_in_entries(entries, "non_classe")
    non_classe_uri = f"{root.rstrip('/')}/{non_classe_path}"
    if not fs.is_dir(non_classe_uri):
        raise click.UsageError(
            f"Dossier _Non classé introuvable à {non_classe_uri!r} — lancez scaffold d'abord"
        )

    decisions: list[dict] = []
    with open(manifest, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                parsed = json.loads(line)
            except json.JSONDecodeError:
                logger.warning("ligne manifeste ignorée (JSON invalide) : %r", line)
                continue
            if not parsed.get("uri"):
                continue
            decisions.append(parsed)

    result = apply(filesystem=fs, decisions=decisions, non_classe_uri=non_classe_uri)

    for event in result.events:
        row: dict = {
            "uri": event.uri,
            "name": event.name,
            "status": event.status.value,
        }
        if event.dest_uri is not None:
            row["dest_uri"] = event.dest_uri
        if event.reason is not None:
            row["reason"] = event.reason
        click.echo(json.dumps(row, ensure_ascii=False))

    summary = {
        "moved": result.moved,
        "skipped": result.skipped,
        "failed": result.failed,
    }
    click.echo(json.dumps(summary))

    if result.failed > 0:
        raise SystemExit(1)
