import typer

from . import auth, bucket, api_tokens

app = typer.Typer()
app.add_typer(auth.user, name="user", help="User related stuff")
# TODO: Maybe there's a better way instead
# of calling the decorator in this way?
app.command("login")(auth.login_with_email_or_token)
app.command("logout")(auth.logout)
app.add_typer(bucket.app, name="bucket", help="Manage your buckets")
app.add_typer(api_tokens.app, name="api_tokens", help="Manage your API tokens")
