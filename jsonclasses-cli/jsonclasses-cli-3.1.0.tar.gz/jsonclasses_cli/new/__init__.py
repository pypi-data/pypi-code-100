from typing import Literal
from pathlib import Path
from rich import print
from rich.prompt import Prompt
from .app_content import app_content
from .req_content import req_content
from .conf_content import conf_content
from .mypy_content import mypy_content
from .gitignore_content import gitignore_content
from .readme_content import readme_content
from .env_content import env_content
from ..utils.yesno import yesno
from ..utils.write_file import write_file
from ..utils.run import run


def new(dest: Path,
        interactive: bool | None,
        http_library: Literal['flask', 'fastapi'] | None,
        include_user: bool | None,
        include_admin: bool | None,
        git_init: bool | None,
        venv: bool | None):
    if interactive:
        if http_library is None:
            http_library = Prompt.ask('Which HTTP library would you use?', choices=["Flask", "FastAPI"], default="Flask").lower()
        if include_user is None:
            include_user = yesno(Prompt.ask('Do you want a user model?', choices=['Yes', 'No'], default='Yes'))
        if include_admin is None:
            include_admin = yesno(Prompt.ask('Do you want an admin model?', choices=['Yes', 'No'], default='Yes'))
        if git_init is None:
            git_init = yesno(Prompt.ask('Init git repo?', choices=['Yes', 'No'], default='Yes'))
        if venv is None:
            venv = yesno(Prompt.ask('Create a virtual env?', choices=['Yes', 'No'], default='Yes'))
    else:
        if http_library is None:
            http_library = 'flask'
        if include_user is None:
            include_user = False
        if include_admin is None:
            include_admin = False
        if git_init is None:
            git_init = True
        if venv is None:
            venv = True
    write_file(dest / 'app.py', app_content(http_library=http_library, include_user=include_user, include_admin=include_admin))
    write_file(dest / 'requirements.txt', req_content(http_library=http_library, include_user=include_user, include_admin=include_admin))
    write_file(dest / 'config.json', conf_content(http_library=http_library, include_user=include_user, include_admin=include_admin))
    write_file(dest / 'mypy.ini', mypy_content())
    write_file(dest / '.gitignore', gitignore_content())
    write_file(dest / 'README.md', readme_content(dest))
    write_file(dest / '.env', env_content())
    if git_init:
        if not (dest / '.git').is_dir():
            run('git init')
    if venv:
        if not ((dest / 'venv').is_dir() or (dest / '.venv').is_dir()):
            dest_venv = dest / '.venv'
            run(f'python3 -m venv {dest_venv}')
    if venv:
        venv_dir = dest / 'venv' if (dest / 'venv').is_dir() else dest / '.venv'
        venv_act = venv_dir / 'bin/activate'
        run(f'source {venv_act}; pip install -r requirements.txt')
    else:
        run('pip install -r requirements.txt')
    print("🎉[green]Project is successfully created.[/green]")
    match http_library:
        case 'flask':
            print("\n    Run 'flask run' to start the development server.\n")
