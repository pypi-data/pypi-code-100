from setuptools import setup
from setuptools.command.develop import develop
from subprocess import check_call


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        try:
            print('Installing pre-commit ...')
            check_call([
                'pre-commit', 'install',
                '--hook-type', 'pre-commit',
                '--hook-type', 'commit-msg',
                '--hook-type', 'post-commit'
            ])
        finally:
            develop.run(self)


setup(
    cmdclass={
        'develop': PostDevelopCommand
    }
)
