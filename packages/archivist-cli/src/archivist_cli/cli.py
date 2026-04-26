from __future__ import annotations

import json

import click

from archivist_cli.adapters.fs.local import LocalFilesystem
from archivist_cli.adapters.referentiel.yaml_file import YamlFileReferentiel
from archivist_cli.application.scaffold import scaffold


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx: click.Context) -> None:
    """archivist — OCR et classement de documents."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@main.command()
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
    options = {"core"} | set(extra_options)
    ref = YamlFileReferentiel(uri=referentiel)
    fs = LocalFilesystem()

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


main.add_command(scaffold_cmd, "scaffold")
