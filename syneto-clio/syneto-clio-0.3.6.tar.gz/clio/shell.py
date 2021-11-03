import subprocess

import click


class Shell:
    @staticmethod
    def run(command: str, without_stdout=False, without_encoding=True):
        try:
            result = subprocess.run(
                [command],
                shell=True,
                stdout=None if without_stdout is True else subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding=None if without_encoding is True else "utf-8",
            )
            return result
        except result.stderr as e:
            raise Exception(f"Error while executing command {command}: {e}")

    @staticmethod
    def run_cleanup_command(cleanup_type):
        try:
            result = Shell.run(f"docker {cleanup_type} prune -f", without_encoding=False)
        except result.stderr as e:
            click.echo(f"Error while executing cleanup command: {e}")
            return
        formatted_result = result.stdout.split("\n")
        for line in formatted_result:
            if line.startswith("Total reclaimed space"):
                click.echo(f"After {cleanup_type} cleanup:")
                click.echo(line + "\n")
                break
