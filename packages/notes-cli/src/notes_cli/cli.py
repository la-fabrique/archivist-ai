from __future__ import annotations

import dataclasses
import json
import logging

import click

from cli_core.domain.ports import ConfigError, ConfigStore
from notes_cli.config import AppConfig
from notes_cli.registry import default_registry

logger = logging.getLogger(__name__)


def _config_store() -> ConfigStore:
    return default_registry.resolve("config", "yaml_file", {"app_name": "notes"})


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


@config_set.command(name="llm")
@click.argument("nom")
def config_set_llm(nom: str) -> None:
    """Enregistre l'adaptateur LLM dans la config."""
    names = default_registry.names("llm")
    if nom not in names:
        raise click.BadParameter(
            f"{nom!r} inconnu. Valeurs possibles : {', '.join(names)}",
            param_hint="'NOM'",
        )
    try:
        store = _config_store()
        cfg = AppConfig.from_dict(store.load())
        store.save(dataclasses.replace(cfg, llm=nom).to_dict())
    except ConfigError as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(json.dumps({"llm": nom}))


@config_group.command(name="show")
def config_show() -> None:
    """Affiche la configuration persistée en JSON."""
    try:
        data = AppConfig.from_dict(_config_store().load()).to_dict()
    except ConfigError as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(json.dumps(data))
