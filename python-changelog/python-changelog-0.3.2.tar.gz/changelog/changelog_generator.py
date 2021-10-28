import click
import os
import git

from changelog.gitrepo import Repo

filename = 'CHANGELOG.md'
branch = 'main'
types = 'feat,fix,chore,docs,refactor,test'
bodytags = 'BREAKING CHANGE,MAJOR'

branch_desctiption = 'git branch'
types_desctiption = 'commit types to show in changelog'
bodytags_description = 'body tags that schould be shown in changelog'

@click.group()
def generator():
    pass

@generator.command()
@click.argument('repopath', default='.')
@click.option("--branch", default=branch, help=branch_desctiption)
@click.option("--types", default=types, help=types_desctiption)
@click.option("--bodytags", default=bodytags, help=bodytags_description)
def generate(repopath, branch, types, bodytags):
    repo = Repo(repopath, branch)
    types = types.split(',')
    bodytags = bodytags.split(',')
    text = repo.generate_changelog(types, bodytags)
    if text:
        with open(os.path.join(repopath, filename), 'w') as out_file:
            out_file.write(text)
        print('Done!')

@generator.command()
@click.argument('repopath', default='.')
@click.option("--branch", default=branch, help=branch_desctiption)
@click.option("--types", default=types, help=types_desctiption)
@click.option("--bodytags", default=bodytags, help=bodytags_description)
def add(repopath, branch, types, bodytags):
    repo = Repo(repopath, branch)
    types = types.split(',')
    bodytags = bodytags.split(',')
    try:
        with open(os.path.join(repopath, filename), 'r') as in_file:
            old_text = in_file.read()
    except FileNotFoundError:
        print("No CHANGELOG.md found")
        return
    text = repo.add_changelog(old_text, types, bodytags)
    if text:
        with open(os.path.join(repopath, filename), 'w') as out_file:
            out_file.write(text)
        print('Done!')

@generator.command()
@click.argument('repopath', default='.')
@click.option("--branch", default=branch, help=branch_desctiption)
@click.option("--types", default=types, help=types_desctiption)
@click.option("--bodytags", default=bodytags, help=bodytags_description)
def printout(repopath, branch, types, bodytags):
    repo = Repo(repopath, branch)
    types = types.split(',')
    bodytags = bodytags.split(',')
    print(repo.generate_changelog(types, bodytags))

if __name__ == '__main__':
    generator()
