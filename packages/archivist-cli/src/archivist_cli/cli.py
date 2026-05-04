from __future__ import annotations

import json
import logging
from pathlib import Path
from urllib.parse import urlparse

import click

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
    "--source",
    required=True,
    help="URI du dossier source (file:///path/to/docs).",
)
def scan_cmd(source: str) -> None:
    """Scanne un dossier et liste les fichiers trouvés."""
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
