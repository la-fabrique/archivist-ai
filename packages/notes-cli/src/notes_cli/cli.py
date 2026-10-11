from __future__ import annotations

import dataclasses
import json
import logging
import os

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


def _save(**changes: str) -> None:
    try:
        store = _config_store()
        cfg = AppConfig.from_dict(store.load())
        store.save(dataclasses.replace(cfg, **changes).to_dict())
    except ConfigError as exc:
        raise click.ClickException(str(exc)) from exc


@config_set.command(name="agent")
@click.argument("nom")
def config_set_agent(nom: str) -> None:
    """Enregistre l'adaptateur d'agent dans la config."""
    names = default_registry.names("agent")
    if nom not in names:
        raise click.BadParameter(
            f"{nom!r} inconnu. Valeurs possibles : {', '.join(names)}",
            param_hint="'NOM'",
        )
    _save(agent=nom)
    click.echo(json.dumps({"agent": nom}))


@config_set.command(name="bloc-notes")
@click.argument("chemin")
def config_set_bloc_notes(chemin: str) -> None:
    """Enregistre le dossier du bloc-notes dans la config."""
    path = os.path.abspath(os.path.expanduser(chemin))
    if not os.path.isdir(path):
        raise click.BadParameter(
            f"{path!r} n'est pas un dossier existant.", param_hint="'CHEMIN'"
        )
    _save(bloc_notes=path)
    click.echo(json.dumps({"bloc-notes": path}))


@config_group.command(name="show")
def config_show() -> None:
    """Affiche la configuration persistée en JSON."""
    try:
        data = AppConfig.from_dict(_config_store().load()).to_dict()
    except ConfigError as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(json.dumps(data))
