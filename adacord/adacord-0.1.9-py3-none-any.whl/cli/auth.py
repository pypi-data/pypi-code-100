import typer

from . import commons
from .api import create_api
from .exceptions import cli_wrapper

user = typer.Typer()


@user.command()
@cli_wrapper
def create():
    """
    Create a new user.
    """
    typer.echo("Hey there 👋")

    email = typer.prompt("> What's your email?")
    password = typer.prompt(
        "> What's your password?", hide_input=True, confirmation_prompt=True
    )

    api = create_api(with_auth=False)
    api.User.create(email, password)

    typer.echo(
        typer.style(
            "Awesome, check your email to confirm your email address!",
            fg=typer.colors.WHITE,
            bold=True,
        )
    )


@cli_wrapper
def login_with_email_or_token(
    email: str = typer.Option(None, help="Your user's email."),
    token: str = typer.Option(None, help="Your API or Bucket token."),
):
    """
    Use the cli to log-in (with email/password or api/bucket token).
    """
    if not email and not token:
        typer.echo(
            typer.style(
                "You need to pass your user'email or a token.",
                fg=typer.colors.RED,
                bold=True,
            )
        )
        raise typer.Exit()
    auth = {}
    if email:
        password = typer.prompt("> What's your password?", hide_input=True)
        api = create_api(with_auth=False)
        response = api.User.login(email, password)
        auth["email"] = email
        auth["token"] = response["access_token"]
    elif token:
        auth["token"] = token
    commons.save_auth(auth)


@cli_wrapper
def logout():
    """
    To Logout. For real.
    """
    commons.save_auth({})


@user.command()
@cli_wrapper
def reset_password(email: str = typer.Option(...)):
    """
    Reset your user's password
    """
    api = create_api(with_auth=False)
    api.User.request_password_reset(email)
    typer.echo(
        typer.style(
            "Awesome, check your email for the next steps for the password reset!",
            fg=typer.colors.WHITE,
            bold=True,
        )
    )


@user.command()
@cli_wrapper
def email_verification(email: str = typer.Option(...)):
    """
    Request a new email verification email
    """
    password = typer.prompt("> What's your password?", hide_input=True)
    api = create_api(with_auth=False)
    api.User.request_verification_email(email, password)
    typer.echo(
        typer.style(
            "Awesome, check your email to confirm your email address!",
            fg=typer.colors.WHITE,
            bold=True,
        )
    )
