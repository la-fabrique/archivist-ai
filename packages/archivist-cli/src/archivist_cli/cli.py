from __future__ import annotations

import json
import logging
from pathlib import Path
from urllib.parse import urlparse

import click

from archivist_cli.adapters.index.noop import NoopIndex
from archivist_cli.application.classify import ClassifyConfig, ClassifyUseCase
from archivist_cli.application.scaffold import scaffold
from archivist_cli.application.scan import scan
from archivist_cli.config import AppConfig, install_referentiel, load_config, save_config
from archivist_cli.registry import default_registry

logger = logging.getLogger(__name__)


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
    """Copie le référentiel dans le dossier app data et enregistre son URI."""
    _require_file_uri(uri, "referentiel")
    try:
        installed_uri = install_referentiel(uri)
    except FileNotFoundError as e:
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
    required=True,
    help="URI du fichier référentiel (file:///path/to/referentiel.yaml).",
)
@click.option(
    "--target",
    required=True,
    help="URI du dossier cible (file:///path/to/target).",
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
    referentiel: str,
    target: str,
    extra_options: tuple[str, ...],
    dry_run: bool,
) -> None:
    """Crée l'arborescence de dossiers cible à partir du référentiel."""
    _require_file_uri(referentiel, "referentiel")
    _require_file_uri(target, "target")
    options = {"core"} | set(extra_options)
    ref = default_registry.resolve("referentiel", "yaml_file", {"uri": referentiel})
    fs = default_registry.resolve("fs", "local", {})

    result = scaffold(
        referentiel=ref,
        filesystem=fs,
        target_uri=target,
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
    required=True,
    help="URI du fichier référentiel (file:///path/to/referentiel.yaml).",
)
@click.option(
    "--target",
    required=True,
    help="URI du dossier racine de l'archive (file:///path/to/archive).",
)
def scan_cmd(referentiel: str, target: str) -> None:
    """Scanne _Réception, sauvegarde dans _Conservation brut, extrait les métadonnées."""
    _require_file_uri(referentiel, "referentiel")
    _require_file_uri(target, "target")

    ref = default_registry.resolve("referentiel", "yaml_file", {"uri": referentiel})
    fs = default_registry.resolve("fs", "local", {})
    extractor = default_registry.resolve("metadata", "kreuzberg", {})

    entries = ref.load_entries()

    def _find_role(role: str) -> str:
        matches = [e for e in entries if e.role == role]
        if len(matches) != 1:
            raise click.UsageError(
                f"Le référentiel contient {len(matches)} entrée(s) role={role!r} — exactement 1 attendue"
            )
        return matches[0].path

    reception_path = _find_role("reception")
    backup_path = _find_role("conservation_brut")

    target_base = target.rstrip("/")
    reception_uri = f"{target_base}/{reception_path}"
    backup_uri = f"{target_base}/{backup_path}"

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
        "deleted": result.deleted,
        "files": files_out,
    }))


@main.command(name="classify")
@click.option(
    "--referentiel",
    required=True,
    help="URI du fichier référentiel (file:///path/to/referentiel.yaml).",
)
@click.option(
    "--target",
    required=True,
    help="URI du dossier racine de l'archive (file:///path/to/archive).",
)
@click.option(
    "--llm",
    "llm_name",
    required=True,
    help="Adaptateur LLM à utiliser (ex: claude-cli).",
)
def classify_cmd(referentiel: str, target: str, llm_name: str) -> None:
    """Classe les fichiers de _Réception via LLM et les déplace vers le bon dossier."""
    _require_file_uri(referentiel, "referentiel")
    _require_file_uri(target, "target")

    ref = default_registry.resolve("referentiel", "yaml_file", {"uri": referentiel})
    fs = default_registry.resolve("fs", "local", {})
    extractor = default_registry.resolve("metadata", "kreuzberg", {})
    llm = default_registry.resolve("llm", llm_name, {})

    entries = ref.load_entries()

    def _find_role(role: str) -> str:
        matches = [e for e in entries if e.role == role]
        if len(matches) != 1:
            raise click.UsageError(
                f"Le référentiel contient {len(matches)} entrée(s) role={role!r} — exactement 1 attendue"
            )
        return matches[0].path

    for role in ("reception", "conservation_brut", "non_classe"):
        path = _find_role(role)
        role_uri = f"{target.rstrip('/')}/{path}"
        if not fs.is_dir(role_uri):
            raise click.UsageError(
                f"Dossier manquant : {role_uri!r} — lancez scaffold d'abord"
            )

    uc = ClassifyUseCase(
        fs=fs,
        referentiel=ref,
        extractor=extractor,
        llm=llm,
        index=NoopIndex(),
    )
    result = uc.run(ClassifyConfig(referentiel_uri=referentiel, target_uri=target))

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
