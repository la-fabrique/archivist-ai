from __future__ import annotations

import dataclasses
import json
import logging
import os

import click

from cli_core.domain.ports import ConfigError, ConfigStore
from notes_cli.application.add_idea import AddIdea
from notes_cli.config import AppConfig
from notes_cli.domain.ports import Agent, AgentError
from notes_cli.registry import default_registry

logger = logging.getLogger(__name__)


def _config_store() -> ConfigStore:
    return default_registry.resolve("config", "yaml_file", {"app_name": "notes"})


def _agent(cfg: AppConfig) -> Agent:
    return default_registry.resolve("agent", cfg.agent, {"workspace": cfg.bloc_notes})


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


@main.group(name="add")
def add_group() -> None:
    """Ajoute une note au bloc-notes via l'agent."""


@add_group.command(name="idea")
@click.argument("idee", required=False)
@click.option("--session", "session_id", default=None, help="Identifiant de session à reprendre.")
@click.option("--reply", "reply_text", default=None, help="Réponse à la question de l'agent.")
def add_idea(idee: str | None, session_id: str | None, reply_text: str | None) -> None:
    """Ajoute une idée (premier tour) ou répond à l'agent (--session + --reply)."""
    if idee is not None and reply_text is not None:
        raise click.UsageError("Fournir soit IDEE, soit --session avec --reply, pas les deux.")
    if (session_id is None) != (reply_text is None):
        raise click.UsageError("--session et --reply vont ensemble.")
    if idee is None and reply_text is None:
        raise click.UsageError("Fournir IDEE, ou --session avec --reply.")
    if idee is not None and not idee.strip():
        raise click.UsageError("IDEE ne peut pas être vide.")

    try:
        cfg = AppConfig.from_dict(_config_store().load())
    except ConfigError as exc:
        raise click.ClickException(str(exc)) from exc
    if not cfg.agent:
        raise click.ClickException(
            "Agent non configuré. Lance : notes config set agent claude-code"
        )
    if not cfg.bloc_notes:
        raise click.ClickException(
            "Bloc-notes non configuré. Lance : notes config set bloc-notes <chemin>"
        )
    if not os.path.isdir(cfg.bloc_notes):
        raise click.ClickException(
            f"Le dossier du bloc-notes n'existe plus : {cfg.bloc_notes}. "
            "Lance : notes config set bloc-notes <chemin>"
        )

    use_case = AddIdea(_agent(cfg))
    try:
        if idee is not None:
            reply = use_case.start(idee)
        else:
            assert session_id is not None and reply_text is not None
            reply = use_case.reply(session_id, reply_text)
    except AgentError as exc:
        message = str(exc)
        if exc.session_id:
            message += (
                f"\nSession : {exc.session_id}"
                f"\nReprendre : notes add idea --session {exc.session_id} --reply \"<ta réponse>\""
            )
        raise click.ClickException(message) from exc

    click.echo(
        json.dumps(
            {
                "session": reply.session_id,
                "reponse": reply.text,
                "suite": f'notes add idea --session {reply.session_id} --reply "<ta réponse>"',
            },
            ensure_ascii=False,
        )
    )
