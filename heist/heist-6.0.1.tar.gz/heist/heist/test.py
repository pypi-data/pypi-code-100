from typing import Dict


async def run(hub, remotes: Dict[str, Dict[str, str]], artifact_version=None, **kwargs):
    hub.log.info(
        "This is a test heist manager. You have installed heist correctly. "
        "Install a heist manager to use full functionality"
    )
    return True
