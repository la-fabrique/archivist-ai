from __future__ import annotations

import json
import logging
from urllib.parse import urlparse

import click

from notes_cli.config import AppConfig, load_config, save_config

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
    """notes — dialogue avec un vault de notes."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@main.group(name="config")
def config_group() -> None:
    """Gère la configuration persistante de la CLI."""


@config_group.group(name="set")
def config_set() -> None:
    """Définit un paramètre de configuration."""


@config_set.command(name="vault")
@click.argument("uri")
def config_set_vault(uri: str) -> None:
    """Enregistre le chemin du vault de notes (file:///path/to/vault)."""
    _require_file_uri(uri, "vault")
    cfg = load_config()
    save_config(AppConfig(vault=uri, llm=cfg.llm))
    click.echo(json.dumps({"vault": uri}))


@config_set.command(name="llm")
@click.argument("nom")
def config_set_llm(nom: str) -> None:
    """Enregistre l'adaptateur LLM dans la config."""
    cfg = load_config()
    save_config(AppConfig(vault=cfg.vault, llm=nom))
    click.echo(json.dumps({"llm": nom}))


@config_group.command(name="show")
def config_show() -> None:
    """Affiche la configuration persistée en JSON."""
    cfg = load_config()
    data: dict[str, str] = {}
    if cfg.vault is not None:
        data["vault"] = cfg.vault
    if cfg.llm is not None:
        data["llm"] = cfg.llm
    click.echo(json.dumps(data))
