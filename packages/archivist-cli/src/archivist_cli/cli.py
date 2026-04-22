import click


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx: click.Context) -> None:
    """archivist — OCR et classement de documents."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
