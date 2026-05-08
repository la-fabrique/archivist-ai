from __future__ import annotations

import json
import logging
from pathlib import Path
from urllib.parse import urlparse

import click

from archivist_cli.adapters.index.noop import NoopIndex
from archivist_cli.application.scaffold import scaffold
from archivist_cli.application.scan import scan
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
