from scriptz import cli, __version__, console


@cli.command()
def version():
    """ Display version information. """
    console.print(f"scriptz: version {__version__}")
