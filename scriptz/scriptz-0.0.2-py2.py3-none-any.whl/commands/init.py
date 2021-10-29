from pathlib import Path

from scriptz import cli, Manager


@cli.command()
def init():
    """ Initialize current directory for scriptz. """
    manager = Manager()

    manager.check(
        not manager.ini_path.exists(),
        f"scriptz already initialized ({manager.ini_path.absolute()}).",
    )

    ini_content = (Path(__file__).parent.parent / "scriptz.ini").read_text()
    manager.ini_path.write_text(ini_content)

    manager.check(
        manager.ini_path.is_file(),
        error_msg=f"scriptz initialization ({manager.ini_path}) failed.",
        ok_msg=f"scriptz initialized ({manager.ini_path}) successfully.",
    )
