import click


def sync_options(func):
    options = [click.option("--name"), click.option("--password"), click.option("--ip")]
    for option in reversed(options):
        func = option(func)
    return func


def generate_command(username, ip, password, path, service_name: str) -> str:
    command = (
        f"kubectl exec deployment/{service_name} --container {service_name} -- "
        f"/bin/sh -c \"sshpass -p '{password}' rsync -avzh"
        f' {username}@{ip}:{path} /home/syneto-{service_name}"'
    )
    return command
