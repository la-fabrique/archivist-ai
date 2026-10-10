from __future__ import annotations

import json
import logging
from urllib.parse import urlparse

import click

from notes_cli.config import AppConfig, load_config, save_config

logger = logging.getLogger(__name__)

_FILE_SCHEMES = {"file"}


def _require_file_uri(value: str, param_name: str) -> None:
    if urlparse(value).scheme not in _FILE_SCHEMES:
        raise click.BadParameter(
            f"{value!r} n'est pas un URI valide. Utilisez file:///chemin/vers/{param_name}",
            param_hint=f"'--{param_name}'",
        )


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx: click.Context) -> None:
    """notes — dialogue avec un vault de notes."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@main.group(name="config")
def config_group() -> None:
    """Gère la configuration persistante."""


@config_group.group(name="set")
def config_set() -> None:
    """Définit un paramètre de configuration."""


@config_set.command(name="vault")
@click.argument("uri")
def config_set_vault(uri: str) -> None:
    """Enregistre le chemin du vault de notes (file:///path/to/vault)."""
    _require_file_uri(uri, "vault")
    save_config(AppConfig(vault=uri))
    click.echo(json.dumps({"vault": uri}))


@config_group.command(name="show")
def config_show() -> None:
    """Affiche la configuration persistée en JSON."""
    cfg = load_config()
    data: dict[str, str] = {}
    if cfg.vault is not None:
        data["vault"] = cfg.vault
    click.echo(json.dumps(data))
