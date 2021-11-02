import typer
import os
import pprint
import dotenv
from pathlib import Path
from tabulate import tabulate
from bench.pipeline import Pipeline
from bench.dash import Frame, DashApp

app = typer.Typer()

# loading the .env as global
DEFAULT_ENV = Path.home() / "bench" / "envs" / ".env"

if DEFAULT_ENV.exists():
    CONFIG = dotenv.dotenv_values(DEFAULT_ENV)
    try:
        PATH = CONFIG["ENV_PATH"]
    except Exception:
        typer.echo("The ENV_PATH has not yet been written to the DEFAULT_ENV file.")
    try:
        ENVIRONMENT = dotenv.load_dotenv(PATH)
    except NameError:
        pass


@app.command()
def init(dir: str = typer.Option("", "--directory", "-d")):
    """
    Creates the required Bench directory tree structure in the user's home directory
    If --dir / -d is used, creates the required directory at the absolute path
    """
    # Create a directory at the specified path
    if dir:
        user_dir = Path(dir).resolve()
        try:
            user_env_dir = (user_dir / "bench" / "envs").mkdir(parents=True)
            user_log_dir = (user_dir / "bench" / "logs").mkdir(parents=True)
            user_new_dir = user_dir / "bench"

            # create the .env file
            try:
                (user_new_dir / "envs" / ".env").touch()
                user_env_file = user_new_dir / "envs" / ".env"
                with open(user_env_file, "w") as inpath:
                    inpath.write(f"ENV_PATH={user_env_file}")
            except FileExistsError:
                pass
            typer.echo(f"The directory has been created at: {user_new_dir}")
        except FileExistsError:
            user_exists_dir = user_dir / "bench"
            typer.echo(f"The directory already exists at: {user_exists_dir}")

    # Default behaviour will build configs in the home directory and create a .env file
    default_dir = Path.home()
    default_dir = Path(default_dir).resolve()
    try:
        _env_dir = (default_dir / "bench" / "envs").mkdir(parents=True)
        _log_dir = (default_dir / "bench" / "logs").mkdir(parents=True)
        new_dir = default_dir / "bench"

        # create the .env file and write the DEFAULT_ENV path
        try:
            (new_dir / "envs" / ".env").touch()
            env_file = new_dir / "envs" / ".env"
            with open(env_file, "w") as inpath:
                inpath.write(f"ENV_PATH={env_file}")
        except FileExistsError:
            pass
        if not dir:
            typer.echo(f"The directory has been created at: {new_dir}")
    except FileExistsError:
        exists_dir = default_dir / "bench"
        if not dir:
            typer.echo(f"The directory already exists at: {exists_dir}")


@app.command()
def env(use: str = typer.Option("", "--use", "-u", help="path to .env")):
    """
    Activates the environment
    The default .env is located under $HOME/bench/envs/.env
    Can use the "--use" / "-u" flag to specify the path to the custom .env under the bench directory tree
    """

    def test_dir(root):
        env_dir_child = (root / "envs").resolve()
        log_dir_child = (root / "logs").resolve()
        _env_dir = env_dir_child.is_dir()
        _log_dir = log_dir_child.is_dir()
        if (_env_dir, _log_dir) == (True, True):
            return 1
        else:
            return 0

    # Specify the environment directory
    if use:
        bench_dir = Path(use).parent.parent
        if not bench_dir.exists():
            typer.echo(
                """
                The bench directory doesn't exist
                See "bench init --help"
                """
            )
        else:
            if test_dir(bench_dir) == 1:
                pass
            else:
                typer.echo(
                    """
                    \nThe bench directory tree at {} does not contain the required subdirectories
                    \nUse the init command to create a new directory
                    """.format(
                        bench_dir
                    )
                )
                raise typer.Exit(1)
    else:
        bench_dir = Path.home() / "bench"
        if not bench_dir.exists():
            typer.echo(
                """
                The bench directory doesn't exist
                See "bench init --help"
                """
            )
            raise typer.Exit(1)
        else:
            if test_dir(bench_dir) == 1:
                pass
            else:
                typer.echo(
                    """
                    \nThe bench directory tree at {} does not contain the required subdirectories
                    \nUse the init command to create a new directory
                    """.format(
                        bench_dir
                    )
                )
                raise typer.Exit(1)

    if use:
        if Path(use).exists():
            env_path = Path(use)
            typer.echo(f"The environment has been activated at {env_path}")
        else:
            typer.echo("The specified .env file was not found")
            raise typer.Exit(1)
    else:
        env_path = Path.home() / "bench" / "envs" / ".env"
        typer.echo(f"The environment has been activated at {env_path}")

    dotenv.set_key(DEFAULT_ENV, "ENV_PATH", f"{env_path}")


@app.command()
def add(ticker: str):
    """
    Adds a symbol to the .env. Will re-order the list in alphabetical order.
    """
    ticker = ticker.upper()
    if os.getenv("BENCH_WATCHLIST") is None:
        typer.echo("The 'BENCH_WATCHLIST' environment variable has not been created.")
    elif len(os.getenv("BENCH_WATCHLIST")) == 0:
        watchlist = []
        watchlist.append(ticker)
        sorted_watchlist = sorted(watchlist)
        watchlist_csv = ",".join(sorted_watchlist)
        dotenv.set_key(PATH, "BENCH_WATCHLIST", watchlist_csv)
        typer.echo(f"{ticker} has been added to the watchlist!")
    else:
        watchlist = os.getenv("BENCH_WATCHLIST")
        watchlist_to_list = watchlist.split(",")
        if ticker in watchlist_to_list:
            typer.echo(f"{ticker} is already on the watchlist!")
        else:
            watchlist_to_list.append(ticker)
            sorted_watchlist = sorted(watchlist_to_list)
            watchlist_csv = ",".join(sorted_watchlist)
            dotenv.set_key(PATH, "BENCH_WATCHLIST", watchlist_csv)
            typer.echo(f"{ticker} has been added to the watchlist!")


@app.command()
def remove(ticker: str):
    """
    Removes a symbol from the .env. Will re-order the list in alphabetical order.
    """
    ticker = ticker.upper()
    if os.getenv("BENCH_WATCHLIST") is None:
        typer.echo("The 'BENCH_WATCHLIST' environment variable has not been created.")
    elif len(os.getenv("BENCH_WATCHLIST")) == 0:
        typer.echo("The watchlist is empty.")
    else:
        watchlist = os.getenv("BENCH_WATCHLIST")
        watchlist_to_list = watchlist.split(",")
        if ticker in watchlist_to_list:
            watchlist_to_list.remove(ticker)
            sorted_watchlist = sorted(watchlist_to_list)
            watchlist_csv = ",".join(sorted_watchlist)
            dotenv.set_key(PATH, "BENCH_WATCHLIST", watchlist_csv)
            typer.echo(f"{ticker} has been removed from the watchlist!")
        else:
            typer.echo(f"{ticker} is not in the watchlist!")


@app.command()
def watchlist():
    """
    Displays the watchlist in the .env file
    """
    if os.getenv("BENCH_WATCHLIST") is None or len(os.getenv("BENCH_WATCHLIST")) == 0:
        typer.echo("The watchlist is empty.")
    else:
        watchlist = os.getenv("BENCH_WATCHLIST")
        watchlist = watchlist.split(",")
        table = [[i] for i in watchlist]
        print(tabulate(table, tablefmt="simple"))


@app.command()
def pipeline(
    interval: str = typer.Option(..., "--interval", "-i"),
    number: int = typer.Option(..., "--number", "-n"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    """
    Runs the Bench pipeline.
    """
    job = Pipeline(period=interval, num_periods=number, verbose=verbose)
    job.run()


@app.command()
def dash():
    """
    Runs the Dash app at localhost:8050
    """
    data = Frame().dataframe()
    app = DashApp(data)
    app.run(data)


if __name__ == "__main__":
    app()
